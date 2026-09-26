"""Funciones comunes de los scripts de estimación de la integración (segunda versión).

- total(): total expandido (por ejemplo, la población joven de Lima Este según una encuesta) y su error
  estándar por linealización, con el mismo diseño que microdatos_inei.razon().
- Estimador: acumula filas con valor, error estándar, CV, n y precisión (umbrales del proyecto).
"""

import numpy as np
import pandas as pd

from microdatos_inei import clasificar_precision, razon


def total(peso, estrato, conglomerado, variable, dominio):
    """Total ponderado de `variable` en el `dominio` y su error estándar (conglomerados dentro de estratos)."""
    w = np.asarray(peso, float)
    y = np.nan_to_num(np.asarray(variable, float)) * np.asarray(dominio, float)
    u = w * y
    tot = pd.DataFrame({"h": np.asarray(estrato), "c": np.asarray(conglomerado), "u": u}) \
        .groupby(["h", "c"], observed=True)["u"].sum().reset_index()
    var = 0.0
    for _, g in tot.groupby("h", observed=True):
        n = len(g)
        if n > 1:
            var += n / (n - 1) * np.sum((g["u"] - g["u"].mean()) ** 2)
    return float(u.sum()), float(np.sqrt(var))


class Estimador:
    """Acumula estimaciones de proporciones (en %) para un mismo diseño muestral.

    Con `divisor_total`, cada proporción guarda también el total expandido de su numerador (personas) y su
    error estándar, divididos entre el número de años agrupados: es la cantidad que estima la propia encuesta.
    """

    def __init__(self, peso, estrato, conglomerado, fuente, divisor_total=None):
        self.arg = (peso, estrato, conglomerado)
        self.fuente = fuente
        self.divisor_total = divisor_total
        self.filas = []

    def proporcion(self, claves, numerador, denominador, dominio, divisor_total=None):
        valor, ee, n = razon(*self.arg, numerador.astype(float), denominador.astype(float), dominio)
        fila = {**claves, "valor": valor, "ee": ee, "n_muestral": n}
        divisor = divisor_total or self.divisor_total
        if divisor:
            t, t_ee = total(*self.arg, (numerador.astype(bool) & denominador.astype(bool)).astype(float), dominio)
            fila.update({"personas_encuesta": t / divisor, "personas_encuesta_ee": t_ee / divisor})
        self.filas.append(fila)

    def tabla(self):
        res = pd.DataFrame(self.filas)
        res["cv"] = 100 * res["ee"] / res["valor"]
        res.loc[res["valor"] == 0, "cv"] = np.nan
        res["precision"] = clasificar_precision(res["cv"])
        # Un cero con muestra suficiente es un dato (no hubo casos), no una estimación imprecisa.
        res.loc[(res["valor"] == 0) & (res["n_muestral"] >= 30), "precision"] = "confiable"
        res["fuente"] = self.fuente
        return res
