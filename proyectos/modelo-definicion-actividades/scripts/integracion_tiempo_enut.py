"""Disponibilidad de tiempo de los jóvenes por día y franja horaria, con el diario de la ENUT 2024 (INEI).

Usa el mismo diario y la misma clasificación de actividades que capa2_uso_tiempo_enut.py (144 franjas de
10 minutos para un día de semana, un sábado y un domingo; hasta tres actividades simultáneas por franja).

Uso (desde la carpeta del proyecto; requiere los microdatos que descarga capa2_uso_tiempo_enut.py):
    python scripts/integracion_tiempo_enut.py   # -> data/processed/integracion_tiempo_enut.csv
                                                #    y data/processed/integracion_bases_enut.csv

Definiciones (decisión I2-D7 de fuentes/metodologia_integracion.md):
- Franja comprometida: tiene trabajo remunerado o búsqueda de trabajo, traslados, estudio, trabajo doméstico
  no remunerado, cuidado de otras personas del hogar o producción para autoconsumo, o la persona duerme.
- Disponible en un bloque horario: tiene al menos 2 horas seguidas (12 franjas) sin obligaciones ni sueño dentro
  del bloque, lo necesario para asistir a una actividad corta. Es disponibilidad observada en el día registrado,
  no preferencia: no dice si la persona iría a una actividad a esa hora ni cuánto tarda en llegar.
- Horas no comprometidas: horas del día sin obligaciones ni sueño (incluyen comer, aseo, descanso y ocio).
Lima Este = dominio no planificado (~230 jóvenes): solo el total de 15-29; se publica según el CV.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from capa2_uso_tiempo_enut import CLAVES, DIAS, RAW, _grupo, _horas_por_persona
from integracion_comun import Estimador, total
from microdatos_inei import LIMA_ESTE

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "processed" / "integracion_tiempo_enut.csv"
OBLIGACIONES = {"Trabajo remunerado y búsqueda de trabajo", "Traslados al trabajo", "Traslados al estudio", "Estudio",
                "Trabajo doméstico no remunerado", "Cuidado de otras personas del hogar",
                "Producción para autoconsumo"}
BLOQUES = {  # nombre: (día, hora de inicio, hora de fin)
    "Lunes a viernes, 14:00-18:00": ("DSEM", 14, 18),
    "Lunes a viernes, 18:00-22:00": ("DSEM", 18, 22),
    "Sábado, 09:00-13:00": ("SAB", 9, 13),
    "Sábado, 14:00-18:00": ("SAB", 14, 18),
    "Sábado, 18:00-22:00": ("SAB", 18, 22),
    "Domingo, 09:00-13:00": ("DOM", 9, 13),
    "Domingo, 14:00-18:00": ("DOM", 14, 18),
}
FRANJAS_MINIMAS = 12  # 2 horas seguidas
NOMBRE_DIA = {"DSEM": "Un día de lunes a viernes", "SAB": "Sábado", "DOM": "Domingo"}


def _franjas():
    """Una fila por persona y franja con: hora de inicio y, por día, si está comprometida."""
    act = [f"P600_{d}_ACT{i}" for d in DIAS for i in (1, 2, 3)]
    d6 = pd.read_stata(RAW / "V_ENUT2024_600.dta", columns=CLAVES + ["HORA_ID"] + act, convert_categoricals=False)
    codigos = pd.unique(d6[act].to_numpy().ravel())
    grupo = {c: _grupo(c) for c in codigos if pd.notna(c)}
    ocupa = {c: (g in OBLIGACIONES) or (g == "Dormir") for c, g in grupo.items()}
    # HORA_ID = "HH:MM - HH:MM"; el diario va de 01:00 a 01:00 del día siguiente ("24:50 - 01:00").
    d6["hora"] = d6["HORA_ID"].astype(str).str.slice(0, 2).astype(int)
    d6["orden"] = d6["hora"] * 60 + d6["HORA_ID"].astype(str).str.slice(3, 5).astype(int)
    for dia in DIAS:
        cols = [f"P600_{dia}_ACT{i}" for i in (1, 2, 3)]
        d6[f"comp_{dia}"] = np.column_stack([d6[c].map(ocupa).fillna(False).to_numpy(bool) for c in cols]).any(axis=1)
        d6[f"dato_{dia}"] = d6[cols].notna().any(axis=1)
    return d6[CLAVES + ["hora", "orden"] + [f"comp_{d}" for d in DIAS] + [f"dato_{d}" for d in DIAS]] \
        .sort_values(CLAVES + ["orden"])


def _racha_libre_maxima(b, dia):
    """Máximo de franjas seguidas sin obligaciones, por persona, dentro del bloque `b` (ya ordenado)."""
    libre = ~b[f"comp_{dia}"].to_numpy(bool)
    persona = b.groupby(CLAVES, sort=False).ngroup().to_numpy()
    corte = np.r_[True, (persona[1:] != persona[:-1]) | (libre[1:] != libre[:-1])]
    racha = np.cumsum(corte)
    largo = pd.Series(1, index=racha).groupby(level=0).transform("size").to_numpy()
    return pd.Series(np.where(libre, largo, 0), index=b.index).groupby([b[c] for c in CLAVES]).max()


def calcular():
    fr = _franjas()
    por_persona = []
    for nombre, (dia, h0, h1) in BLOQUES.items():
        b = fr[fr.hora.between(h0, h1 - 1)]
        dato = b.groupby(CLAVES)[f"dato_{dia}"].all()
        racha = _racha_libre_maxima(b, dia)
        por_persona.append(pd.Series((racha >= FRANJAS_MINIMAS) & dato, name=f"libre|{nombre}"))
        por_persona.append(pd.Series(dato, name=f"valido|{nombre}"))
    for dia in DIAS:
        g = fr.groupby(CLAVES).agg(comp=(f"comp_{dia}", "sum"), n=(f"dato_{dia}", "sum"))
        por_persona.append(pd.Series((g["n"] - g["comp"]) * 10 / 60, name=f"horas_libres|{dia}"))
        por_persona.append(pd.Series(g["n"] >= 140, name=f"dia_completo|{dia}"))
    # Como en la Capa 2, solo cuentan las personas con al menos una actividad registrada en el diario.
    con_diario = fr.groupby(CLAVES)[[f"dato_{d}" for d in DIAS]].any().any(axis=1)
    por_persona.append(pd.Series(con_diario, name="con_diario"))
    pp = pd.concat(por_persona, axis=1).reset_index()
    pp = pp[pp.con_diario.fillna(False).astype(bool)]

    per = pd.read_stata(RAW / "V_ENUT2024_200.dta", columns=CLAVES + ["P204", "P205_A", "CCDD", "CCPP", "CCDI", "AREA"],
                        convert_categoricals=False)
    fac = pd.read_stata(RAW / "V_ENUT2024_600.dta", columns=CLAVES + ["FACTORFINAL"], convert_categoricals=False) \
        .drop_duplicates(CLAVES)
    # Horas semanales de trabajo remunerado y estudio: para identificar a quienes no trabajaron ni estudiaron.
    act = [f"P600_{d}_ACT{i}" for d in DIAS for i in (1, 2, 3)]
    d6 = pd.read_stata(RAW / "V_ENUT2024_600.dta", columns=CLAVES + act, convert_categoricals=False)
    trabajo_estudio = {c for c in pd.unique(d6[act].to_numpy().ravel()) if pd.notna(c) and _grupo(c) in
                       {"Trabajo remunerado y búsqueda de trabajo", "Estudio"}}
    domestico = {c for c in pd.unique(d6[act].to_numpy().ravel()) if pd.notna(c) and _grupo(c) in
                 {"Trabajo doméstico no remunerado", "Cuidado de otras personas del hogar"}}
    d6["te"] = d6[act].isin(trabajo_estudio).any(axis=1)
    solo_domestico = {c for c in domestico if _grupo(c) == "Trabajo doméstico no remunerado"}
    horas_dom, horas_control = {}, {}
    for dia, peso in DIAS.items():
        cols = [f"P600_{dia}_ACT{i}" for i in (1, 2, 3)]
        claves = [d6[c] for c in CLAVES]
        horas_dom[dia] = d6[cols].isin(domestico).any(axis=1).groupby(claves).sum() * 10 / 60 * peso
        horas_control[dia] = d6[cols].isin(solo_domestico).any(axis=1).groupby(claves).sum() * 10 / 60 * peso
    te = d6.groupby(CLAVES)["te"].any().rename("trabajo_o_estudio")
    dom = (horas_dom["DSEM"] + horas_dom["SAB"] + horas_dom["DOM"]).rename("horas_domestico_cuidado")
    control = (horas_control["DSEM"] + horas_control["SAB"] + horas_control["DOM"]).rename("horas_control")
    df = pp.merge(per, on=CLAVES, how="left").merge(fac, on=CLAVES, how="left") \
        .merge(te.reset_index(), on=CLAVES, how="left").merge(dom.reset_index(), on=CLAVES, how="left") \
        .merge(control.reset_index(), on=CLAVES, how="left")
    # Participación semanal por grupo de actividades (misma función que la Capa 2), para estimar personas.
    PRACTICAS = ["Deporte y ejercicio físico", "Voluntariado y ayuda a la comunidad u otros hogares", "Leer",
                 "Aficiones, artes y juegos", "Asistir a eventos culturales, de entretenimiento o deportivos",
                 "Cuidado de otras personas del hogar"]
    horas = _horas_por_persona()[CLAVES + PRACTICAS]
    df = df.merge(horas, on=CLAVES, how="left")
    df["edad"] = pd.to_numeric(df["P205_A"], errors="coerce")
    df["ubigeo"] = df["CCDD"].astype(str).str.zfill(2) + df["CCPP"].astype(str).str.zfill(2) + \
        df["CCDI"].astype(str).str.zfill(2)
    df["estrato"] = df["CCDD"].astype(str) + "_" + df["AREA"].astype(str)
    df = df[df.FACTORFINAL.notna() & df.edad.notna()].copy()

    todos = pd.Series(True, index=df.index)
    lm, le = df.ubigeo.str.startswith("1501"), df.ubigeo.isin(LIMA_ESTE)
    j = df.edad.between(15, 29)
    sin_te = ~df.trabajo_o_estudio.fillna(False).astype(bool)
    dominios = {
        ("lima_metropolitana", "total", "15-29", "todos"): lm & j,
        ("lima_metropolitana", "hombre", "15-29", "todos"): lm & j & (df.P204 == 1),
        ("lima_metropolitana", "mujer", "15-29", "todos"): lm & j & (df.P204 == 2),
        ("lima_metropolitana", "total", "15-19", "todos"): lm & df.edad.between(15, 19),
        ("lima_metropolitana", "total", "20-24", "todos"): lm & df.edad.between(20, 24),
        ("lima_metropolitana", "total", "25-29", "todos"): lm & df.edad.between(25, 29),
        ("lima_metropolitana", "mujer", "15-29", "no trabajó ni estudió en la semana"): lm & j & (df.P204 == 2) & sin_te,
        ("lima_metropolitana", "mujer", "15-29", "trabajó o estudió en la semana"): lm & j & (df.P204 == 2) & ~sin_te,
        ("lima_este", "total", "15-29", "todos"): le & j,
    }
    est = Estimador(df.FACTORFINAL, df.estrato, df.CONG, "ENUT 2024 (INEI), cálculo propio")
    uno = pd.Series(1.0, index=df.index)
    for (geo, sexo, edad, grupo), dom in dominios.items():
        base = {"nivel_geografico": geo, "sexo": sexo, "grupo_edad": edad, "grupo": grupo, "periodo": "2024"}
        for nombre in BLOQUES:
            valido = df[f"valido|{nombre}"].fillna(False).astype(bool)
            est.proporcion({**base, "indicador": "disponible_en_bloque", "categoria": nombre, "unidad": "%"},
                           df[f"libre|{nombre}"].fillna(False).astype(bool) & valido, valido, dom, divisor_total=1)
        for dia in DIAS:
            completo = df[f"dia_completo|{dia}"].fillna(False).astype(bool)
            est.proporcion({**base, "indicador": "horas_no_comprometidas", "categoria": NOMBRE_DIA[dia],
                            "unidad": "horas"}, df[f"horas_libres|{dia}"].fillna(0) / 100, completo.astype(float),
                           dom & completo)
        for practica in PRACTICAS:
            est.proporcion({**base, "indicador": "participacion_semanal", "categoria": practica, "unidad": "%"},
                           df[practica].fillna(0) > 0, uno, dom, divisor_total=1)
        est.proporcion({**base, "indicador": "horas_domestico_cuidado", "categoria": "Semana",
                        "unidad": "horas"}, df.horas_domestico_cuidado.fillna(0) / 100, uno, dom)
        est.proporcion({**base, "indicador": "control_horas_domestico", "categoria": "Semana",
                        "unidad": "horas"}, df.horas_control.fillna(0) / 100, uno, dom)
    res = est.tabla()
    # razon() devuelve valor × 100; para horas se dividió el numerador entre 100 para recuperar la escala.

    # Control interno: las horas de trabajo doméstico deben coincidir con capa2_uso_tiempo_enut.csv.
    c2 = pd.read_csv(RAIZ / "data" / "processed" / "capa2_uso_tiempo_enut.csv")
    c2 = c2[(c2.familia == "horas_semanales_promedio") & (c2.categoria == "Trabajo doméstico no remunerado")
            & (c2.grupo_edad == "15-29")]
    for (geo, sexo), ref in c2.set_index(["nivel_geografico", "sexo"]).valor.items():
        propio = res[(res.indicador == "control_horas_domestico") & (res.nivel_geografico == geo) & (res.sexo == sexo)
                     & (res.grupo_edad == "15-29") & (res.grupo == "todos")].valor
        if len(propio):
            print(f"Control, trabajo doméstico, {geo} {sexo}: {propio.iloc[0]:.2f} h (Capa 2: {ref:.2f} h)")
    res = res[res.indicador != "control_horas_domestico"]
    res.round(3).to_csv(SALIDA, index=False)

    # Base de población según la expansión de la ENUT (jóvenes con diario, 2024).
    bases = []
    for geo, m_geo in {"lima_este": le, "lima_metropolitana": lm}.items():
        for sexo, m_s in {"total": todos, "hombre": df.P204 == 1, "mujer": df.P204 == 2}.items():
            t, ee = total(df.FACTORFINAL, df.estrato, df.CONG, uno, m_geo & j & m_s)
            bases.append({"fuente": "ENUT 2024 (expansión)", "nivel_geografico": geo, "grupo_edad": "15-29",
                          "sexo": sexo, "poblacion": t, "ee": ee})
    pd.DataFrame(bases).round(0).to_csv(RAIZ / "data" / "processed" / "integracion_bases_enut.csv", index=False)
    print(f"{len(res)} estimaciones -> {SALIDA.name}")


if __name__ == "__main__":
    calcular()
