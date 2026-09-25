"""Indicadores laborales de jóvenes de 15-29 años con microdatos de la ENAHO (cálculo propio).

Dato Joven publica los indicadores laborales de Lima Metropolitana solo hasta 2023. Este script
los extiende a 2024-2025 con los microdatos públicos de la ENAHO (INEI), y primero **valida la
réplica** comparando 2022-2023 con los valores de Dato Joven (tolerancia: ±1 punto).

Uso (desde la carpeta del proyecto):
    python scripts/empleo_enaho.py descargar   # Módulo 05 (Empleo e Ingresos) -> data/raw/enaho/
    python scripts/empleo_enaho.py calcular    # -> data/processed/capa1_empleo_enaho*.csv

Definiciones (INEI):
- Población: residentes habituales de 15 a 29 años (p208a).
- PEA: ocu500 = 1 (ocupado) o 2 (desocupado abierto).
- Tasa de actividad = PEA / población. Tasa de desempleo = desocupados / PEA.
- Empleo informal = ocupinf = 1 entre los ocupados. Solo 2022-2023: desde 2024 el INEI no publica
  esa variable en el módulo 500, y construirla con otra definición no sería comparable.
- Lima Metropolitana = provincia de Lima (UBIGEO 1501**), sin el Callao, como en Dato Joven.
- Factor de expansión: fac500a. Error estándar por linealización de razones con conglomerados
  (conglome) y estratos (estrato), con estimación por dominio.
"""

import argparse
import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enaho"
PROCESADOS = RAIZ / "data" / "processed"

# Códigos de la ENAHO anual (metodología actualizada) en el portal de microdatos del INEI.
CODIGOS = {2022: 784, 2023: 906, 2024: 966, 2025: 1031}
URL = "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/{codigo}-Modulo05.zip"
COLUMNAS = ["conglome", "vivienda", "hogar", "codperso", "ubigeo", "dominio", "estrato", "p204", "p205",
            "p206", "p207", "p208a", "ocu500", "ocupinf", "fac500a"]
TOLERANCIA = 1.0  # puntos porcentuales para aceptar la réplica
UMBRAL_CV = 15.0


def descargar():
    RAW.mkdir(parents=True, exist_ok=True)
    for anio, codigo in CODIGOS.items():
        destino = RAW / f"enaho_{anio}_modulo05.dta"
        if destino.exists():
            print(f"  {destino.name} ya existe")
            continue
        resp = requests.get(URL.format(codigo=codigo), timeout=600)
        resp.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            dta = [n for n in z.namelist() if n.lower().endswith(".dta") and "500" in n]
            if len(dta) != 1:
                raise RuntimeError(f"{anio}: no se encontró un único archivo del módulo 500: {z.namelist()}")
            destino.write_bytes(z.read(dta[0]))
        print(f"  {destino.name} ({dta[0]})")


