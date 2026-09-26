"""Prueba de factibilidad para la auditoría de la integración (fuentes/auditoria_integracion.md).

Comprueba qué denominadores de Lima Este se pueden estimar con los microdatos de la ENAHO que el proyecto ya
descargó (Módulos 03 y 05, 2022-2025), y con qué precisión. NO produce resultados del proyecto: solo imprime
cifras preliminares para el diagnóstico. No escribe en data/processed/.

Uso (desde la carpeta del proyecto):
    python scripts/auditoria_factibilidad_enaho.py

Definiciones provisionales (a validar antes de usarlas, como en la decisión D15):
- Estudia = matriculado y asiste (p306 = 1 y p307 = 1), como en capa2_educacion_internet_enaho.py.
- Trabaja = ocupado (ocu500 = 1). Busca trabajo = desocupado abierto (ocu500 = 2).
- Lima Este = dominio no planificado, 2022-2025 agrupados; error estándar por linealización (C2-D1, C2-D2).
"""

import glob

import numpy as np
import pandas as pd

from microdatos_inei import LIMA_ESTE, razon

CLAVES = ["conglome", "vivienda", "hogar", "codperso"]
ANIOS = [2022, 2023, 2024, 2025]
POBLACION_2026 = {"15-29": 712279, "15-24": 447115, "mujeres 15-29": 380941}  # capa1_poblacion_joven_distritos


def leer():
    partes = []
    for anio in ANIOS:
        c5 = CLAVES + ["ubigeo", "estrato", "p204", "p205", "p206", "p207", "p208a", "ocu500", "fac500a",
                       "p507", "p546", "p547"] + (["ocupinf"] if anio <= 2023 else [])
        m5 = pd.read_stata(f"data/raw/enaho/enaho_{anio}_modulo05.dta", columns=c5, convert_categoricals=False)
        ruta03 = glob.glob(f"data/raw/enaho/modulo03_{anio}/*300.dta")[0]
        m3 = pd.read_stata(ruta03, columns=CLAVES + ["p301a", "p306", "p307", "p308c1", "t313a"],
                           convert_categoricals=False)
        df = m5.merge(m3, on=CLAVES, how="left")
        for c in df.columns.difference(CLAVES + ["ubigeo", "estrato"]):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["ubigeo"] = df.ubigeo.astype(str).str.zfill(6)
        df["conglome"] = f"{anio}_" + df.conglome.astype(str)
        df["estrato"] = f"{anio}_" + df.estrato.astype(str)
        residente = ((df.p204 == 1) & (df.p205 == 2)) | ((df.p204 == 2) & (df.p206 == 1))
        df = df[residente & df.fac500a.notna() & df.ocu500.notna()].copy()
        df["anio"] = anio
        partes.append(df)
    return pd.concat(partes, ignore_index=True)


