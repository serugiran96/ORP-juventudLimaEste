"""Cliente mínimo para consultar reportes de Power BI "publicados en la web".

Usa los mismos endpoints públicos que el visor de Power BI (sin autenticación).
Microsoft no los documenta y pueden cambiar sin aviso: el flujo está descrito en
fuentes/exploracion_dato_joven.md (Anexo).

Uso básico:

    reporte = ReportePBI("ebddf39c-9fde-4695-9385-4ff363a3ffcf")
    filas = reporte.consultar(
        "factPoblacionJoven",
        columnas=["UBIGEO", "AÑO", "SEXO", "RANGO DE EDAD"],
        agregaciones={"POBLACION JOVEN": "suma"},
        filtros={"UBIGEO": ["150137"]},
    )

Solo se deben hacer consultas agregadas (conteos o sumas por grupo): nunca se
descargan registros individuales (ver reglas en exploracion_dato_joven.md, sección 5).
"""

import gzip
import json
import re
import time

import requests

API = "https://wabi-south-central-us-api.analysis.windows.net"
PAUSA_SEGUNDOS = 1.0  # como máximo una consulta por segundo
TAM_PAGINA = 10000

# Códigos de agregación de las consultas semánticas de Power BI.
AGREGACIONES = {"suma": 0, "promedio": 1, "conteo": 2, "min": 3, "max": 4, "conteo_no_nulos": 5}


class ErrorPBI(RuntimeError):
    pass


class ReportePBI:
    def __init__(self, clave, sesion=None):
        self.clave = clave
        self.sesion = sesion or requests.Session()
        self._info = None
        self._esquema = None

    # --- peticiones -----------------------------------------------------------------

    def _pedir(self, metodo, ruta, cuerpo=None, reintentos=3):
        cabeceras = {"Accept": "application/json", "X-PowerBI-ResourceKey": self.clave}
        for intento in range(reintentos):
            time.sleep(PAUSA_SEGUNDOS)
            resp = self.sesion.request(metodo, API + ruta, json=cuerpo, headers=cabeceras, timeout=120)
            if resp.status_code == 200:
                contenido = resp.content
                if contenido[:2] == b"\x1f\x8b":
                    contenido = gzip.decompress(contenido)
                return json.loads(contenido)
            if resp.status_code in (429, 500, 502, 503, 504) and intento < reintentos - 1:
                time.sleep(5 * (intento + 1))
                continue
            raise ErrorPBI(f"{metodo} {ruta}: HTTP {resp.status_code} {resp.text[:200]}")

    # --- metadatos ------------------------------------------------------------------

    @property
    def info(self):
        """modelId, datasetId, reportId, fecha de última actualización y páginas."""
        if self._info is None:
            d = self._pedir("GET", f"/public/reports/{self.clave}/modelsAndExploration?preferReadOnlySession=true")
            modelo = d["models"][0]
            self._info = {
                "model_id": modelo["id"],
                "dataset_id": modelo["dbName"],
                "report_id": d["exploration"]["report"]["objectId"],
                "ultima_actualizacion": modelo.get("LastRefreshTime"),
                "paginas": [s.get("displayName") for s in d["exploration"].get("sections", [])],
            }
        return self._info

    def esquema(self):
        """Diccionario {tabla: [columnas]}; las medidas llevan el sufijo '*'."""
        if self._esquema is None:
            d = self._pedir("POST", "/public/reports/conceptualschema",
                            {"modelIds": [self.info["model_id"]], "userPreferredLocale": "es-ES"})
            self._esquema = {}
            for s in d.get("schemas", []):
                for entidad in s["schema"].get("Entities", []):
                    self._esquema[entidad["Name"]] = [
                        p["Name"] + ("*" if "Measure" in p else "") for p in entidad.get("Properties", [])
                    ]
        return self._esquema

    # --- consultas ------------------------------------------------------------------

    def consultar(self, tabla, columnas=(), medidas=(), agregaciones=None, filtros=None, tam_pagina=TAM_PAGINA):
        """Devuelve una lista de diccionarios, una fila por combinación de `columnas`.

        columnas: columnas por las que se agrupa.
        medidas: medidas ya definidas en el modelo (nombres sin '*').
        agregaciones: {columna: "suma" | "conteo" | ...}.
        filtros: {columna: [valores]} (condición "está en").
        """
        agregaciones = agregaciones or {}
        filtros = filtros or {}
        seleccion = []
        for c in columnas:
            seleccion.append({**_col(c), "Name": f"t.{c}"})
        for m in medidas:
            seleccion.append({"Measure": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": m},
                              "Name": f"t.{m}"})
        for c, fn in agregaciones.items():
            seleccion.append({"Aggregation": {"Expression": _col(c), "Function": AGREGACIONES[fn]},
                              "Name": f"{fn}({c})"})
        consulta = {"Version": 2, "From": [{"Name": "t", "Entity": tabla, "Type": 0}], "Select": seleccion}
        if filtros:
            consulta["Where"] = [
                {"Condition": {"In": {"Expressions": [_col(c)],
                                      "Values": [[{"Literal": {"Value": _literal(v)}}] for v in valores]}}}
                for c, valores in filtros.items()
            ]

        filas, tokens = [], None
        while True:
            ventana = {"Count": tam_pagina}
            if tokens:
                ventana["RestartTokens"] = tokens
            cuerpo = {
                "version": "1.0.0",
                "cancelQueries": [],
                "modelId": self.info["model_id"],
                "queries": [{
                    "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
                        "Query": consulta,
                        "Binding": {"Primary": {"Groupings": [{"Projections": list(range(len(seleccion)))}]},
                                    "DataReduction": {"DataVolume": 3, "Primary": {"Window": ventana}},
                                    "Version": 1},
                    }}]},
                    "QueryId": "",
                    "ApplicationContext": {"DatasetId": self.info["dataset_id"],
                                           "Sources": [{"ReportId": self.info["report_id"]}]},
                }],
            }
            resultado = self._pedir("POST", "/public/reports/querydata?synchronous=true", cuerpo)
            nuevas, tokens = _decodificar(resultado)
            filas.extend(nuevas)
            if not tokens:
                # Al paginar, Power BI repite la fila de corte al inicio de la página
                # siguiente. Como cada fila es una combinación única de grupos, se
                # eliminan duplicados exactos.
                unicas = {tuple(f.items()): f for f in filas}
                return list(unicas.values())


