"""Funciones comunes para preparar los datos del observatorio (lectura, formato de estimaciones)."""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PROC = RAIZ / "data" / "processed"
RES = RAIZ / "resultados"
FUENTES = RAIZ / "fuentes"

LIMA_ESTE = ["Ate", "Chaclacayo", "El Agustino", "La Molina", "Lurigancho-Chosica", "San Juan de Lurigancho",
             "Santa Anita"]
CORTO = {"San Juan de Lurigancho": "SJL", "Lurigancho-Chosica": "Lurigancho-Chosica"}
EDADES = ["15-19", "20-24", "25-29"]
SEXOS = ["total", "mujer", "hombre"]


def leer(nombre):
    return pd.read_csv(PROC / nombre)


def r1(x, d=1):
    return None if x is None or pd.isna(x) else round(float(x), d)


def estimacion(fila, pob=None):
    """Cifra de encuesta con IC 95 %, CV y precisión. Si no es publicable, sin valor."""
    if fila is None:
        return None
    p = fila["precision"]
    if p == "no_publicable" or pd.isna(fila["valor"]):
        return {"v": None, "p": "n", "n": int(fila["n_muestral"])}
    v, ee = float(fila["valor"]), float(fila["ee"])
    lo, hi = max(v - 1.96 * ee, 0), min(v + 1.96 * ee, 100)
    e = {"v": r1(v), "lo": r1(lo), "hi": r1(hi), "cv": r1(fila["cv"]), "p": "c" if p == "confiable" else "r",
         "n": int(fila["n_muestral"])}
    if pob:
        e["per"] = [int(round(lo * pob / 100, -3)), int(round(hi * pob / 100, -3))]
    return e


def buscar(df, **filtros):
    m = pd.Series(True, index=df.index)
    for k, v in filtros.items():
        m &= df[k] == v
    sub = df[m]
    if len(sub) > 1:
        raise ValueError(f"Más de una fila para {filtros}")
    return None if sub.empty else sub.iloc[0]


def lista(x):
    """'a; b; c' -> ['a', 'b', 'c'] (vacío si no hay dato)."""
    return [] if x is None or (isinstance(x, float) and pd.isna(x)) else [p.strip() for p in str(x).split(";") if p.strip()]


def limpio(x):
    """Valor apto para JSON: sin NaN."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    return x
