"""Utilidades comunes para trabajar con microdatos de encuestas del INEI.

- descargar(): baja un módulo del portal de microdatos (https://proyectos.inei.gob.pe/microdatos/).
- razon(): estima una proporción o razón ponderada con su error estándar por linealización,
  para un diseño estratificado por conglomerados, con estimación por dominio.
- clasificar_precision(): aplica los umbrales de CV del proyecto.
"""

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

URL = "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/{formato}/{codigo}-Modulo{modulo}.zip"

LIMA_ESTE = ["150103", "150107", "150111", "150114", "150118", "150132", "150137"]

# Umbrales de coeficiente de variación (decisión del equipo, Capa 2):
# CV <= 15 % se publica; 15 % < CV <= 25 % se publica como referencial; CV > 25 % no se publica.
CV_REFERENCIAL = 15.0
CV_MAXIMO = 25.0


def descargar(codigo, modulo, destino, formato="STATA", extensiones=(".dta", ".csv", ".pdf")):
    """Descarga y descomprime un módulo. Devuelve la lista de archivos extraídos."""
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    resp = requests.get(URL.format(formato=formato, codigo=codigo, modulo=modulo), timeout=600)
    resp.raise_for_status()
    extraidos = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        for nombre in z.namelist():
            if nombre.lower().endswith(extensiones):
                ruta = destino / Path(nombre).name
                ruta.write_bytes(z.read(nombre))
                extraidos.append(ruta)
    return extraidos


def razon(peso, estrato, conglomerado, numerador, denominador, dominio):
    """Razón ponderada (en %) y su error estándar por linealización.

    Todos los argumentos son arreglos del mismo largo sobre la muestra completa. Las
    observaciones fuera del `dominio` contribuyen con cero (estimación por dominio), de modo
    que el error estándar considera correctamente los dominios no planificados.
    Devuelve (valor, error_estandar, n_muestral_del_denominador).
    """
    w = np.asarray(peso, float)
    d = np.asarray(dominio, float)
    y = np.nan_to_num(np.asarray(numerador, float)) * d
    x = np.nan_to_num(np.asarray(denominador, float)) * d
    X = np.sum(w * x)
    if X == 0:
        return np.nan, np.nan, 0
    r = np.sum(w * y) / X
    u = w * (y - r * x) / X
    tot = pd.DataFrame({"h": np.asarray(estrato), "c": np.asarray(conglomerado), "u": u}) \
        .groupby(["h", "c"], observed=True)["u"].sum().reset_index()
    var = 0.0
    for _, g in tot.groupby("h", observed=True):
        n = len(g)
        if n > 1:
            var += n / (n - 1) * np.sum((g["u"] - g["u"].mean()) ** 2)
    return 100 * r, 100 * np.sqrt(var), int(np.sum(x > 0))


def clasificar_precision(cv):
    """'confiable' (CV <= 15), 'referencial' (15 < CV <= 25) o 'no_publicable' (CV > 25 o sin dato)."""
    cv = pd.Series(cv, dtype=float)
    return np.select([cv <= CV_REFERENCIAL, cv <= CV_MAXIMO], ["confiable", "referencial"], "no_publicable")
