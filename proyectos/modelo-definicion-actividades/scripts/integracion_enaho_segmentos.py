"""Segmentos de jóvenes de Lima Este con la ENAHO 2022-2025 (Módulos 02, 03 y 05): situación de estudio y
trabajo, búsqueda de empleo, trabajo independiente, informalidad, población compatible con la preparación
preuniversitaria y caracterización de las mujeres jóvenes dedicadas al hogar.

Uso (desde la carpeta del proyecto):
    python scripts/integracion_enaho_segmentos.py descargar  # Módulo 02 -> data/raw/enaho/modulo02_{año}/
    python scripts/integracion_enaho_segmentos.py calcular   # -> data/processed/integracion_enaho_*.csv

Requiere los Módulos 03 y 05, que descargan capa2_educacion_internet_enaho.py y empleo_enaho.py.

Definiciones (fuentes/metodologia_integracion.md, decisiones I2-D3 a I2-D5):
- Asiste = matriculado y asiste (p306 = 1 y p307 = 1), como Dato Joven (validado en C2-D5).
- Estudia = asiste, o no asiste porque está de vacaciones entre ciclos (t313a = 6).
- Trabaja = ocupado (ocu500 = 1). Busca trabajo = desocupado abierto (ocu500 = 2).
- Estudia y trabaja = ocupado que asiste. Solo estudia = estudia y no trabaja. Solo trabaja = ocupado que no
  asiste. No estudia ni trabaja (definición del proyecto) = ni estudia ni trabaja.
- La réplica de Lima Metropolitana se compara con Dato Joven. "Estudia y trabaja" y "solo estudia" son
  equivalentes (±1 punto en todos los años y por sexo); "no estudia ni trabaja" y "solo trabaja" no lo son
  (Dato Joven no publica su tratamiento de los desocupados ocultos). Por eso la categoría del proyecto no se
  llama "NINI" y nunca se compara con la de Dato Joven.
Lima Este = dominio no planificado; 2022-2025 agrupados; umbrales de CV del proyecto (C2-D1).
"""

import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd

from integracion_comun import Estimador, total
from microdatos_inei import LIMA_ESTE, descargar

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enaho"
PROCESADOS = RAIZ / "data" / "processed"
CODIGOS = {2022: 784, 2023: 906, 2024: 966, 2025: 1031}
CLAVES = ["conglome", "vivienda", "hogar", "codperso"]
TOLERANCIA = 1.0


def descargar_todo():
    for anio, codigo in CODIGOS.items():
        archivos = descargar(codigo, "02", RAW / f"modulo02_{anio}", extensiones=(".dta",))
        for a in archivos:
            if a.name.startswith("enaho_tabla"):  # tablas de ocupaciones: no se usan
                a.unlink()
        print(f"  {anio}: {[a.name for a in archivos if a.exists()]}")


def _numericas(df, excluir):
    for c in df.columns.difference(excluir):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _leer(anio):
    c5 = CLAVES + ["ubigeo", "estrato", "p204", "p205", "p206", "p207", "p208a", "ocu500", "fac500a", "p507",
                   "p546", "p547", "p549"] + (["ocupinf"] if anio <= 2023 else [])
    m5 = pd.read_stata(RAW / f"enaho_{anio}_modulo05.dta", columns=c5, convert_categoricals=False)
    m3 = pd.read_stata(glob.glob(str(RAW / f"modulo03_{anio}" / "*300.dta"))[0],
                       columns=CLAVES + ["p301a", "p306", "p307", "p308c1", "t313a", "p314a", "p316_5"],
                       convert_categoricals=False)
    m2 = pd.read_stata(glob.glob(str(RAW / f"modulo02_{anio}" / "*200.dta"))[0],
                       columns=CLAVES + ["p203", "p204", "p208a", "p209"], convert_categoricals=False)
    m2 = _numericas(m2, CLAVES)
    # Niños de 0 a 5 años que son miembros del hogar.
    ninos = m2[(m2.p204 == 1) & (m2.p208a <= 5)].groupby(["conglome", "vivienda", "hogar"]).size() \
        .rename("ninos_0_5").reset_index()
    df = m5.merge(m3, on=CLAVES, how="left").merge(m2[CLAVES + ["p203", "p209"]], on=CLAVES, how="left") \
        .merge(ninos, on=["conglome", "vivienda", "hogar"], how="left")
    df = _numericas(df, CLAVES + ["ubigeo", "estrato"])
    df["ninos_0_5"] = df["ninos_0_5"].fillna(0)
    if "ocupinf" not in df:
        df["ocupinf"] = np.nan
    df["ubigeo"] = df["ubigeo"].astype(str).str.zfill(6)
    df["conglome"] = f"{anio}_" + df["conglome"].astype(str)
    df["estrato"] = f"{anio}_" + df["estrato"].astype(str)
    residente = ((df.p204 == 1) & (df.p205 == 2)) | ((df.p204 == 2) & (df.p206 == 1))
    df = df[residente & df.fac500a.notna() & df.ocu500.notna()].copy()
    df["anio"] = anio
    return df


