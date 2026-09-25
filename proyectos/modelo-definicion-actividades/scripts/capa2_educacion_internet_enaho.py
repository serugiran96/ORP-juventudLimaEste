"""Usos de internet, estudios y motivos para no estudiar de jóvenes, con la ENAHO (Módulo 03), 2022-2025.

Uso (desde la carpeta del proyecto):
    python scripts/capa2_educacion_internet_enaho.py descargar  # -> data/raw/enaho/modulo03_{año}/
    python scripts/capa2_educacion_internet_enaho.py calcular   # -> data/processed/capa2_educacion_internet_enaho*.csv

Indicadores para jóvenes de 15-29 años (residentes habituales):
- Uso de internet el mes anterior, uso diario y propósitos de uso (entre quienes usan internet).
- Asistencia actual a educación básica o superior, nivel al que asisten y motivo principal de no
  estar matriculados o no asistir (p313, recodificada por el INEI en t313a).
Niveles: Lima Metropolitana, Lima Este (7 distritos, dominio no planificado: estimación propia) y
nacional, por año, y 2022-2025 agrupados para Lima Metropolitana y Lima Este.
Factor: factora07 (anual del módulo). Error estándar por linealización (conglome, estrato).
La réplica se valida con Dato Joven (uso de internet, 15-29, y asistencia universitaria, 17-24).
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from microdatos_inei import LIMA_ESTE, clasificar_precision, descargar, razon

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enaho"
PROCESADOS = RAIZ / "data" / "processed"
CODIGOS = {2022: 784, 2023: 906, 2024: 966, 2025: 1031}

PROPOSITOS = {1: "Obtener información", 2: "Comunicarse (correo, chat, redes)", 3: "Comprar productos o servicios",
              4: "Banca electrónica", 5: "Educación formal y capacitación", 6: "Trámites con el Estado",
              7: "Entretenimiento", 8: "Vender productos o servicios", 12: "Descargar aplicaciones o software"}
NIVELES = {3: "Secundaria", 4: "Superior no universitaria", 5: "Superior universitaria", 6: "Maestría/doctorado",
           2: "Primaria", 7: "Básica especial"}
MOTIVOS = {1: "Problemas económicos", 2: "Está trabajando", 3: "Terminó sus estudios o asiste a academia preuniversitaria",
           5: "Problemas familiares", 6: "De vacaciones", 8: "Asiste a un centro técnico-productivo (CETPRO)",
           9: "No le interesa o no le gusta estudiar", 10: "Se dedica a los quehaceres del hogar", 11: "Otra razón",
           12: "Asiste a un centro de enseñanza no regular", 17: "Institución no licenciada",
           18: "No le gustan o no aprende en clases virtuales"}


def descargar_todo():
    for anio, codigo in CODIGOS.items():
        archivos = descargar(codigo, "03", RAW / f"modulo03_{anio}", extensiones=(".dta", ".pdf"))
        print(f"  {anio}: {[a.name for a in archivos]}")


def _leer(anio):
    ruta = next((RAW / f"modulo03_{anio}").glob("*300.dta"))
    cols = ["conglome", "estrato", "ubigeo", "p204", "p205", "p206", "p207", "p208a", "factora07", "p306", "p307",
            "p308a", "t313a", "p314a", "p314d"] + [f"p316_{k}" for k in PROPOSITOS]
    df = pd.read_stata(ruta, columns=cols, convert_categoricals=False)
    for c in cols:
        if c not in ("conglome", "estrato", "ubigeo"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["ubigeo"] = df["ubigeo"].astype(str).str.zfill(6)
    df["conglome"] = f"{anio}_" + df["conglome"].astype(str)
    df["estrato"] = f"{anio}_" + df["estrato"].astype(str)
    residente = ((df.p204 == 1) & (df.p205 == 2)) | ((df.p204 == 2) & (df.p206 == 1))
    df = df[residente & df.factora07.notna()].copy()
    df["anio"] = anio
    return df


def _estimar(df, dominios, claves, edad_min=15, edad_max=29):
    arg = (df["factora07"], df["estrato"], df["conglome"])
    filas = []

    def agregar(dom, familia, categoria, num, den):
        valor, ee, n = razon(*arg, num, den, dominios[dom])
        filas.append({**claves[dom], "familia": familia, "categoria": categoria, "valor": valor, "ee": ee,
                      "n_muestral": n})

    todos = pd.Series(1.0, index=df.index)
    usa = df.p314a == 1
    con_dato_internet = df.p314a.notna()
    # Como Dato Joven, se usa la asistencia (p307), que solo se pregunta a los matriculados.
    asiste = (df.p306 == 1) & (df.p307 == 1)
    no_asiste = ((df.p306 == 2) | (df.p307 == 2)) & df.t313a.notna()
    for dom in dominios:
        agregar(dom, "internet", "Usó internet el mes anterior", usa, con_dato_internet)
        agregar(dom, "internet", "Usa internet al menos una vez al día (entre usuarios)", df.p314d == 1, usa)
        for k, nombre in PROPOSITOS.items():
            agregar(dom, "proposito_internet", nombre, df[f"p316_{k}"] == 1, usa & df[f"p316_{k}"].notna())
        agregar(dom, "educacion", "Asiste actualmente a educación básica o superior", asiste, df.p306.notna())
        for k, nombre in NIVELES.items():
            agregar(dom, "nivel_asistencia", nombre, asiste & (df.p308a == k), asiste & df.p308a.notna())
        for k, nombre in MOTIVOS.items():
            agregar(dom, "motivo_no_asistencia", nombre, no_asiste & (df.t313a == k), no_asiste)
    return filas


def calcular():
    datos = pd.concat([_leer(a) for a in CODIGOS], ignore_index=True)
    geos = {"lima_metropolitana": datos.ubigeo.str.startswith("1501"), "lima_este": datos.ubigeo.isin(LIMA_ESTE),
            "nacional": pd.Series(True, index=datos.index)}
    sexos = {"total": pd.Series(True, index=datos.index), "hombre": datos.p207 == 1, "mujer": datos.p207 == 2}
    grupos = {"15-29": datos.p208a.between(15, 29), "15-19": datos.p208a.between(15, 19),
              "20-24": datos.p208a.between(20, 24), "25-29": datos.p208a.between(25, 29)}
    dominios, claves = {}, {}
    for anio in list(CODIGOS) + ["2022-2025"]:
        m_anio = pd.Series(True, index=datos.index) if anio == "2022-2025" else datos.anio == anio
        for geo, m_geo in geos.items():
            if anio == "2022-2025" and geo == "nacional":
                continue
            for sexo, m_sexo in sexos.items():
                for grupo, m_grupo in grupos.items():
                    if grupo != "15-29" and sexo != "total":
                        continue
                    nombre = f"{anio}|{geo}|{sexo}|{grupo}"
                    dominios[nombre] = m_anio & m_geo & m_sexo & m_grupo
                    claves[nombre] = {"periodo": str(anio), "nivel_geografico": geo, "sexo": sexo, "grupo_edad": grupo}
    res = pd.DataFrame(_estimar(datos, dominios, claves))
    res["cv"] = 100 * res["ee"] / res["valor"]
    res.loc[res["valor"] == 0, "cv"] = np.nan
    res["precision"] = clasificar_precision(res["cv"])
    res.loc[(res["valor"] == 0) & (res["n_muestral"] >= 30), "precision"] = "confiable"
    res["valor_publicable"] = res["valor"].where(res["precision"] != "no_publicable")
    res["fuente"] = "ENAHO 2022-2025, Módulo 03 (INEI), cálculo propio"
    PROCESADOS.mkdir(parents=True, exist_ok=True)
    res.round(3).to_csv(PROCESADOS / "capa2_educacion_internet_enaho.csv", index=False)

    # Validación con Dato Joven: uso de internet (15-29) y asistencia universitaria (17-24).
    val = []
    for anio in CODIGOS:
        a = datos.anio == anio
        for geo in ["lima_metropolitana", "nacional"]:
            m = a & geos[geo]
            v, _, _ = razon(datos.factora07, datos.estrato, datos.conglome, datos.p314a == 1, datos.p314a.notna(),
                            m & grupos["15-29"])
            val.append({"anio": anio, "nivel_geografico": geo, "indicador": "USO DE INTERNET", "valor_enaho": v})
            # Asistencia universitaria: asisten a superior universitaria, entre los de 17-24 años
            v, _, _ = razon(datos.factora07, datos.estrato, datos.conglome,
                            (datos.p306 == 1) & (datos.p307 == 1) & (datos.p308a == 5),
                            datos.p306.notna(), m & datos.p208a.between(17, 24))
            val.append({"anio": anio, "nivel_geografico": geo, "indicador": "ASISTENCIA UNIVERSITARIA", "valor_enaho": v})
    val = pd.DataFrame(val)
    dj = pd.read_csv(PROCESADOS / "capa1_indicadores_encuestas.csv")
    dj = dj[(dj.desagregacion == "total") & dj.indicador.isin(val.indicador.unique()) & ~dj.sin_dato] \
        .rename(columns={"anio": "anio", "valor": "valor_dato_joven"})
    val = val.merge(dj[["anio", "nivel_geografico", "indicador", "valor_dato_joven"]],
                    on=["anio", "nivel_geografico", "indicador"], how="left")
    val["diferencia"] = val["valor_enaho"] - val["valor_dato_joven"]
    val.round(2).to_csv(PROCESADOS / "capa2_educacion_internet_enaho_validacion.csv", index=False)
    print(val.round(1).to_string(index=False))
    print(f"\n{len(res)} estimaciones -> capa2_educacion_internet_enaho.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[p.parse_args().paso]()
