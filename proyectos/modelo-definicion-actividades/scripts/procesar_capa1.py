"""Limpia y organiza los datos de Dato Joven extraídos para la Capa 1.

Entrada: data/raw/dato_joven/*.csv (generados por extraer_dato_joven.py)
Salida:  data/processed/capa1_*.csv (ver el diccionario en data/README.md)

Uso (desde la carpeta del proyecto):
    python scripts/procesar_capa1.py

Todas las tablas llevan la columna `nivel_geografico`, que separa la evidencia distrital
de Lima Este, la de Lima Metropolitana y la nacional. Nunca se mezclan niveles.
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "dato_joven"
PROCESADOS = RAIZ / "data" / "processed"

LIMA_ESTE = {
    "150103": "Ate",
    "150107": "Chaclacayo",
    "150111": "El Agustino",
    "150114": "La Molina",
    "150118": "Lurigancho-Chosica",
    "150132": "San Juan de Lurigancho",
    "150137": "Santa Anita",
}
PERIODO = range(2022, 2027)
UMBRAL_CV = 15.0  # en la fuente, los valores con CV > 15 van entre paréntesis (referenciales)

DIMENSIONES = {
    "educacion": "Educación",
    "empleo": "Empleo y situación laboral",
    "habilidades-digitales": "Internet y competencias digitales",
    "salud": "Salud",
    "participacion-ciudadana": "Participación ciudadana",
    "violencia-y-discriminacion": "Violencia y discriminación",
    "victimizacion": "Seguridad y victimización",
}
DIMENSION_TABLERO = {  # excepciones al mapeo por categoría del portal
    "Jóvenes que no estudian ni trabajan (NINI)": "No estudian ni trabajan",
}
DIMENSION_CONSOLIDADO = {
    "Victimizacion": "Seguridad y victimización",
    "Violencia": "Violencia y discriminación",
    "Participación": "Participación ciudadana",
}
FUENTES = {
    "ENCUESTA NACIONAL DE HOGARES": "ENAHO",
    "ENCUESTA PERMANENTE DE EMPLEO NACIONAL": "EPEN",
    "ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR": "ENDES",
    "ENCUESTA NACIONAL DE PROGRAMAS PRESUPUESTALES": "ENAPRES",
}
NIVELES = {"LIMA METROPOLITANA": "lima_metropolitana", "NACIONAL": "nacional"}


def guardar(df, nombre):
    PROCESADOS.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESADOS / f"{nombre}.csv", index=False)
    print(f"  {nombre}.csv: {len(df)} filas")


def distritos():
    d = pd.read_csv(RAW / "distritos_lima_metropolitana.csv", dtype=str)
    d["distrito"] = d["distrito"].str.title().str.replace(" De ", " de ").str.replace(" Del ", " del ")
    d.loc[d["ubigeo"].isin(LIMA_ESTE), "distrito"] = d["ubigeo"].map(LIMA_ESTE)
    d["lima_este"] = d["ubigeo"].isin(LIMA_ESTE)
    return d[["ubigeo", "distrito", "lima_este"]]


# --- población -------------------------------------------------------------------------

def poblacion():
    print("Población")
    dist = distritos()
    joven = pd.read_csv(RAW / "poblacion_joven_distritos_lima.csv", dtype={"UBIGEO": str})
    joven = joven.rename(columns={"UBIGEO": "ubigeo", "AÑO": "anio", "SEXO": "sexo", "RANGO DE EDAD": "grupo_edad",
                                  "suma(POBLACION JOVEN)": "poblacion"})
    joven["sexo"] = joven["sexo"].str.lower()
    joven = joven.merge(dist, on="ubigeo")
    joven["nivel_geografico"] = "distrito"
    guardar(joven[["nivel_geografico", "ubigeo", "distrito", "lima_este", "anio", "sexo", "grupo_edad", "poblacion"]]
            .sort_values(["ubigeo", "anio", "sexo", "grupo_edad"]), "capa1_poblacion_joven_distritos")

    total = pd.read_csv(RAW / "poblacion_total_distritos_lima.csv", dtype={"UBIGEO": str})
    total = total.rename(columns={"UBIGEO": "ubigeo", "AÑO": "anio", "SEXO": "sexo", "suma(POBLACION)": "poblacion"})
    total["anio"] = total["anio"].astype(int)

    # Resumen por distrito y año, más los agregados de Lima Este (suma de los 7 distritos)
    # y de Lima Metropolitana (suma de los 43).
    j = joven.pivot_table(index=["ubigeo", "anio"], columns="grupo_edad", values="poblacion", aggfunc="sum")
    j.columns = [f"joven_{c.replace(' a ', '_')}" for c in j.columns]
    j["joven_15_29"] = j.sum(axis=1)
    js = joven.pivot_table(index=["ubigeo", "anio"], columns="sexo", values="poblacion", aggfunc="sum")
    js.columns = [f"joven_{c}" for c in js.columns]
    t = total.groupby(["ubigeo", "anio"])["poblacion"].sum().rename("poblacion_total")
    res = j.join(js).join(t).reset_index().merge(dist, on="ubigeo")
    res["nivel_geografico"] = "distrito"

    def agregar(df, etiqueta, nivel):
        a = df.drop(columns=["ubigeo", "distrito", "lima_este", "nivel_geografico"]).groupby("anio").sum().reset_index()
        a["ubigeo"], a["distrito"], a["lima_este"], a["nivel_geografico"] = "", etiqueta, False, nivel
        return a

    res = pd.concat([res,
                     agregar(res[res["lima_este"]], "Lima Este (7 distritos)", "lima_este_agregado"),
                     agregar(res, "Lima Metropolitana (43 distritos)", "lima_metropolitana")], ignore_index=True)

    nj = pd.read_csv(RAW / "poblacion_joven_nacional.csv")
    nt = pd.read_csv(RAW / "poblacion_total_nacional.csv")
    nac = (nj.pivot_table(index="AÑO", columns="RANGO DE EDAD", values="suma(POBLACION JOVEN)", aggfunc="sum"))
    nac.columns = [f"joven_{c.replace(' a ', '_')}" for c in nac.columns]
    nac["joven_15_29"] = nac.sum(axis=1)
    nacs = nj.pivot_table(index="AÑO", columns="SEXO", values="suma(POBLACION JOVEN)", aggfunc="sum")
    nacs.columns = [f"joven_{c.lower()}" for c in nacs.columns]
    nac = nac.join(nacs).join(nt.groupby("AÑO")["suma(POBLACION)"].sum().rename("poblacion_total"))
    nac = nac.reset_index().rename(columns={"AÑO": "anio"})
    nac["anio"] = nac["anio"].astype(int)
    nac["ubigeo"], nac["distrito"], nac["lima_este"], nac["nivel_geografico"] = "", "Perú", False, "nacional"
    res = pd.concat([res, nac], ignore_index=True)

    res["pct_joven"] = 100 * res["joven_15_29"] / res["poblacion_total"]
    res["pct_mujer_joven"] = 100 * res["joven_mujer"] / res["joven_15_29"]
    cols = ["nivel_geografico", "ubigeo", "distrito", "lima_este", "anio", "joven_15_29", "joven_15_19",
            "joven_20_24", "joven_25_29", "joven_hombre", "joven_mujer", "poblacion_total", "pct_joven",
            "pct_mujer_joven"]
    guardar(res[cols].sort_values(["nivel_geografico", "ubigeo", "anio"]), "capa1_poblacion_resumen")
    return res


# --- encuestas -------------------------------------------------------------------------

def _valor(texto):
    """'12.5%' -> 12.5; '(3.1%)' -> 3.1 (referencial); '(¬)' -> sin dato."""
    if pd.isna(texto) or "¬" in str(texto):
        return None
    return float(str(texto).strip("()%"))


def _unidad(tablero, texto):
    if isinstance(texto, str) and "%" in texto:
        return "%"
    if tablero.startswith("Años promedio"):
        return "años"
    if tablero.startswith("Ingreso"):
        return "soles"
    return ""


def _limpiar_encuestas(df, origen):
    df = df.copy()
    df["anio"] = df["AÑO"].astype(int)
    df["valor"] = df["VALOR"].map(_valor)
    df["cv"] = pd.to_numeric(df["CV"], errors="coerce")
    df["referencial"] = df["cv"] > UMBRAL_CV
    df["sin_dato"] = df["valor"].isna()
    df["fuente"] = df["FUENTE"].str.strip().str.upper().replace(FUENTES)
    df["poblacion"] = df["POBLACION"].str.replace("AÑOS", "", regex=False).str.strip()
    df["nivel_geografico"] = df["REGION"].map(NIVELES)
    df["desagregacion"] = df["CATEGORIA"].str.lower().replace({"regional": "total", "nacional": "total"})
    df["origen"] = origen
    return df


def encuestas():
    print("Indicadores de encuestas")
    ind = pd.read_csv(RAW / "encuestas_regionales.csv", dtype=str)
    ind = _limpiar_encuestas(ind, "tablero_individual")
    ind["dimension"] = ind["tablero"].map(DIMENSION_TABLERO).fillna(ind["categoria_portal"].map(DIMENSIONES))
    ind["unidad"] = [_unidad(t, v) for t, v in zip(ind["tablero"], ind["VALOR"])]

    # Filas ambiguas: la fuente repite una misma etiqueta con valores distintos
    # (p. ej., tres filas "CELULAR SIN PLAN DE DATOS" el mismo año). Se excluyen.
    clave = ["tablero", "anio", "REGION", "CATEGORIA", "INDICADOR"]
    ambiguas = ind.duplicated(clave, keep=False)
    ind["excluida_por_etiqueta_ambigua"] = ambiguas

    # Tablas del consolidado que no están en los tableros individuales.
    con = pd.read_csv(RAW / "consolidado_regionales.csv", dtype=str)
    con = _limpiar_encuestas(con, "consolidado")
    nuevas = con[~con["INDICADOR"].isin(set(ind["INDICADOR"]))].copy()
    nuevas["tablero"] = nuevas["tabla"]
    nuevas["dimension"] = nuevas["tabla"].str.extract(r"^fact([A-Za-zÁÉÍÓÚáéíóú]+)")[0].map(
        lambda s: next((v for k, v in DIMENSION_CONSOLIDADO.items() if s.startswith(k)), None))
    nuevas["unidad"] = [_unidad(t, v) for t, v in zip(nuevas["tablero"], nuevas["VALOR"])]
    nuevas["excluida_por_etiqueta_ambigua"] = False

    cols = ["dimension", "tablero", "INDICADOR", "fuente", "poblacion", "nivel_geografico", "desagregacion",
            "anio", "valor", "unidad", "cv", "referencial", "sin_dato", "origen", "excluida_por_etiqueta_ambigua"]
    out = pd.concat([ind[cols], nuevas[cols]], ignore_index=True).rename(columns={"INDICADOR": "indicador"})
    out["en_periodo_prioritario"] = out["anio"].isin(PERIODO)
    guardar(out.sort_values(["dimension", "tablero", "indicador", "nivel_geografico", "desagregacion", "anio"]),
            "capa1_indicadores_encuestas")

    # Control de coherencia entre tableros individuales y consolidado.
    comunes = con[con["INDICADOR"].isin(set(ind["INDICADOR"]))]
    m = comunes.merge(ind[~ambiguas], on=["INDICADOR", "REGION", "CATEGORIA", "AÑO"], suffixes=("_con", "_ind"))
    difieren = m[(m["valor_con"] - m["valor_ind"]).abs() > 0.05]
    print(f"  coherencia consolidado vs. tableros: {len(m)} valores comunes, {len(difieren)} distintos")
    guardar(difieren[["INDICADOR", "REGION", "CATEGORIA", "AÑO", "valor_ind", "valor_con"]],
            "control_consolidado_vs_tableros")

    nac = pd.read_csv(RAW / "encuestas_nacionales.csv", dtype=str)
    nac = _limpiar_encuestas(nac, "tablero_individual")
    nac["dimension"] = nac["tablero"].map(DIMENSION_TABLERO).fillna(nac["categoria_portal"].map(DIMENSIONES))
    nac["unidad"] = [_unidad(t, v) for t, v in zip(nac["tablero"], nac["VALOR"])]
    nac["nivel_geografico"] = "nacional"
    nac["excluida_por_etiqueta_ambigua"] = nac.duplicated(["tablero", "anio", "CATEGORIA", "INDICADOR"], keep=False)
    nac = nac[cols].rename(columns={"INDICADOR": "indicador"})
    guardar(nac.sort_values(["dimension", "tablero", "indicador", "desagregacion", "anio"]),
            "capa1_indicadores_encuestas_desagregacion_nacional")


# --- RENOJ y voluntariado --------------------------------------------------------------

def renoj(pob):
    print("RENOJ")
    dist = distritos()
    r = pd.read_csv(RAW / "renoj_organizaciones_distritos_lima.csv", dtype={"UBIGEO": str})
    r = r.rename(columns={"UBIGEO": "ubigeo", "AÑO ACREDITACIÓN": "anio_acreditacion",
                          "TIPO DE ORGANIZACIÓN": "tipo", "DETALLE TIPO DE ORGANIZACIÓN": "detalle_tipo",
                          "TEMÁTICA DE ORGANIZACIÓN": "tematica", "Temática de organización 1": "tematica_1",
                          "Temática de organización 2": "tematica_2", "Total de Organizaciones": "organizaciones"})
    r = r.merge(dist, on="ubigeo")
    r["nivel_geografico"] = "distrito"
    guardar(r[["nivel_geografico", "ubigeo", "distrito", "lima_este", "anio_acreditacion", "tipo", "detalle_tipo",
               "tematica", "tematica_1", "tematica_2", "organizaciones"]], "capa1_renoj_organizaciones")

    tot = r.groupby("ubigeo")["organizaciones"].sum().rename("organizaciones_acumuladas")
    rec = r[r["anio_acreditacion"].isin(PERIODO)].groupby("ubigeo")["organizaciones"].sum().rename(
        "acreditadas_2022_2026")
    p = pob[(pob["nivel_geografico"] == "distrito") & (pob["anio"] == 2026)].set_index("ubigeo")["joven_15_29"]
    res = dist.set_index("ubigeo").join(tot).join(rec).join(p).fillna({"organizaciones_acumuladas": 0,
                                                                         "acreditadas_2022_2026": 0})
    res["organizaciones_por_10mil_jovenes"] = 1e4 * res["organizaciones_acumuladas"] / res["joven_15_29"]
    res = res.reset_index()
    res["nivel_geografico"] = "distrito"
    guardar(res, "capa1_renoj_resumen_distritos")


def voluntariado(pob):
    print("Voluntariado")
    dist = distritos()
    v = pd.read_csv(RAW / "voluntariado_distritos_lima.csv", dtype={"UBIGEO": str})
    v = v.rename(columns={"UBIGEO": "ubigeo", "Total Voluntarios": "personas"}).merge(dist, on="ubigeo")
    total = v[v["variable"] == "TOTAL"].set_index("ubigeo")["personas"]
    v = v[v["variable"] != "TOTAL"].copy()
    v["valor"] = v["valor"].astype(str).str.strip()
    v["pct_del_distrito"] = 100 * v["personas"] / v["ubigeo"].map(total)
    v["nivel_geografico"] = "distrito"
    guardar(v[["nivel_geografico", "ubigeo", "distrito", "lima_este", "variable", "valor", "personas",
               "pct_del_distrito"]], "capa1_voluntariado_distritos")

    p = pob[(pob["nivel_geografico"] == "distrito") & (pob["anio"] == 2026)].set_index("ubigeo")["joven_15_29"]
    res = dist.set_index("ubigeo").join(total.rename("personas_inscritas")).join(p)
    res["personas_inscritas"] = res["personas_inscritas"].fillna(0)
    res["inscritas_por_10mil_jovenes"] = 1e4 * res["personas_inscritas"] / res["joven_15_29"]
    res = res.reset_index()
    res["nivel_geografico"] = "distrito"
    guardar(res, "capa1_voluntariado_resumen_distritos")


# --- registros sensibles ---------------------------------------------------------------

UMBRAL_CELDA = 10  # decisión del equipo: ocultar conteos menores de 10
PERIODO_PROMEDIO = range(2022, 2026)  # años completos en los cuatro registros

REGISTROS = {
    # nombre: (archivo, columna de año, columna de conteo, desagregaciones, denominador)
    "maternidad_adolescente": ("cnv_madres_15_19_distritos_lima.csv", "anio", "Total nacidos vivos",
                               ["rango_edad"], "mujeres_15_19"),
    "violencia_atendida_cem": ("cem_casos_edad_sexo_distritos_lima.csv", "anio", "Total de Casos",
                               ["grupo_edad_victima", "sexo_victima"], "jovenes_15_29"),
    "violencia_cem_por_tipo": ("cem_casos_tipo_violencia_distritos_lima.csv", "anio", "Total de Casos",
                               ["tipo_violencia"], None),
    "discapacidad_certificados": ("discapacidad_certificados_distritos_lima.csv", "anio_emision", "Total Casos",
                                  ["grupo_edad", "sexo"], "jovenes_15_29"),
    "discapacidad_conadis": ("conadis_inscritos_distritos_lima.csv", "anio_inscripcion",
                             "Total jóvenes registrados", ["rango_edad", "sexo"], "jovenes_15_29"),
}
PARCIALES = {"maternidad_adolescente": {2026: "enero–junio"}, "discapacidad_conadis": {2026: "año en curso"}}


def ocultar(df, valor, grupos=None):
    """Oculta conteos < UMBRAL_CELDA. Si se pasan `grupos`, aplica ocultación complementaria:
    en cada grupo cuyo total se publica, si queda exactamente una celda oculta, oculta también la
    siguiente más pequeña para que no pueda deducirse restando del total."""
    df = df.copy()
    df["oculto"] = df[valor] < UMBRAL_CELDA
    if grupos:
        for _, sub in df.groupby(grupos):
            if sub["oculto"].sum() == 1 and (~sub["oculto"]).sum() >= 1:
                df.loc[sub[~sub["oculto"]][valor].idxmin(), "oculto"] = True
    df[valor] = df[valor].where(~df["oculto"])
    return df


def sensibles(pob):
    print("Registros sensibles (con ocultación de celdas < 10)")
    dist = distritos()
    pj = pd.read_csv(PROCESADOS / "capa1_poblacion_joven_distritos.csv", dtype={"ubigeo": str})
    p26 = pj[pj["anio"] == 2026]
    denominadores = {
        "mujeres_15_19": p26[(p26.sexo == "mujer") & (p26.grupo_edad == "15 a 19")].set_index("ubigeo")["poblacion"],
        "jovenes_15_29": p26.groupby("ubigeo")["poblacion"].sum(),
    }
    por_anio, desagregado, resumen = [], [], []
    for registro, (archivo, col_anio, col_n, variables, denom) in REGISTROS.items():
        d = pd.read_csv(RAW / archivo, dtype={"ubigeo": str})
        d = d.rename(columns={col_anio: "anio", col_n: "casos"})
        d["anio"] = d["anio"].astype(int)

        # 1) Totales por distrito y año (43 distritos) y agregado de Lima Este.
        if registro != "violencia_cem_por_tipo":
            t = d.groupby(["ubigeo", "anio"])["casos"].sum().reset_index().merge(dist, on="ubigeo")
            t["nivel_geografico"] = "distrito"
            le = t[t.lima_este].groupby("anio")["casos"].sum().reset_index()
            le["ubigeo"], le["distrito"], le["lima_este"], le["nivel_geografico"] = "", "Lima Este (7 distritos)", \
                False, "lima_este_agregado"
            t = pd.concat([t, le], ignore_index=True)
            # Ocultación complementaria entre los 7 distritos y su agregado, año por año.
            t["grupo"] = t["anio"].astype(str) + "_" + (t.lima_este | (t.nivel_geografico == "lima_este_agregado")).astype(str)
            t = ocultar(t, "casos", ["grupo"]).drop(columns="grupo")
            t["registro"] = registro
            t["periodo_parcial"] = t["anio"].map(PARCIALES.get(registro, {})).fillna("")
            por_anio.append(t)

        # 2) Desagregaciones por distrito, periodo 2022-2025 sumado.
        dp = d[d["anio"].isin(PERIODO_PROMEDIO)]
        dp_le = dp[dp["ubigeo"].isin(LIMA_ESTE)].assign(ubigeo="LIMA_ESTE")
        for v in variables:
            g = pd.concat([dp, dp_le]).groupby(["ubigeo", v])["casos"].sum().reset_index() \
                .rename(columns={v: "categoria"})
            g["variable"] = v
            total = pd.concat([dp, dp_le]).groupby("ubigeo")["casos"].sum()
            g = ocultar(g, "casos", ["ubigeo"])
            g = g.merge(pd.concat([dist, pd.DataFrame([{"ubigeo": "LIMA_ESTE", "distrito": "Lima Este (7 distritos)",
                                                         "lima_este": False}])]), on="ubigeo")
            g["pct_del_distrito"] = 100 * g["casos"] / g["ubigeo"].map(total)
            g["registro"], g["periodo"] = registro, "2022–2025"
            desagregado.append(g)

        # 3) Promedio anual 2022-2025 y tasa con población 2026 (ver D5).
        if denom:
            s = dp.groupby("ubigeo")["casos"].sum().rename("casos_2022_2025").reset_index().merge(dist, on="ubigeo")
            s["promedio_anual"] = s["casos_2022_2025"] / len(PERIODO_PROMEDIO)
            s["denominador"] = denom
            s["poblacion_2026"] = s["ubigeo"].map(denominadores[denom])
            factor = 1000 if denom == "mujeres_15_19" else 10000
            s["tasa"] = factor * s["promedio_anual"] / s["poblacion_2026"]
            s["tasa_por"] = "1 000 mujeres de 15–19" if factor == 1000 else "10 000 jóvenes de 15–29"
            oculto = s["casos_2022_2025"] < UMBRAL_CELDA
            s.loc[oculto, ["casos_2022_2025", "promedio_anual", "tasa"]] = float("nan")
            s["oculto"] = oculto
            s["mediana_lima_metropolitana"] = s["tasa"].median()
            s["registro"] = registro
            resumen.append(s)

    cols_a = ["registro", "nivel_geografico", "ubigeo", "distrito", "lima_este", "anio", "casos", "oculto",
              "periodo_parcial"]
    guardar(pd.concat(por_anio, ignore_index=True)[cols_a], "capa1_registros_distrito_anio")
    cols_d = ["registro", "periodo", "ubigeo", "distrito", "lima_este", "variable", "categoria", "casos",
              "oculto", "pct_del_distrito"]
    guardar(pd.concat(desagregado, ignore_index=True)[cols_d], "capa1_registros_distrito_desagregado")
    cols_r = ["registro", "ubigeo", "distrito", "lima_este", "casos_2022_2025", "promedio_anual", "denominador",
              "poblacion_2026", "tasa", "tasa_por", "mediana_lima_metropolitana", "oculto"]
    guardar(pd.concat(resumen, ignore_index=True)[cols_r], "capa1_registros_resumen")


def main():
    pob = poblacion()
    encuestas()
    renoj(pob)
    voluntariado(pob)
    sensibles(pob)


if __name__ == "__main__":
    main()