def _variables(d):
    v = {}
    v["asiste"] = (d.p306 == 1) & (d.p307 == 1)
    v["estudia"] = v["asiste"] | (d.t313a == 6)
    v["ocupado"] = d.ocu500 == 1
    v["desocupado"] = d.ocu500 == 2
    v["pea"] = d.ocu500.isin([1, 2])
    v["inactivo"] = d.ocu500.isin([3, 4])
    v["estudia_y_trabaja"] = v["ocupado"] & v["asiste"]
    v["solo_estudia"] = ~v["ocupado"] & v["estudia"]
    v["solo_trabaja"] = v["ocupado"] & ~v["asiste"]
    v["ni_estudia_ni_trabaja"] = ~v["ocupado"] & ~v["estudia"]
    v["busca_o_quiere_trabajar"] = d.ocu500.isin([2, 3]) | ((d.ocu500 == 4) & (d.p547 == 1))
    v["hogar"] = v["ni_estudia_ni_trabaja"] & v["inactivo"] & (d.p546 == 5)
    v["independiente"] = v["ocupado"] & d.p507.isin([1, 2])
    v["informal"] = v["ocupado"] & (d.ocupinf == 1)
    v["base_preu"] = ~v["estudia"] & (d.p301a == 6)
    return v


def validar(d, v):
    """Réplica de 'Actividades que realizan los jóvenes' (Lima Metropolitana) frente a Dato Joven."""
    dj = pd.read_csv(PROCESADOS / "capa1_indicadores_encuestas.csv")
    dj = dj[(dj.tablero == "Actividades que realizan los jóvenes") & (dj.nivel_geografico == "lima_metropolitana")
            & dj.desagregacion.isin(["total", "hombre", "mujer"]) & dj.anio.isin(CODIGOS)]
    ref = dj.set_index(["anio", "desagregacion", "indicador"]).valor
    equivalencias = {"TRABAJA Y ESTUDIA": "estudia_y_trabaja", "SOLO ESTUDIA": "solo_estudia",
                     "SOLO TRABAJA": "solo_trabaja", "NINI": "ni_estudia_ni_trabaja"}
    j = d.p208a.between(15, 29) & d.ubigeo.str.startswith("1501")
    uno = pd.Series(1.0, index=d.index)
    filas = []
    est = Estimador(d.fac500a, d.estrato, d.conglome, "")
    for anio in CODIGOS:
        for sexo, ms in {"total": j, "hombre": j & (d.p207 == 1), "mujer": j & (d.p207 == 2)}.items():
            for ind_dj, var in equivalencias.items():
                est.filas = []
                est.proporcion({}, v[var], uno, ms & (d.anio == anio))
                valor = est.filas[0]["valor"]
                filas.append({"anio": anio, "sexo": sexo, "categoria_dato_joven": ind_dj, "categoria_proyecto": var,
                              "valor_proyecto": valor, "valor_dato_joven": ref[(anio, sexo, ind_dj)]})
    val = pd.DataFrame(filas)
    val["diferencia"] = val.valor_proyecto - val.valor_dato_joven
    val["dentro_tolerancia"] = val.diferencia.abs() <= TOLERANCIA
    resumen = val.groupby("categoria_proyecto").agg(max_dif=("diferencia", lambda s: s.abs().max()),
                                                   equivalente=("dentro_tolerancia", "all"))
    return val, resumen