def _leer(anio):
    ruta = RAW / f"enaho_{anio}_modulo05.dta"
    disponibles = set(pd.read_stata(ruta, iterator=True).variable_labels())
    # Desde 2024 el INEI ya no incluye la variable de informalidad (ocupinf) en el módulo 500.
    df = pd.read_stata(ruta, columns=[c for c in COLUMNAS if c in disponibles], convert_categoricals=False)
    if "ocupinf" not in df:
        df["ocupinf"] = np.nan
    for c in ["p204", "p205", "p206", "p207", "p208a", "ocu500", "ocupinf"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["ubigeo"] = df["ubigeo"].astype(str).str.zfill(6)
    # Residentes habituales (criterio del INEI para los indicadores de empleo).
    residente = ((df.p204 == 1) & (df.p205 == 2)) | ((df.p204 == 2) & (df.p206 == 1))
    df = df[residente & df.ocu500.notna() & df.fac500a.notna()].copy()
    df["anio"] = anio
    return df


def _razon(df, numerador, denominador, dominio):
    """Razón ponderada y su error estándar (linealización, diseño estratificado por conglomerados).

    numerador, denominador, dominio: arreglos booleanos o numéricos sobre toda la muestra; las
    observaciones fuera del dominio contribuyen con cero (estimación por dominio).
    """
    w = df["fac500a"].to_numpy(float)
    d = np.asarray(dominio, float)
    y = np.asarray(numerador, float) * d
    x = np.asarray(denominador, float) * d
    X = np.sum(w * x)
    if X == 0:
        return np.nan, np.nan, 0
    r = np.sum(w * y) / X
    u = w * (y - r * x) / X
    tot = pd.DataFrame({"h": df["estrato"].to_numpy(), "c": df["conglome"].to_numpy(), "u": u}) \
        .groupby(["h", "c"], observed=True)["u"].sum().reset_index()
    var = 0.0
    for _, g in tot.groupby("h", observed=True):
        n = len(g)
        if n > 1:
            var += n / (n - 1) * np.sum((g["u"] - g["u"].mean()) ** 2)
    return 100 * r, 100 * np.sqrt(var), int(np.sum(x > 0))


def calcular():
    filas = []
    for anio in CODIGOS:
        df = _leer(anio)
        joven = df.p208a.between(15, 29)
        geos = {"lima_metropolitana": df.ubigeo.str.startswith("1501"), "nacional": pd.Series(True, df.index)}
        sexos = {"total": pd.Series(True, df.index), "hombre": df.p207 == 1, "mujer": df.p207 == 2}
        pea = df.ocu500.isin([1, 2])
        ocupado = df.ocu500 == 1
        for geo, en_geo in geos.items():
            for sexo, es_sexo in sexos.items():
                dom = joven & en_geo & es_sexo
                indicadores = [("PEA", pea, pd.Series(True, df.index)), ("DESEMPLEO", df.ocu500 == 2, pea)]
                if df.ocupinf.notna().any():
                    indicadores += [("EMPLEO INFORMAL", df.ocupinf == 1, ocupado),
                                    ("EMPLEO FORMAL", df.ocupinf == 2, ocupado)]
                for indicador, num, den in indicadores:
                    valor, ee, n = _razon(df, num, den, dom)
                    filas.append({"anio": anio, "nivel_geografico": geo, "desagregacion": sexo,
                                  "indicador": indicador, "valor": valor, "ee": ee,
                                  "cv": 100 * ee / valor if valor else np.nan, "n_muestral": n})
        print(f"  {anio}: {len(df)} residentes de 14+ años en la muestra")
    res = pd.DataFrame(filas)
    res["referencial"] = res["cv"] > UMBRAL_CV
    res["fuente"] = "ENAHO (cálculo propio con microdatos del INEI)"
    res["poblacion"] = "15-29"

    # Validación con Dato Joven (mismos indicadores, 2022-2023).
    dj = pd.read_csv(PROCESADOS / "capa1_indicadores_encuestas.csv")
    dj = dj[dj.indicador.isin(res.indicador.unique()) & dj.anio.isin([2022, 2023]) & ~dj.sin_dato
            & dj.tablero.isin(["Tasa de desempleo", "Población económicamente activa (PEA)", "Empleo informal",
                               "Empleo formal"])]
    val = res.merge(dj[["anio", "nivel_geografico", "desagregacion", "indicador", "valor"]],
                    on=["anio", "nivel_geografico", "desagregacion", "indicador"], suffixes=("_enaho", "_dato_joven"))
    val["diferencia"] = val["valor_enaho"] - val["valor_dato_joven"]
    val["dentro_tolerancia"] = val["diferencia"].abs() <= TOLERANCIA
    PROCESADOS.mkdir(parents=True, exist_ok=True)
    val.round(2).to_csv(PROCESADOS / "capa1_empleo_enaho_validacion.csv", index=False)

    # Un indicador se acepta para 2024-2025 solo si su réplica 2022-2023 está dentro de la tolerancia
    # en todas las combinaciones comparables de ese nivel geográfico.
    ok = val.groupby(["nivel_geografico", "indicador"])["dentro_tolerancia"].all().rename("replica_validada")
    res = res.merge(ok.reset_index(), on=["nivel_geografico", "indicador"], how="left")
    res["replica_validada"] = res["replica_validada"].fillna(False)
    res.round(3).to_csv(PROCESADOS / "capa1_empleo_enaho.csv", index=False)

    print("\nValidación contra Dato Joven (2022-2023):")
    print(val[["anio", "nivel_geografico", "desagregacion", "indicador", "valor_enaho", "valor_dato_joven",
               "diferencia"]].round(1).to_string(index=False))
    print(f"\nDentro de ±{TOLERANCIA} punto: {val.dentro_tolerancia.sum()} de {len(val)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar, "calcular": calcular}[p.parse_args().paso]()
