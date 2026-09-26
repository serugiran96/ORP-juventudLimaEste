"""Inseguridad y actividades evitadas por temor a la delincuencia, con la ENAPRES 2022-2025 (INEI).

El capítulo de seguridad ciudadana (600 en 2022-2024; 400 en 2025) se aplica a personas de 14 años o más en
el área urbana. De él se usan dos preguntas que afectan la posibilidad real de participar en actividades:
- "¿Qué tan seguro/a se siente caminando solo/a en su zona o barrio de noche?" (muy inseguro o inseguro).
- "¿Dejó o evitó ..., en los últimos 12 meses, por temor a ser víctima de la delincuencia?": salir de noche,
  llegar muy tarde a casa y cualquiera de las actividades de la lista.

Uso (desde la carpeta del proyecto):
    python scripts/integracion_seguridad_enapres.py descargar  # -> data/raw/enapres/{año}_cap600|cap400/
    python scripts/integracion_seguridad_enapres.py calcular   # -> data/processed/integracion_seguridad_enapres*.csv

Validación: la réplica de Lima Metropolitana se compara con Dato Joven (fuente: ENAPRES), tolerancia ±1 punto.
- Inseguridad de noche: 2022-2025, total y por sexo.
- Dejó alguna actividad: 2022-2024, total. En 2025 la lista cambió (se agregó "usar internet fuera de casa") y
  el valor salta de ~33 % a ~63 %: 2025 no es comparable y se excluye de todas las preguntas de esta lista.
Lima Este = dominio no planificado; se agrupan los años (2022-2025 o 2022-2024). Estrato aproximado =
departamento × área, como en la Capa 2 (C2-D3), porque 2024-2025 no traen el estrato.
Solo se estiman proporciones: los factores del capítulo no expanden a totales de población coherentes (en
2024-2025 el factor corresponde a una submuestra), así que no se calculan cantidades de personas con esta fuente.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from integracion_comun import Estimador
from microdatos_inei import LIMA_ESTE, descargar

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enapres"
PROCESADOS = RAIZ / "data" / "processed"
TOLERANCIA = 1.0

# año: (código de encuesta, módulo, carpeta, archivo, variable de noche, "¿ha dejado o evita?",
#       "¿dejó o evitó en los últimos 12 meses?" (solo se pregunta si la anterior es "sí"), factor)
CONFIG = {
    2022: (785, 1731, "2022_cap600", "CAP_600_URBANO_7.csv", "P611B_1", "P621A_{}", "P621C_{}", "FACTOR"),
    2023: (903, 1819, "2023_cap600", "CAP_600_URBANO_7.csv", "P611B_1", "P621A_{}", "P621C_{}", "FACTOR"),
    2024: (965, 1860, "2024_cap600", "CAP_600_ANUAL_7.csv", "P604", "P646_{}", "P648_{}", "FACTOR_CAP600B"),
    2025: (1030, 2074, "2025_cap400", "CAP_400_URBANO_4.csv", "P405", "P466_{}", "P467_{}", "FACTOR_CAP400"),
}
ANIOS_EVITA = [2022, 2023, 2024]
ITEMS_EVITA = range(1, 8)  # 2022-2024: salir de noche ... llevar dinero, otro


def descargar_todo():
    for anio, (codigo, modulo, carpeta, *_) in CONFIG.items():
        archivos = descargar(codigo, modulo, RAW / carpeta, formato="CSV", extensiones=(".csv", ".pdf"))
        print(f"  {anio}: {[a.name for a in archivos]}")


def _leer(anio):
    _, _, carpeta, archivo, noche, evita, evito_12m, factor = CONFIG[anio]
    ruta = RAW / carpeta / archivo
    primera = ruta.open(encoding="latin1").readline()
    sep = ";" if primera.count(";") > primera.count(",") else ","
    df = pd.read_csv(ruta, sep=sep, encoding="latin1", low_memory=False, dtype=str)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    decimal = (lambda s: s.str.replace(",", ".", regex=False)) if sep == ";" else (lambda s: s)
    num = lambda c: pd.to_numeric(decimal(df[c]), errors="coerce") if c in df else pd.Series(np.nan, index=df.index)
    out = pd.DataFrame({
        "anio": anio,
        "ubigeo": df["CCDD"].str.zfill(2) + df["CCPP"].str.zfill(2) + df["CCDI"].str.zfill(2),
        "estrato": df["CCDD"].str.zfill(2) + "_" + df["AREA"].astype(str),
        "conglomerado": f"{anio}_" + df["CONGLOMERADO"].astype(str),
        "factor": num(factor),
        "edad": num("P208_A"),
        "sexo": num("P207").map({1: "hombre", 2: "mujer"}),
        "noche": num(noche),
    })
    if anio in ANIOS_EVITA:
        for k in ITEMS_EVITA:
            out[f"evita_{k}"] = num(evita.format(k))
            out[f"evito12_{k}"] = num(evito_12m.format(k))
    return out[out.factor.notna() & out.edad.notna()].copy()


def calcular():
    d = pd.concat([_leer(a) for a in CONFIG], ignore_index=True)
    noche_valida = d.noche.between(1, 4)
    noche_insegura = d.noche.isin([1, 2])
    en_evita = d.anio.isin(ANIOS_EVITA)
    # Universo: quienes respondieron la lista ("¿ha dejado o evita...?"); la pregunta de los últimos 12 meses
    # solo se hace a quienes dijeron que sí, así que el resto cuenta como "no" en el numerador.
    cols = [f"evita_{k}" for k in ITEMS_EVITA]
    cols12 = [f"evito12_{k}" for k in ITEMS_EVITA]
    evita_valida = en_evita & d[cols].notna().any(axis=1)
    evita_alguna = (d[cols12] == 1).any(axis=1)
    indicadores = {
        "noche_inseguro": ("Se siente inseguro/a caminando solo/a de noche en su zona o barrio", noche_insegura,
                           noche_valida, "2022-2025"),
        "evito_alguna": ("Dejó o evitó alguna actividad por temor a la delincuencia (últimos 12 meses)",
                         evita_alguna, evita_valida, "2022-2024"),
        "evito_salir_noche": ("Dejó o evitó salir de noche por temor a la delincuencia (últimos 12 meses)",
                              d["evito12_1"] == 1, evita_valida, "2022-2024"),
        "evito_llegar_tarde": ("Dejó o evitó llegar muy tarde a casa por temor a la delincuencia (últimos 12 meses)",
                               d["evito12_4"] == 1, evita_valida, "2022-2024"),
    }
    geos = {"lima_este": d.ubigeo.isin(LIMA_ESTE), "lima_metropolitana": d.ubigeo.str.startswith("1501")}
    sexos = {"total": pd.Series(True, index=d.index), "hombre": d.sexo == "hombre", "mujer": d.sexo == "mujer"}
    edades = {"15-29": d.edad.between(15, 29), "15-19": d.edad.between(15, 19), "20-24": d.edad.between(20, 24),
              "25-29": d.edad.between(25, 29), "30+": d.edad >= 30}
    est = Estimador(d.factor, d.estrato, d.conglomerado, "ENAPRES 2022-2025, capítulo de seguridad ciudadana "
                                                         "(INEI), cálculo propio")
    # Por año (Lima Metropolitana, para validar) y agrupado (Lima Este y Lima Metropolitana).
    for ind, (desc, num, den, periodo) in indicadores.items():
        for anio in sorted(d.anio.unique()):
            if ind != "noche_inseguro" and anio not in ANIOS_EVITA:
                continue
            for s, m_s in sexos.items():
                est.proporcion({"indicador": ind, "descripcion": desc, "nivel_geografico": "lima_metropolitana",
                                "periodo": str(anio), "sexo": s, "grupo_edad": "15-29"},
                               num, den, geos["lima_metropolitana"] & edades["15-29"] & m_s & (d.anio == anio))
        for g, m_g in geos.items():
            for e, m_e in edades.items():
                for s, m_s in sexos.items():
                    if e != "15-29" and s != "total":
                        continue
                    est.proporcion({"indicador": ind, "descripcion": desc, "nivel_geografico": g, "periodo": periodo,
                                    "sexo": s, "grupo_edad": e}, num, den, m_g & m_e & m_s)
    res = est.tabla()
    res.round(3).to_csv(PROCESADOS / "integracion_seguridad_enapres.csv", index=False)

    dj = pd.read_csv(PROCESADOS / "capa1_indicadores_encuestas.csv")
    dj = dj[(dj.nivel_geografico == "lima_metropolitana") & ~dj.sin_dato]
    ref = {"noche_inseguro": dj[dj.indicador == "INSEGURIDAD AL CAMINAR EN SU BARRIO O ZONA DE NOCHE"],
           "evito_alguna": dj[dj.indicador.str.startswith("DEJÓ DE REALIZAR ALGUNA ACTIVIDAD")]}
    val = []
    for ind, r in ref.items():
        propio = res[(res.indicador == ind) & (res.nivel_geografico == "lima_metropolitana") & (res.periodo.str.len() == 4)]
        for _, f in propio.iterrows():
            x = r[(r.anio == int(f.periodo)) & (r.desagregacion == f.sexo)]
            if len(x):
                val.append({"indicador": ind, "anio": int(f.periodo), "sexo": f.sexo, "valor_proyecto": f.valor,
                            "valor_dato_joven": x.valor.iloc[0]})
    val = pd.DataFrame(val)
    val["diferencia"] = val.valor_proyecto - val.valor_dato_joven
    val["dentro_tolerancia"] = val.diferencia.abs() <= TOLERANCIA
    val.round(2).to_csv(PROCESADOS / "integracion_seguridad_enapres_validacion.csv", index=False)
    print(val.round(1).to_string(index=False))
    print(f"Dentro de ±{TOLERANCIA} punto: {val.dentro_tolerancia.sum()} de {len(val)}")
    print(f"{len(res)} estimaciones -> integracion_seguridad_enapres.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[p.parse_args().paso]()
