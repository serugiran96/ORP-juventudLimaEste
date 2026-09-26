"""Participación cultural por grupo de edad en Lima Este, con la ENAPRES 2022-2025 (capítulo 800A).

Extiende capa2_cultura_enapres.py sin modificarlo: usa sus mismas funciones de lectura y estimación, con
nuevos dominios (Lima Este y Lima Metropolitana, 2022-2025 agrupados, por grupo de edad). Sirve para comprobar
si los segmentos de edad de las fichas de actividades tienen datos que los respalden.

Uso (desde la carpeta del proyecto; requiere los microdatos que descarga capa2_cultura_enapres.py):
    python scripts/integracion_cultura_edad_enapres.py
        # -> data/processed/integracion_cultura_edad_enapres.csv (por edad),
        #    integracion_cultura_totales_enapres.csv (personas que realizan cada práctica, 15-29)
        #    e integracion_bases_enapres.csv (población expandida)
"""

from pathlib import Path

import numpy as np
import pandas as pd

import capa2_cultura_enapres as cultura
from integracion_comun import total
from microdatos_inei import LIMA_ESTE, clasificar_precision

RAIZ = Path(__file__).resolve().parent.parent
PROCESADOS = RAIZ / "data" / "processed"


def calcular():
    datos = pd.concat([cultura._leer(a) for a in cultura.CODIGOS], ignore_index=True)
    geos = {"lima_este": datos.ubigeo.isin(LIMA_ESTE), "lima_metropolitana": datos.ubigeo.str.startswith("1501")}
    edades = {"15-19": datos.edad.between(15, 19), "20-24": datos.edad.between(20, 24),
              "25-29": datos.edad.between(25, 29), "15-24": datos.edad.between(15, 24)}
    dominios, claves = {}, {}
    for geo, m_geo in geos.items():
        for edad, m_edad in edades.items():
            nombre = f"{geo}|{edad}"
            dominios[nombre] = m_geo & m_edad
            claves[nombre] = {"periodo": "2022-2025", "nivel_geografico": geo, "grupo_edad": edad, "sexo": "total"}
    cultura.claves = claves  # _estimar() lee las etiquetas de esta variable del módulo
    res = pd.DataFrame(cultura._estimar(datos, dominios))
    res["cv"] = 100 * res["ee"] / res["valor"]
    res.loc[res["valor"] == 0, "cv"] = np.nan
    res["precision"] = clasificar_precision(res["cv"])
    res.loc[(res["valor"] == 0) & (res["n_muestral"] >= 30), "precision"] = "confiable"
    res["fuente"] = "ENAPRES 2022-2025, capítulo 800A (INEI), cálculo propio"
    res.round(3).to_csv(PROCESADOS / "integracion_cultura_edad_enapres.csv", index=False)

    # Base de población según la expansión del capítulo (promedio anual 2022-2025).
    uno = pd.Series(1.0, index=datos.index)
    bases = []
    sexos = {"total": uno.astype(bool), "hombre": datos.sexo == "hombre", "mujer": datos.sexo == "mujer"}
    for geo, m_geo in geos.items():
        for edad, m_edad in {"15-29": datos.edad.between(15, 29), **edades}.items():
            for sexo, m_sexo in sexos.items():
                t, ee = total(datos.factor, datos.estrato, datos.conglomerado, uno, m_geo & m_edad & m_sexo)
                bases.append({"fuente": "ENAPRES 2022-2025, cap. 800A (expansión, promedio anual)",
                              "nivel_geografico": geo, "grupo_edad": edad, "sexo": sexo, "poblacion": t / 4,
                              "ee": ee / 4})
    pd.DataFrame(bases).round(0).to_csv(PROCESADOS / "integracion_bases_enapres.csv", index=False)

    # Personas que realizan cada práctica según la propia encuesta (promedio anual 2022-2025), 15-29.
    practicas = {**{("asistencia", n): datos[f"s8_{k}"] == 1 for k, n in cultura.SERVICIOS.items()},
                 **{("bienes_culturales", n): datos[f"b13_{k}"] == 1 for k, n in cultura.BIENES.items()},
                 **{("patrimonio", n): datos[f"pat_{k}"] == 1 for k, n in cultura.PATRIMONIO.items()}}
    totales = []
    for geo, m_geo in geos.items():
        for sexo, m_sexo in sexos.items():
            dom = m_geo & datos.edad.between(15, 29) & m_sexo
            for (familia, item), m in practicas.items():
                t, ee = total(datos.factor, datos.estrato, datos.conglomerado, m.astype(float), dom)
                totales.append({"familia": familia, "item": item, "nivel_geografico": geo, "grupo_edad": "15-29",
                                "sexo": sexo, "periodo": "2022-2025", "personas_encuesta": t / 4,
                                "personas_encuesta_ee": ee / 4})
    pd.DataFrame(totales).round(0).to_csv(PROCESADOS / "integracion_cultura_totales_enapres.csv", index=False)
    print(f"{len(res)} estimaciones -> integracion_cultura_edad_enapres.csv; bases y totales -> "
          "integracion_bases_enapres.csv, integracion_cultura_totales_enapres.csv")


if __name__ == "__main__":
    calcular()
