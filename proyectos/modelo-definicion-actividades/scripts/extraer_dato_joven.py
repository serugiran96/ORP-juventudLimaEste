"""Extrae de Dato Joven los conjuntos de datos de la Capa 1 (solo consultas agregadas).

Uso (desde la carpeta del proyecto):
    python scripts/extraer_dato_joven.py todo
    python scripts/extraer_dato_joven.py poblacion encuestas consolidado renoj voluntariado

Salida: data/raw/dato_joven/*.csv y data/raw/dato_joven/_metadatos.json
(la carpeta data/ no se sube al repositorio).

Los registros sensibles (CNV, CEM, discapacidad) no están incluidos todavía: su
extracción depende de una decisión sobre la ocultación de celdas pequeñas.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from powerbi_publico import ReportePBI

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "raw" / "dato_joven"
CATALOGO = RAIZ / "fuentes" / "catalogo_tableros_dato_joven.csv"

CLAVE_DEMOGRAFIA = "ebddf39c-9fde-4695-9385-4ff363a3ffcf"
CLAVE_CONSOLIDADO = "e53bf32b-4313-45fa-966b-33172bd8d50f"
CLAVE_RENOJ = "a8e15d92-0bea-4689-8269-cbf2f1161419"
CLAVE_VOLUNTARIADO = "b6d288e4-c6a4-4890-a3e7-90f63632e731"

PROVINCIA_LIMA = "1501"  # Lima Metropolitana: 43 distritos de la provincia de Lima
UBIGEO_NACIONAL = "000000"  # fila con el total del país en las tablas de población
REGIONES_ENCUESTA = ["LIMA METROPOLITANA", "NACIONAL"]


def _sin_prefijo(filas):
    """Quita el prefijo 't.' de los nombres de columna que agrega el cliente."""
    return pd.DataFrame([{k.removeprefix("t."): v for k, v in f.items()} for f in filas])


class Extractor:
    def __init__(self):
        SALIDA.mkdir(parents=True, exist_ok=True)
        self.ruta_meta = SALIDA / "_metadatos.json"
        self.meta = json.loads(self.ruta_meta.read_text()) if self.ruta_meta.exists() else {}
        self._reportes = {}
        self._distritos_lima = None

    def reporte(self, clave):
        if clave not in self._reportes:
            self._reportes[clave] = ReportePBI(clave)
        return self._reportes[clave]

    def guardar(self, df, nombre, clave, tablas, filtros, nota=""):
        ruta = SALIDA / f"{nombre}.csv"
        df.to_csv(ruta, index=False)
        self.meta[nombre] = {
            "archivo": ruta.name,
            "filas": len(df),
            "clave_reporte": clave,
            "tablas": tablas,
            "filtros": filtros,
            "ultima_actualizacion_tablero": self.reporte(clave).info["ultima_actualizacion"] if clave else None,
            "fecha_extraccion": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "nota": nota,
        }
        self.ruta_meta.write_text(json.dumps(self.meta, ensure_ascii=False, indent=2))
        print(f"  {ruta.name}: {len(df)} filas")

    def distritos_lima(self):
        """Códigos UBIGEO de los 43 distritos de Lima Metropolitana."""
        if self._distritos_lima is None:
            filas = self.reporte(CLAVE_DEMOGRAFIA).consultar(
                "dimDistrito", columnas=["ID_DIS", "DISTRITO", "ID_PROV"], filtros={"ID_PROV": [PROVINCIA_LIMA]})
            self._distritos_lima = _sin_prefijo(filas).rename(columns={"ID_DIS": "ubigeo", "DISTRITO": "distrito"})
        return self._distritos_lima

    # --- conjuntos de datos -----------------------------------------------------------

    def poblacion(self):
        print("Población (Datos Demográficos)")
        r = self.reporte(CLAVE_DEMOGRAFIA)
        ubigeos = list(self.distritos_lima()["ubigeo"])
        self.guardar(self.distritos_lima(), "distritos_lima_metropolitana", CLAVE_DEMOGRAFIA,
                     ["dimDistrito"], {"ID_PROV": PROVINCIA_LIMA})

        joven = _sin_prefijo(r.consultar(
            "factPoblacionJoven", columnas=["UBIGEO", "AÑO", "SEXO", "RANGO DE EDAD"],
            agregaciones={"POBLACION JOVEN": "suma"}, filtros={"UBIGEO": ubigeos}))
        self.guardar(joven, "poblacion_joven_distritos_lima", CLAVE_DEMOGRAFIA, ["factPoblacionJoven"],
                     {"UBIGEO": "43 distritos de Lima Metropolitana"})

        total = _sin_prefijo(r.consultar(
            "factPoblacionGeneral", columnas=["UBIGEO", "AÑO", "SEXO"],
            agregaciones={"POBLACION": "suma"}, filtros={"UBIGEO": ubigeos}))
        self.guardar(total, "poblacion_total_distritos_lima", CLAVE_DEMOGRAFIA, ["factPoblacionGeneral"],
                     {"UBIGEO": "43 distritos de Lima Metropolitana"})

        # Totales nacionales, como referencia. El total del país está en una fila propia
        # (UBIGEO "000000"): sumar todas las filas contaría dos veces a la población.
        nac_joven = _sin_prefijo(r.consultar("factPoblacionJoven", columnas=["AÑO", "SEXO", "RANGO DE EDAD"],
                                             agregaciones={"POBLACION JOVEN": "suma"},
                                             filtros={"UBIGEO": [UBIGEO_NACIONAL]}))
        self.guardar(nac_joven, "poblacion_joven_nacional", CLAVE_DEMOGRAFIA, ["factPoblacionJoven"],
                     {"UBIGEO": UBIGEO_NACIONAL})
        nac_total = _sin_prefijo(r.consultar("factPoblacionGeneral", columnas=["AÑO", "SEXO"],
                                             agregaciones={"POBLACION": "suma"},
                                             filtros={"UBIGEO": [UBIGEO_NACIONAL]}))
        self.guardar(nac_total, "poblacion_total_nacional", CLAVE_DEMOGRAFIA, ["factPoblacionGeneral"],
                     {"UBIGEO": UBIGEO_NACIONAL})

    def encuestas(self):
        print("Indicadores de encuestas (38 tableros)")
        catalogo = pd.read_csv(CATALOGO)
        catalogo = catalogo[catalogo["tipo"] == "encuesta"].drop_duplicates("clave")
        regionales, nacionales = [], []
        for _, fila in catalogo.iterrows():
            r = self.reporte(fila["clave"])
            esquema = r.esquema()
            for tabla, destino, filtros in [("datosRegionales", regionales, {"REGION": REGIONES_ENCUESTA}),
                                            ("datosNacionales", nacionales, {})]:
                columnas = [c for c in esquema[tabla] if not c.endswith("*")]
                df = _sin_prefijo(r.consultar(tabla, columnas=columnas, filtros=filtros))
                df = df.rename(columns={"ANIO": "AÑO"})
                df.insert(0, "tablero", fila["nombre"])
                df.insert(1, "categoria_portal", fila["categoria"])
                df.insert(2, "clave_reporte", fila["clave"])
                df["ultima_actualizacion_tablero"] = r.info["ultima_actualizacion"]
                destino.append(df)
            print(f"  {fila['nombre']}")
        self.guardar(pd.concat(regionales, ignore_index=True), "encuestas_regionales", None,
                     ["datosRegionales"], {"REGION": REGIONES_ENCUESTA},
                     "Un tablero por indicador; claves en la columna clave_reporte.")
        self.guardar(pd.concat(nacionales, ignore_index=True), "encuestas_nacionales", None,
                     ["datosNacionales"], {}, "Desagregaciones solo nacionales.")

    def consolidado(self):
        print("Tablero consolidado 'Indicadores regionales'")
        r = self.reporte(CLAVE_CONSOLIDADO)
        partes = []
        for tabla, columnas in r.esquema().items():
            cols = [c for c in columnas if not c.endswith("*")]
            if not tabla.startswith("fact") or "REGION" not in cols or "VALOR" not in cols:
                continue
            df = _sin_prefijo(r.consultar(tabla, columnas=cols, filtros={"REGION": REGIONES_ENCUESTA}))
            df.insert(0, "tabla", tabla)
            partes.append(df)
        self.guardar(pd.concat(partes, ignore_index=True), "consolidado_regionales", CLAVE_CONSOLIDADO,
                     sorted({p["tabla"].iloc[0] for p in partes if len(p)}), {"REGION": REGIONES_ENCUESTA})

    def renoj(self):
        print("RENOJ (organizaciones juveniles)")
        r = self.reporte(CLAVE_RENOJ)
        ubigeos = list(self.distritos_lima()["ubigeo"])
        columnas = ["UBIGEO", "AÑO ACREDITACIÓN", "TIPO DE ORGANIZACIÓN", "DETALLE TIPO DE ORGANIZACIÓN",
                    "TEMÁTICA DE ORGANIZACIÓN", "Temática de organización 1", "Temática de organización 2"]
        df = _sin_prefijo(r.consultar("Representantes", columnas=columnas, medidas=["Total de Organizaciones"],
                                      filtros={"UBIGEO": ubigeos}))
        self.guardar(df, "renoj_organizaciones_distritos_lima", CLAVE_RENOJ, ["Representantes"],
                     {"UBIGEO": "43 distritos de Lima Metropolitana"},
                     "Conteo de organizaciones por combinación de atributos. No incluye datos de miembros.")

    def voluntariado(self):
        print("Programa de Voluntariado Juvenil")
        r = self.reporte(CLAVE_VOLUNTARIADO)
        ubigeos = list(self.distritos_lima()["ubigeo"])
        esquema = r.esquema()["fact_Voluntarios"]
        # Variables de perfil, participación, intereses y experiencia. Se excluyen a propósito
        # los campos sensibles (salud, discapacidad, comunidades, nacionalidad) y los de texto libre.
        variables = (["RANGO_EDAD", "SEXO", "NIVEL_EDUCATIVO", "OCUPACION", "AREA_ESTANDARIZADA",
                      "PARTICIPA_ORGANIZACIÓN_JUVENIL", "PARTICIPA_CONSEJO_DE_JUVENTUD", "PARTICIPA_VOLUNTARIADO",
                      "MODALIDAD_VOLUNTARIADO", "EXPERIENCIA_VOLUNTARIADO", "TIEMPO_EXPERIENCIA_VOLUNTARIADO"]
                     + [c for c in esquema if c.startswith(("INTERES_VOLUNTARIADO_", "EXPERIENCIA_VOLUNTARIADO_"))])
        partes = []
        total = _sin_prefijo(r.consultar("fact_Voluntarios", columnas=["UBIGEO"], medidas=["Total Voluntarios"],
                                         filtros={"UBIGEO": ubigeos}))
        total["variable"], total["valor"] = "TOTAL", "TOTAL"
        partes.append(total)
        for v in variables:
            df = _sin_prefijo(r.consultar("fact_Voluntarios", columnas=["UBIGEO", v], medidas=["Total Voluntarios"],
                                          filtros={"UBIGEO": ubigeos}))
            df = df.rename(columns={v: "valor"})
            df["variable"] = v
            partes.append(df)
        df = pd.concat(partes, ignore_index=True)[["UBIGEO", "variable", "valor", "Total Voluntarios"]]
        self.guardar(df, "voluntariado_distritos_lima", CLAVE_VOLUNTARIADO, ["fact_Voluntarios"],
                     {"UBIGEO": "43 distritos de Lima Metropolitana"},
                     "Conteos de personas inscritas por distrito y una variable a la vez. "
                     "Sin campos sensibles ni de texto libre.")


def main():
    conjuntos = ["poblacion", "encuestas", "consolidado", "renoj", "voluntariado"]
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("conjuntos", nargs="+", choices=conjuntos + ["todo"])
    args = p.parse_args()
    elegidos = conjuntos if "todo" in args.conjuntos else args.conjuntos
    ext = Extractor()
    for nombre in elegidos:
        getattr(ext, nombre)()


if __name__ == "__main__":
    main()