def _col(nombre):
    return {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": nombre}}


def _literal(valor):
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, int):
        return f"{valor}L"
    if isinstance(valor, float):
        return f"{valor}D"
    return "'" + str(valor).replace("'", "''") + "'"


_NUM = re.compile(r"^(-?\d+(?:\.\d+)?)([LDM])$")


def _normalizar(valor):
    """Power BI a veces devuelve números como texto con sufijo de tipo ('479L', '0.5D')."""
    if isinstance(valor, str):
        m = _NUM.match(valor)
        if m:
            return int(m.group(1)) if m.group(2) == "L" else float(m.group(1))
    return valor


def _decodificar(resultado):
    """Decodifica el formato comprimido DSR. Devuelve (filas, tokens_para_la_siguiente_pagina)."""
    datos = resultado["results"][0]["result"]["data"]
    dsr = datos["dsr"]
    if "DS" not in dsr:
        raise ErrorPBI(json.dumps(dsr, ensure_ascii=False)[:600])
    ds = dsr["DS"][0]
    if "PH" not in ds:
        raise ErrorPBI(json.dumps(ds, ensure_ascii=False)[:600])
    nombres = {s["Value"]: s["Name"] for s in datos["descriptor"]["Select"]}
    diccionarios = ds.get("ValueDicts", {})

    filas, esquema, previa = [], None, None
    for fila in ds["PH"][0].get("DM0", []):
        if "S" in fila:
            esquema = fila["S"]
        repetidos, nulos = fila.get("R", 0), fila.get("Ø", 0)
        comprimidos = iter(fila["C"]) if "C" in fila else None
        actual = []
        for j, campo in enumerate(esquema):
            if repetidos >> j & 1:
                valor = previa[j]
            elif nulos >> j & 1:
                valor = None
            else:
                valor = next(comprimidos, None) if comprimidos is not None else fila.get(campo["N"])
                if "DN" in campo and isinstance(valor, int):
                    valor = diccionarios[campo["DN"]][valor]
            actual.append(valor)
        previa = actual
        filas.append({nombres.get(c["N"], c["N"]): _normalizar(v) for c, v in zip(esquema, actual)})
    return filas, ds.get("RT")
