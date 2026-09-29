"""Estimaciones nuevas de la ENAHO para la capa de Contexto del observatorio web, 2022-2025.

Uso (desde la carpeta del proyecto):
    python scripts/web_contexto_enaho.py descargar   # -> data/raw/enaho/modulo84_{año}/ (participación ciudadana)
    python scripts/web_contexto_enaho.py calcular    # -> data/processed/web_*_enaho.csv

Educación (Módulo 03), jóvenes de 15-29 años residentes habituales:
- Asistencia actual y nivel al que asisten, como porcentaje de TODOS los jóvenes del grupo (no solo de quienes
  estudian): universidad (p308a = 5), instituto o superior no universitaria (4), escolar (1-3, 7), posgrado (6).
- Nivel educativo alcanzado (p301a): sin secundaria completa, secundaria completa, superior técnica, superior
  universitaria o posgrado. "Sin educación superior" = hasta secundaria completa.
Participación en organizaciones (Módulo 84, capítulo 800, y Módulo 02):
- Porcentaje de jóvenes que pertenece a algún grupo, organización o asociación (800b, p803), por tipo, y el papel
  que cumplen (p804). El universo son los jóvenes de los hogares que respondieron el capítulo 800 (800a).
- Se valida con Dato Joven (participación en asociación u organización, 15-29, Lima Metropolitana, por año).

Lima Este = 7 distritos (dominio no planificado), 2022-2025 agrupados; Lima Metropolitana como referencia.
Factores: factora07 (educación) y facpob07 (participación). Error estándar por linealización (conglome, estrato).
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
FUENTE_EDU = "ENAHO 2022-2025, Módulo 03 (INEI), cálculo propio"
FUENTE_PART = "ENAHO 2022-2025, Módulos 02 y 84 (INEI), cálculo propio"

ASISTE = {"Universidad": [5], "Instituto (superior no universitaria)": [4], "Escolar": [1, 2, 3, 7],
          "Posgrado": [6]}
ALCANZADO = {"Sin secundaria completa": [1, 2, 3, 4, 5, 12], "Secundaria completa": [6],
             "Superior técnica (incompleta o completa)": [7, 8],
             "Superior universitaria o posgrado (incompleta o completa)": [9, 10, 11]}
TIPOS = {1: "Clubes y asociaciones deportivas", 2: "Agrupación o partido político", 3: "Clubes culturales",
         4: "Asociación vecinal", 7: "Asociación profesional", 8: "Asociación de trabajadores", 9: "Club de madres",
         10: "Asociación de padres de familia (APAFA)", 11: "Vaso de leche", 12: "Comedor popular",
         20: "Preparación de desayuno o almuerzo escolar", 18: "Otra organización"}
PAPEL = {1: "Dirigente o representante", 2: "Miembro activo", 3: "Miembro no activo", 4: "Otro"}
CLAVES = ["conglome", "vivienda", "hogar"]


def descargar_todo():
    for anio, codigo in CODIGOS.items():
        archivos = descargar(codigo, "84", RAW / f"modulo84_{anio}", extensiones=(".dta", ".pdf"))
        print(f"  {anio}: {[a.name for a in archivos]}")


def _residente(df):
    return ((df.p204 == 1) & (df.p205 == 2)) | ((df.p204 == 2) & (df.p206 == 1))


def _numericas(df, excepto):
    for c in df.columns:
        if c not in excepto:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _prefijar(df, anio):
    df["ubigeo"] = df["ubigeo"].astype(str).str.zfill(6)
    df["conglome"] = f"{anio}_" + df["conglome"].astype(str)
    df["estrato"] = f"{anio}_" + df["estrato"].astype(str)
    df["anio"] = anio
    return df


def _leer_educacion(anio):
    ruta = next((RAW / f"modulo03_{anio}").glob("*300.dta"))
    cols = ["conglome", "estrato", "ubigeo", "p204", "p205", "p206", "p207", "p208a", "factora07",
            "p301a", "p306", "p307", "p308a"]
    df = _numericas(pd.read_stata(ruta, columns=cols, convert_categoricals=False), ("conglome", "estrato", "ubigeo"))
    df = df[_residente(df) & df.factora07.notna()].copy()
    return _prefijar(df, anio)


def _leer_participacion(anio):
    """Una fila por joven de 15-29 residente en un hogar que respondió el capítulo 800."""
    carpeta = RAW / f"modulo84_{anio}"
    hogares = pd.read_stata(next(carpeta.glob("*800a.dta")), columns=CLAVES, convert_categoricals=False)
    orgs = pd.read_stata(next(carpeta.glob("*800b.dta")), columns=CLAVES + ["codperso", "p803", "p804"],
                         convert_categoricals=False)
    c2 = CLAVES + ["codperso", "ubigeo", "estrato", "p204", "p205", "p206", "p207", "p208a", "facpob07"]
    per = pd.read_stata(next((RAW / f"modulo02_{anio}").glob("*200.dta")), columns=c2, convert_categoricals=False)
    for df in (hogares, orgs, per):
        for c in CLAVES + (["codperso"] if "codperso" in df else []):
            df[c] = df[c].astype(str).str.strip()
    per = _numericas(per, CLAVES + ["codperso", "ubigeo", "estrato"])
    orgs["p803"] = pd.to_numeric(orgs.p803, errors="coerce")
    orgs["p804"] = pd.to_numeric(orgs.p804, errors="coerce")
    orgs = orgs[orgs.p803.notna() & (orgs.p803 != 19)]
    per = per[_residente(per) & per.facpob07.notna() & per.p208a.between(15, 29)]
    per = per.merge(hogares.drop_duplicates(), on=CLAVES, how="inner")
    llave = CLAVES + ["codperso"]
    per["participa"] = per.set_index(llave).index.isin(orgs.set_index(llave).index)
    for k in TIPOS:
        ids = orgs.loc[orgs.p803 == k, llave].drop_duplicates().set_index(llave).index
        per[f"tipo_{k}"] = per.set_index(llave).index.isin(ids)
    for k in PAPEL:
        ids = orgs.loc[orgs.p804 == k, llave].drop_duplicates().set_index(llave).index
        per[f"papel_{k}"] = per.set_index(llave).index.isin(ids)
    return _prefijar(per, anio)


def _dominios(df):
    geos = {"lima_este": df.ubigeo.isin(LIMA_ESTE), "lima_metropolitana": df.ubigeo.str.startswith("1501")}
    sexos = {"total": pd.Series(True, index=df.index), "mujer": df.p207 == 2, "hombre": df.p207 == 1}
    edades = {"15-29": df.p208a.between(15, 29), "15-19": df.p208a.between(15, 19),
              "20-24": df.p208a.between(20, 24), "25-29": df.p208a.between(25, 29)}
    for g, mg in geos.items():
        for s, ms in sexos.items():
            for e, me in edades.items():
                yield {"nivel_geografico": g, "sexo": s, "grupo_edad": e}, mg & ms & me


def _fila(clave, familia, categoria, universo, estimacion, fuente, periodo="2022-2025"):
    valor, ee, n = estimacion
    cv = 100 * ee / valor if valor else np.nan
    return {"familia": familia, "categoria": categoria, "universo": universo, **clave, "periodo": periodo,
            "valor": valor, "ee": ee, "n_muestral": n, "cv": cv, "fuente": fuente}


def _con_precision(filas):
    df = pd.DataFrame(filas)
    df.insert(df.columns.get_loc("cv") + 1, "precision", clasificar_precision(df.cv))
    return df


def calcular_educacion():
    d = pd.concat([_leer_educacion(a) for a in CODIGOS], ignore_index=True)
    arg = (d.factora07, d.estrato, d.conglome)
    asiste = (d.p306 == 1) & (d.p307 == 1)
    con_dato = d.p306.notna()
    con_nivel = d.p301a.notna()
    filas = []
    for clave, dom in _dominios(d):
        r = lambda num, den: razon(*arg, num, den, dom)
        filas.append(_fila(clave, "asistencia", "Estudia (cualquier nivel)", "jóvenes del grupo",
                           r(asiste, con_dato), FUENTE_EDU))
        for nombre, codigos in ASISTE.items():
            filas.append(_fila(clave, "asistencia", nombre, "jóvenes del grupo",
                               r(asiste & d.p308a.isin(codigos), con_dato), FUENTE_EDU))
        for nombre, codigos in ALCANZADO.items():
            filas.append(_fila(clave, "nivel_alcanzado", nombre, "jóvenes del grupo",
                               r(d.p301a.isin(codigos), con_nivel), FUENTE_EDU))
        filas.append(_fila(clave, "nivel_alcanzado", "Sin educación superior", "jóvenes del grupo",
                           r(d.p301a.isin(ALCANZADO["Sin secundaria completa"] + [6]), con_nivel), FUENTE_EDU))
        filas.append(_fila(clave, "nivel_alcanzado", "Superior completa", "jóvenes del grupo",
                           r(d.p301a.isin([8, 10, 11]), con_nivel), FUENTE_EDU))
    return _con_precision(filas)


def calcular_participacion():
    d = pd.concat([_leer_participacion(a) for a in CODIGOS], ignore_index=True)
    arg = (d.facpob07, d.estrato, d.conglome)
    todos = pd.Series(True, index=d.index)
    filas = []
    for clave, dom in _dominios(d):
        r = lambda num, den: razon(*arg, num, den, dom)
        filas.append(_fila(clave, "participacion", "Participa en algún grupo u organización", "jóvenes del grupo",
                           r(d.participa, todos), FUENTE_PART))
        for k, nombre in TIPOS.items():
            filas.append(_fila(clave, "tipo", nombre, "jóvenes del grupo", r(d[f"tipo_{k}"], todos), FUENTE_PART))
            filas.append(_fila(clave, "tipo_entre_participantes", nombre, "jóvenes que participan",
                               r(d[f"tipo_{k}"], d.participa), FUENTE_PART))
        for k, nombre in PAPEL.items():
            filas.append(_fila(clave, "papel", nombre, "jóvenes que participan",
                               r(d[f"papel_{k}"], d.participa), FUENTE_PART))
    # Validación con Dato Joven: Lima Metropolitana, 15-29, total, por año.
    dj = pd.read_csv(PROCESADOS / "capa1_indicadores_encuestas.csv")
    dj = dj[(dj.indicador == "PARTICIPACIÓN EN ASOCIACIÓN U ORGANIZACIÓN") & (dj.nivel_geografico == "lima_metropolitana")
            & (dj.desagregacion == "total")].set_index("anio").valor
    val = []
    lm = d.ubigeo.str.startswith("1501")
    for anio in CODIGOS:
        v, ee, n = razon(*arg, d.participa, todos, lm & (d.anio == anio))
        val.append({"anio": anio, "valor_enaho": round(v, 2), "ee": round(ee, 2), "valor_dato_joven": dj.get(anio),
                    "diferencia": round(v - dj[anio], 2) if anio in dj.index else np.nan, "n_muestral": n})
    return _con_precision(filas), pd.DataFrame(val)


def calcular():
    edu = calcular_educacion()
    edu.to_csv(PROCESADOS / "web_educacion_enaho.csv", index=False)
    part, val = calcular_participacion()
    part.to_csv(PROCESADOS / "web_participacion_enaho.csv", index=False)
    val.to_csv(PROCESADOS / "web_participacion_enaho_validacion.csv", index=False)
    print(f"web_educacion_enaho.csv: {len(edu)} filas; web_participacion_enaho.csv: {len(part)} filas")
    print("Validación con Dato Joven (participación, Lima Metropolitana, 15-29):")
    print(val.to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[ap.parse_args().accion]()