def calcular():
    d = pd.concat([_leer(a) for a in CODIGOS], ignore_index=True)
    v = _variables(d)
    val, resumen = validar(d, v)
    val.round(2).to_csv(PROCESADOS / "integracion_enaho_validacion.csv", index=False)
    print("Validación frente a Dato Joven (Lima Metropolitana, 2022-2025, total y por sexo):")
    print(resumen.round(2).to_string())
    equivalente = {k: "sí" if ok else "no" for k, ok in resumen["equivalente"].items()}
    # Indicadores validados en otros scripts con la misma definición (decisión D15 de la Capa 1).
    equivalente.update({"desempleo": "sí (D15)", "informal_ocupados": "sí (D15)"})

    geos = {"lima_este": d.ubigeo.isin(LIMA_ESTE), "lima_metropolitana": d.ubigeo.str.startswith("1501")}
    edades = {"15-29": d.p208a.between(15, 29), "15-19": d.p208a.between(15, 19), "20-24": d.p208a.between(20, 24),
              "25-29": d.p208a.between(25, 29), "15-24": d.p208a.between(15, 24), "16-19": d.p208a.between(16, 19)}
    sexos = {"total": pd.Series(True, index=d.index), "hombre": d.p207 == 1, "mujer": d.p207 == 2}
    uno = pd.Series(True, index=d.index)
    est = Estimador(d.fac500a, d.estrato, d.conglome, "ENAHO 2022-2025, Módulos 02, 03 y 05 (INEI), cálculo propio",
                    divisor_total=4)

    def prop(ind, desc, universo, num, den, dom_extra=None, periodo="2022-2025", edades_=("15-29",),
             sexos_=("total", "hombre", "mujer"), geos_=("lima_este", "lima_metropolitana")):
        m_per = uno if periodo == "2022-2025" else d.anio.isin([2022, 2023])
        for g in geos_:
            for e in edades_:
                for s in sexos_:
                    dom = geos[g] & edades[e] & sexos[s] & m_per
                    if dom_extra is not None:
                        dom = dom & dom_extra
                    est.proporcion({"indicador": ind, "descripcion": desc, "universo": universo,
                                    "nivel_geografico": g, "periodo": periodo, "sexo": s, "grupo_edad": e,
                                    "equivalente_dato_joven": equivalente.get(ind, "no aplica")},
                                   num, den, dom, divisor_total=4 if periodo == "2022-2025" else 2)

    todas = ("15-29", "15-19", "20-24", "25-29")
    # 1. Situación de estudio y trabajo (% de la población del grupo)
    for ind, desc in [("estudia_y_trabaja", "Estudia y trabaja"), ("solo_estudia", "Solo estudia"),
                      ("solo_trabaja", "Solo trabaja"),
                      ("ni_estudia_ni_trabaja", "No estudia ni trabaja (definición del proyecto)")]:
        prop(ind, desc, "población del grupo", v[ind], uno, edades_=todas)
    prop("busca_trabajo", "Busca trabajo (desocupado abierto)", "población del grupo", v["desocupado"], uno,
         edades_=todas)
    prop("desempleo", "Tasa de desempleo", "población económicamente activa", v["desocupado"], v["pea"],
         edades_=todas)
    prop("busca_o_quiere_trabajar", "Sin trabajo y busca o quiere trabajar", "población del grupo",
         v["busca_o_quiere_trabajar"], uno, edades_=todas)
    prop("independiente", "Trabaja como independiente o empleador", "población del grupo", v["independiente"], uno)
    prop("independiente_ocupados", "Independientes o empleadores entre los ocupados", "ocupados",
         v["independiente"], v["ocupado"])
    prop("informal", "Ocupado con empleo informal", "población del grupo", v["informal"], uno, periodo="2022-2023")
    prop("informal_ocupados", "Empleo informal entre los ocupados", "ocupados", v["informal"],
         v["ocupado"] & d.ocupinf.notna(), periodo="2022-2023")

    # 2. Composición de quienes no estudian ni trabajan
    nn = v["ni_estudia_ni_trabaja"]
    for ind, desc, num in [("nn_busca", "Busca trabajo", nn & v["desocupado"]),
                           ("nn_quiere", "No busca, pero quería trabajar",
                            nn & v["inactivo"] & ~v["desocupado"] & ((d.ocu500 == 3) | (d.p547 == 1))),
                           ("nn_hogar", "Se dedica a los quehaceres del hogar", v["hogar"]),
                           ("nn_estudiando", "Declara estar estudiando (sin asistir a educación formal)",
                            nn & v["inactivo"] & (d.p546 == 4))]:
        prop(ind, desc, "no estudia ni trabaja", num, nn)

    # 3. Mujeres dedicadas al hogar: tamaño y caracterización
    prop("hogar", "No estudia ni trabaja y se dedica a los quehaceres del hogar", "población del grupo", v["hogar"],
         uno, edades_=todas, sexos_=("mujer", "hombre"))
    mujer = d.p207 == 2
    grupos_mujer = {"hogar": v["hogar"], "resto": ~v["hogar"]}
    for nombre, seg in grupos_mujer.items():
        for ind, desc, num, den in [
            ("edad_15_19", "Tiene 15-19 años", d.p208a.between(15, 19), seg),
            ("edad_20_24", "Tiene 20-24 años", d.p208a.between(20, 24), seg),
            ("edad_25_29", "Tiene 25-29 años", d.p208a.between(25, 29), seg),
            ("en_union", "Conviviente o casada", d.p209.isin([1, 2]), seg & d.p209.notna()),
            ("jefa_o_esposa", "Es jefa de hogar o esposa/pareja del jefe", d.p203.isin([1, 2]), seg & d.p203.notna()),
            ("hija", "Es hija del jefe de hogar", d.p203 == 3, seg & d.p203.notna()),
            ("ninos_0_5", "Vive en un hogar con niños de 0 a 5 años", d.ninos_0_5 > 0, seg),
            ("secundaria_completa", "Tiene al menos secundaria completa", d.p301a >= 6,
             seg & d.p301a.notna() & (d.p301a != 12)),
            ("quiere_trabajar", "Quería trabajar la semana anterior", d.p547 == 1, seg & d.p547.notna()),
            ("hogar_impide_buscar", "No buscó trabajo porque los quehaceres del hogar no se lo permiten",
             d.p549 == 6, seg & d.p549.notna()),
            ("uso_internet", "Usó internet el mes anterior", d.p314a == 1, seg & d.p314a.notna()),
            ("internet_educacion", "Usa internet para educación o capacitación (entre usuarias)", d.p316_5 == 1,
             seg & (d.p314a == 1) & d.p316_5.notna()),
        ]:
            prop(f"{nombre}_{ind}", desc, f"mujeres 15-29 ({'dedicadas al hogar' if nombre == 'hogar' else 'resto'})",
                 num & den, den, dom_extra=mujer, sexos_=("mujer",))

    # 4. Población compatible con la preparación preuniversitaria
    base = v["base_preu"]
    for e in ("15-24", "16-19", "20-24"):
        prop("base_preu", "No estudia y su nivel máximo es secundaria completa", "población del grupo", base, uno,
             edades_=(e,))
        for cod, ind, desc in [(1, "motivo_economico", "motivo principal: problemas económicos"),
                               (2, "motivo_trabajo", "motivo principal: está trabajando"),
                               (3, "motivo_termino_o_academia", "motivo principal: terminó sus estudios o asiste a "
                                                                "academia (categoría mixta del INEI)")]:
            prop(f"base_preu_{ind}", f"No estudia, secundaria completa y {desc}", "población del grupo",
                 base & (d.t313a == cod), uno, edades_=(e,))
            prop(f"base_preu_{ind}_share", f"Entre quienes no estudian con secundaria completa: {desc}",
                 "no estudia con secundaria completa", base & (d.t313a == cod), base, edades_=(e,))

    # 5. Desplazamiento de quienes estudian
    for e in ("15-19", "20-24", "25-29"):
        prop("estudia_otro_distrito", "Su centro de estudios está en otro distrito", "asiste a educación",
             v["asiste"] & (d.p308c1 == 0), v["asiste"] & d.p308c1.notna(), edades_=(e,), sexos_=("total",))

    res = est.tabla()
    res.round(3).to_csv(PROCESADOS / "integracion_enaho_segmentos.csv", index=False)

    # 6. Bases de población: expansión de la ENAHO (promedio anual 2022-2025)
    bases = []
    for g, m_g in geos.items():
        for e in ("15-29", "15-19", "20-24", "25-29", "15-24", "16-19"):
            for s, m_s in sexos.items():
                t, ee = total(d.fac500a, d.estrato, d.conglome, uno.astype(float), m_g & edades[e] & m_s)
                bases.append({"fuente": "ENAHO 2022-2025 (expansión, promedio anual)", "nivel_geografico": g,
                              "grupo_edad": e, "sexo": s, "poblacion": t / 4, "ee": ee / 4})
    pd.DataFrame(bases).round(0).to_csv(PROCESADOS / "integracion_bases_enaho.csv", index=False)
    print(f"{len(res)} estimaciones -> integracion_enaho_segmentos.csv; bases -> integracion_bases_enaho.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[p.parse_args().paso]()