def main():
    d = leer()
    le = d.ubigeo.isin(LIMA_ESTE)
    lm = d.ubigeo.str.startswith("1501")
    uno = pd.Series(1.0, index=d.index)
    estudia = (d.p306 == 1) & (d.p307 == 1)
    ocupado = d.ocu500 == 1
    desocupado = d.ocu500 == 2
    inactivo = d.ocu500.isin([3, 4])
    ni_ni = ~estudia & ~ocupado
    j29, j24 = d.p208a.between(15, 29), d.p208a.between(15, 24)
    mujer = d.p207 == 2

    def est(num, den, dom):
        v, ee, n = razon(d.fac500a, d.estrato, d.conglome, num.astype(float), den.astype(float), dom)
        return v, ee, n

    def linea(etiqueta, num, den, dom, base=None):
        v, ee, n = est(num, den, dom & le)
        cv = 100 * ee / v
        lo, hi = v - 1.96 * ee, v + 1.96 * ee
        texto = f"  {etiqueta:64} {v:5.1f} %  CV {cv:4.1f}  n={n:5}  IC95 {lo:4.1f}–{hi:4.1f}"
        if base:
            expansion = d.loc[dom & le].groupby("anio").fac500a.sum().mean()
            texto += (f"  | pob. 2026: {POBLACION_2026[base] * lo / 1e5:4.0f}–{POBLACION_2026[base] * hi / 1e5:4.0f} mil"
                      f"  | expansión ENAHO: {expansion * lo / 1e5:4.0f}–{expansion * hi / 1e5:4.0f} mil")
        print(texto)

    print("1. Réplica de 'Actividades que realizan los jóvenes' (Lima Metropolitana, 15-29) frente a Dato Joven")
    dj = pd.read_csv("data/processed/capa1_indicadores_encuestas.csv")
    dj = dj[(dj.tablero == "Actividades que realizan los jóvenes") & (dj.nivel_geografico == "lima_metropolitana")
            & (dj.desagregacion == "total") & dj.anio.isin(ANIOS)]
    categorias = {"SOLO ESTUDIA": estudia & ~ocupado, "TRABAJA Y ESTUDIA": estudia & ocupado,
                  "SOLO TRABAJA": ~estudia & ocupado, "NINI": ni_ni}
    for anio in ANIOS:
        propio = {k: est(v, uno, j29 & lm & (d.anio == anio))[0] for k, v in categorias.items()}
        ref = dj[dj.anio == anio].set_index("indicador").valor
        print(f"  {anio}: " + "; ".join(f"{k} {propio[k]:.1f} (DJ {ref.get(k, np.nan):.1f})" for k in categorias))

    print("\n2. Población joven de Lima Este según la expansión de la ENAHO (15-29), por año")
    print("  " + "; ".join(f"{a}: {v / 1000:.0f} mil" for a, v in d[le & j29].groupby("anio").fac500a.sum().items())
          + f"  (Dato Joven/REUNIS 2026: {POBLACION_2026['15-29'] / 1000:.0f} mil)")

    print("\n3. Situación de estudio y trabajo, Lima Este 2022-2025 (% de cada grupo)")
    grupos = {"15-29": j29, "15-19": d.p208a.between(15, 19), "20-24": d.p208a.between(20, 24),
              "25-29": d.p208a.between(25, 29), "hombres 15-29": j29 & (d.p207 == 1), "mujeres 15-29": j29 & mujer}
    for nombre, g in grupos.items():
        print(f" {nombre}")
        for k, v in categorias.items():
            linea(k.lower(), v, uno, g)
        linea("desocupados / PEA", desocupado, d.ocu500.isin([1, 2]), g)

    print("\n4. Composición de quienes no estudian ni trabajan (Lima Este, 15-29)")
    for nombre, g in {"total": j29, "hombres": j29 & (d.p207 == 1), "mujeres": j29 & mujer}.items():
        print(f" {nombre}")
        linea("busca trabajo (desocupado)", ni_ni & desocupado, ni_ni, g)
        linea("inactivo que quería trabajar (p547)", ni_ni & inactivo & (d.p547 == 1), ni_ni, g)
        linea("inactivo dedicado a quehaceres del hogar (p546 = 5)", ni_ni & inactivo & (d.p546 == 5), ni_ni, g)
        linea("inactivo que declara estar estudiando (p546 = 4)", ni_ni & inactivo & (d.p546 == 4), ni_ni, g)
        linea("de vacaciones (t313a = 6)", ni_ni & (d.t313a == 6), ni_ni, g)

    print("\n5. Denominadores de segmentos (Lima Este, % de toda la población del grupo y conversión a población)")
    linea("15-29: no estudia ni trabaja", ni_ni, uno, j29, "15-29")
    linea("15-29: busca trabajo (desocupado)", desocupado, uno, j29, "15-29")
    linea("15-29: sin trabajo y busca o quiere trabajar", desocupado | (inactivo & (d.p547 == 1)), uno, j29, "15-29")
    linea("mujeres 15-29: no estudia ni trabaja y se dedica al hogar", ni_ni & inactivo & (d.p546 == 5), uno,
          j29 & mujer, "mujeres 15-29")
    linea("15-29: estudia y trabaja", estudia & ocupado, uno, j29, "15-29")
    linea("15-29: trabaja como independiente o empleador", ocupado & d.p507.isin([1, 2]), uno, j29, "15-29")
    linea("15-29: ocupado informal (solo 2022-2023)", ocupado & (d.ocupinf == 1), uno, j29 & (d.anio <= 2023),
          "15-29")
    base = ~estudia & (d.p301a == 6)
    linea("15-24: no estudia y su nivel máximo es secundaria completa", base, uno, j24, "15-24")
    for codigo, motivo in [(1, "problemas económicos"), (2, "está trabajando"),
                           (3, "terminó estudios o asiste a academia (categoría mixta)")]:
        linea(f"15-24: ídem, motivo {motivo}", base & (d.t313a == codigo), uno, j24, "15-24")

    print("\n6. Otros indicadores (Lima Este)")
    linea("ocupados 15-29: informales (2022-2023)", ocupado & (d.ocupinf == 1), ocupado & d.ocupinf.notna(),
          j29 & (d.anio <= 2023))
    linea("ocupados 15-29: independientes o empleadores", ocupado & d.p507.isin([1, 2]), ocupado & d.p507.notna(), j29)
    for nombre, g in {"15-19": d.p208a.between(15, 19), "20-29": d.p208a.between(20, 29)}.items():
        linea(f"estudiantes {nombre}: su centro está en otro distrito", estudia & (d.p308c1 == 0),
              estudia & d.p308c1.notna(), g)
    print("\n7. Universo de los motivos para no estudiar (t313a): casos con dato por grupo de edad (toda la muestra)")
    con_dato = d[d.t313a.notna()]
    print("  " + "; ".join(f"{g}: {n}" for g, n in
                          pd.cut(con_dato.p208a, [14, 19, 24, 29, 120], labels=["15-19", "20-24", "25-29", "30+"])
                          .value_counts(sort=False).items()))


if __name__ == "__main__":
    main()
