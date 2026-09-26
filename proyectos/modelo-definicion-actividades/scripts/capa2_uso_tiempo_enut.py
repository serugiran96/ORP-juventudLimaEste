"""Uso del tiempo de jóvenes con microdatos de la ENUT 2024 (INEI).

La ENUT 2024 registra, para cada persona de 12 años o más, un diario de 144 franjas de 10 minutos
para un día de semana, un sábado y un domingo, con hasta tres actividades simultáneas por franja
(capítulo 600). También pregunta por la satisfacción con el tiempo libre (capítulo 800).

Uso (desde la carpeta del proyecto):
    python scripts/capa2_uso_tiempo_enut.py descargar  # -> data/raw/enut/2024/
    python scripts/capa2_uso_tiempo_enut.py calcular   # -> data/processed/capa2_uso_tiempo_enut.csv

Cálculo:
- Horas semanales por grupo de actividades = 5 × (día de semana) + sábado + domingo. Una franja cuenta
  para una actividad si esta aparece en cualquiera de sus tres registros simultáneos, así que la suma
  de todos los grupos puede superar las 168 horas.
- Indicadores: % de personas que realizó la actividad en la semana, promedio de horas semanales de toda
  la población y promedio entre quienes la realizaron.
- Jóvenes de 15-29 años (y adultos de 30+ como contraste). Lima Metropolitana, Lima Este (7 distritos,
  dominio no planificado: estimación propia) y nacional. Un solo año: 2024.
- Error estándar por linealización. Conglomerado = CONG; estrato aproximado = departamento × área
  (la base no trae el estrato de diseño; es una aproximación conservadora).
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from microdatos_inei import LIMA_ESTE, clasificar_precision, descargar, razon

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enut" / "2024"
SALIDA = RAIZ / "data" / "processed" / "capa2_uso_tiempo_enut.csv"
CODIGO, MODULOS = 963, ["1850", "1854", "1855"]
CLAVES = ["CONG", "NSELV", "HOGAR", "P201"]
DIAS = {"DSEM": 5, "SAB": 1, "DOM": 1}  # peso de cada día en la semana


def _grupo(codigo):
    """Clasifica un código de actividad de la ENUT en un grupo analítico."""
    c = int(codigo)
    if c in (10, 12, 13) or 111 <= c <= 114:
        return "Trabajo remunerado y búsqueda de trabajo"
    if c == 14:
        return "Traslados al trabajo"
    if c == 62:
        return "Traslados al estudio"
    if 610 <= c <= 614:
        return "Estudio"
    if 300 <= c <= 372:
        return "Trabajo doméstico no remunerado"
    if 410 <= c <= 440 or 4000 <= c <= 4999:
        return "Cuidado de otras personas del hogar"
    if 210 <= c <= 232:
        return "Producción para autoconsumo"
    if 510 <= c <= 532:
        return "Voluntariado y ayuda a la comunidad u otros hogares"
    if 710 <= c <= 712:
        return "Convivencia con familia y amigos"
    if 720 <= c <= 723:
        return "Asistir a eventos culturales, de entretenimiento o deportivos"
    if 730 <= c <= 732:
        return "Aficiones, artes y juegos"
    if 740 <= c <= 742:
        return "Deporte y ejercicio físico"
    return {81: "Leer", 82: "Ver televisión o videos", 83: "Escuchar radio o audio",
            84: "Usar computadora, tablet o celular (internet, redes, juegos)",
            921: "Comer y beber", 922: "Dormir"}.get(c, "Cuidado personal, descanso y otras actividades personales")


def descargar_todo():
    for m in MODULOS:
        print(f"  {m}: {[a.name for a in descargar(CODIGO, m, RAW)]}")


def _horas_por_persona():
    act = [f"P600_{d}_ACT{i}" for d in DIAS for i in (1, 2, 3)]
    d6 = pd.read_stata(RAW / "V_ENUT2024_600.dta", columns=CLAVES + ["HORA_ID"] + act, convert_categoricals=False)
    codigos = pd.unique(d6[act].to_numpy().ravel())
    mapa = {c: _grupo(c) for c in codigos if pd.notna(c)}
    for col in act:
        d6[col] = d6[col].map(mapa)
    partes = []
    for dia, peso in DIAS.items():
        cols = [f"P600_{dia}_ACT{i}" for i in (1, 2, 3)]
        largo = d6[CLAVES + cols].melt(id_vars=CLAVES, value_name="grupo").dropna(subset=["grupo"])
        # Una franja cuenta una sola vez por grupo, aunque el grupo aparezca en dos registros simultáneos.
        largo["franja"] = largo.index % len(d6)
        largo = largo.drop_duplicates(CLAVES + ["franja", "grupo"])
        m = largo.groupby(CLAVES + ["grupo"]).size().rename("franjas").reset_index()
        m["horas_semana"] = m["franjas"] * 10 / 60 * peso
        partes.append(m)
    horas = pd.concat(partes).groupby(CLAVES + ["grupo"])["horas_semana"].sum().unstack(fill_value=0.0)
    return horas.reset_index()


def calcular():
    per = pd.read_stata(RAW / "V_ENUT2024_200.dta", columns=CLAVES + ["P204", "P205_A", "CCDD", "CCPP", "CCDI", "AREA"],
                        convert_categoricals=False)
    horas = _horas_por_persona()
    grupos = [c for c in horas.columns if c not in CLAVES]
    fac = pd.read_stata(RAW / "V_ENUT2024_600.dta", columns=CLAVES + ["FACTORFINAL"], convert_categoricals=False) \
        .drop_duplicates(CLAVES)
    df = horas.merge(per, on=CLAVES, how="left").merge(fac, on=CLAVES, how="left")
    sat = pd.read_stata(RAW / "V_ENUT2024_700_800_900.dta", columns=CLAVES + ["P801_5", "P802_1", "P803_1", "P803_2"],
                        convert_categoricals=False)
    df = df.merge(sat, on=CLAVES, how="left")
    df["edad"] = pd.to_numeric(df["P205_A"], errors="coerce")
    df["ubigeo"] = df["CCDD"].astype(str).str.zfill(2) + df["CCPP"].astype(str).str.zfill(2) + \
        df["CCDI"].astype(str).str.zfill(2)
    df["estrato"] = df["CCDD"].astype(str) + "_" + df["AREA"].astype(str)
    df = df[df["FACTORFINAL"].notna() & df["edad"].notna()].copy()
    print(f"  personas con diario: {len(df)}")

    todos = pd.Series(True, index=df.index)
    geos = {"lima_metropolitana": df.ubigeo.str.startswith("1501"), "lima_este": df.ubigeo.isin(LIMA_ESTE),
            "nacional": todos}
    sexos = {"total": todos, "hombre": df.P204 == 1, "mujer": df.P204 == 2}
    edades = {"15-29": df.edad.between(15, 29), "30+": df.edad >= 30, "15-19": df.edad.between(15, 19),
              "20-24": df.edad.between(20, 24), "25-29": df.edad.between(25, 29)}
    arg = (df["FACTORFINAL"], df["estrato"], df["CONG"])
    uno = pd.Series(1.0, index=df.index)
    filas = []
    for geo, m_geo in geos.items():
        for sexo, m_sexo in sexos.items():
            for edad, m_edad in edades.items():
                if (edad != "15-29" and sexo != "total") or (geo == "lima_este" and (sexo != "total" or edad == "30+")):
                    continue
                dom = m_geo & m_sexo & m_edad
                base = {"periodo": "2024", "nivel_geografico": geo, "sexo": sexo, "grupo_edad": edad}
                for g in grupos:
                    hace = (df[g] > 0).astype(float)
                    v, ee, n = razon(*arg, hace, uno, dom)
                    filas.append({**base, "familia": "participacion_semanal", "categoria": g, "valor": v, "ee": ee,
                                  "unidad": "%", "n_muestral": n})
                    v, ee, n = razon(*arg, df[g], uno, dom)
                    filas.append({**base, "familia": "horas_semanales_promedio", "categoria": g, "valor": v / 100,
                                  "ee": ee / 100, "unidad": "horas", "n_muestral": n})
                    v, ee, n = razon(*arg, df[g], hace, dom)
                    filas.append({**base, "familia": "horas_semanales_entre_participantes", "categoria": g,
                                  "valor": v / 100, "ee": ee / 100, "unidad": "horas", "n_muestral": n})
                for var, nombre in [("P803_1", "Cantidad de tiempo libre"), ("P803_2", "Calidad del tiempo libre"),
                                    ("P802_1", "Tiempo dedicado a pasatiempos"),
                                    ("P801_5", "Tiempo dedicado a sus amistades")]:
                    valido = df[var].between(1, 5)
                    v, ee, n = razon(*arg, df[var].isin([4, 5]), valido, dom)
                    filas.append({**base, "familia": "satisfaccion_muy_o_totalmente_satisfecho", "categoria": nombre,
                                  "valor": v, "ee": ee, "unidad": "%", "n_muestral": n})
                    v, ee, n = razon(*arg, df[var].isin([1, 2]), valido, dom)
                    filas.append({**base, "familia": "satisfaccion_nada_o_poco_satisfecho", "categoria": nombre,
                                  "valor": v, "ee": ee, "unidad": "%", "n_muestral": n})

    res = pd.DataFrame(filas)
    res["cv"] = 100 * res["ee"] / res["valor"]
    res.loc[res["valor"] == 0, "cv"] = np.nan
    res["precision"] = clasificar_precision(res["cv"])
    res["valor_publicable"] = res["valor"].where(res["precision"] != "no_publicable")
    res["fuente"] = "ENUT 2024 (INEI), cálculo propio"
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    res.round(3).to_csv(SALIDA, index=False)

    # Validación con el informe del INEI: mujeres de 12-19 años dedican 42,2 horas semanales al estudio
    # (entre quienes estudian); hombres de 12-19, 40,5 horas.
    # El INEI incluye los traslados al centro de estudios en el tiempo de estudio.
    estudio = df["Estudio"] + df["Traslados al estudio"]
    for sexo, cod, publicado in [("mujeres", 2, 42.2), ("hombres", 1, 40.5)]:
        dom = df.edad.between(12, 19) & (df.P204 == cod)
        v, _, _ = razon(*arg, estudio, (estudio > 0).astype(float), dom)
        print(f"  Validación, {sexo} 12-19, horas de estudio (con traslados) entre quienes estudian: "
              f"{v / 100:.1f} (INEI: {publicado})")
    print(f"  {len(res)} estimaciones -> {SALIDA.name}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[p.parse_args().paso]()
