"""Registro de evidencias atómicas de la integración (segunda versión).

Cada evidencia es un dato con su fuente, periodo, ámbito, población, valor, error, CV, n y precisión. Los valores
NO se escriben a mano: se leen de data/processed/ (o de fuentes/ para Ipsos) con un selector. Así, cualquier
cifra de un hallazgo, patrón o ficha remite a una fila de resultados/evidencias.csv y, desde ahí, a un archivo.
La Capa 3 no se repite aquí: su registro (fuentes/capa3_registro_oferta.csv) ya es atómico y se cita por C3-###.

Tipos de dato (columna tipo_dato):
- "dato observado": estimación de una encuesta, conteo de un registro o cifra publicada por la fuente.
- "cálculo derivado": resulta de combinar datos (por ejemplo, porcentaje × población de otra fuente).
Las interpretaciones y las hipótesis no son evidencias: viven en las fichas y los patrones.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
P = RAIZ / "data" / "processed"
_cache = {}


def _csv(ruta):
    if ruta not in _cache:
        _cache[ruta] = pd.read_csv(RAIZ / ruta)
    return _cache[ruta]


def _una(df, ruta, **filtros):
    m = pd.Series(True, index=df.index)
    for k, v in filtros.items():
        m &= df[k].astype(str) == str(v)
    fila = df[m]
    if len(fila) != 1:
        raise ValueError(f"{ruta}: {len(fila)} filas para {filtros}")
    return fila.iloc[0]


AMBITO = {"lima_este": "Lima Este", "lima_metropolitana": "Lima Metropolitana", "nacional": "Nacional"}
SEXO = {"total": "", "hombre": "hombres", "mujer": "mujeres"}


def _poblacion(edad, sexo, extra=""):
    partes = [p for p in [SEXO.get(sexo, sexo), f"{edad} años", extra] if p]
    return " ".join(partes).strip()


def _encuesta(ruta, fuente, periodo_col="periodo", divisor_personas=True, **filtros):
    df = _csv(ruta)
    f = _una(df, ruta, **filtros)
    out = {"archivo": ruta, "fuente": fuente, "valor": f.valor, "ee": f.ee, "cv": f.cv, "n_muestral": f.n_muestral,
           "precision": f.precision, "periodo": str(f[periodo_col]), "ambito": AMBITO[f.nivel_geografico]}
    if "personas_encuesta" in f and pd.notna(f.get("personas_encuesta")):
        out.update({"personas_encuesta": f.personas_encuesta, "personas_encuesta_ee": f.personas_encuesta_ee})
    return out


# --- Selectores por fuente ------------------------------------------------------------------------------------
def enapres(item, familia="asistencia", categoria="Sí", geo="lima_este", sexo="total", edad="15-29"):
    if edad in ("15-29", "30+"):
        r = _encuesta("data/processed/capa2_cultura_enapres.csv", "ENAPRES 2022-2025, cap. 800A (INEI), cálculo propio",
                      periodo="2022-2025", nivel_geografico=geo, grupo_edad=edad, sexo=sexo, familia=familia,
                      item=item, categoria=categoria)
        tot = _csv("data/processed/integracion_cultura_totales_enapres.csv")
        t = tot[(tot.familia == familia) & (tot.item == item) & (tot.nivel_geografico == geo) & (tot.sexo == sexo)
                & (categoria == "Sí") & (edad == "15-29")]
        if len(t) == 1:
            r.update({"personas_encuesta": t.personas_encuesta.iloc[0],
                      "personas_encuesta_ee": t.personas_encuesta_ee.iloc[0]})
        return r
    return _encuesta("data/processed/integracion_cultura_edad_enapres.csv",
                     "ENAPRES 2022-2025, cap. 800A (INEI), cálculo propio", nivel_geografico=geo, grupo_edad=edad,
                     sexo=sexo, familia=familia, item=item, categoria=categoria)


def enaho_ed(familia, categoria, geo="lima_este", sexo="total", edad="15-29", periodo="2022-2025"):
    return _encuesta("data/processed/capa2_educacion_internet_enaho.csv",
                     "ENAHO 2022-2025, Módulo 03 (INEI), cálculo propio", periodo=periodo, nivel_geografico=geo,
                     sexo=sexo, grupo_edad=edad, familia=familia, categoria=categoria)


def segmento(indicador, geo="lima_este", sexo="total", edad="15-29"):
    r = _encuesta("data/processed/integracion_enaho_segmentos.csv",
                  "ENAHO 2022-2025, Módulos 02, 03 y 05 (INEI), cálculo propio", indicador=indicador,
                  nivel_geografico=geo, sexo=sexo, grupo_edad=edad)
    fila = _una(_csv("data/processed/integracion_enaho_segmentos.csv"), "seg", indicador=indicador,
                nivel_geografico=geo, sexo=sexo, grupo_edad=edad)
    r["validacion"] = {"sí": "equivalente a Dato Joven (±1 punto)", "no": "no equivalente a Dato Joven",
                       "sí (D15)": "validado con Dato Joven (D15)"}.get(fila.equivalente_dato_joven,
                                                                        "sin referencia externa")
    return r


def seguridad(indicador, geo="lima_este", sexo="total", edad="15-29"):
    df = _csv("data/processed/integracion_seguridad_enapres.csv")
    periodo = "2022-2025" if indicador == "noche_inseguro" else "2022-2024"
    r = _encuesta("data/processed/integracion_seguridad_enapres.csv",
                  "ENAPRES, capítulo de seguridad ciudadana (INEI), cálculo propio", indicador=indicador,
                  nivel_geografico=geo, sexo=sexo, grupo_edad=edad, periodo=periodo)
    r["validacion"] = "réplica validada con Dato Joven (±1 punto)"
    return r


def enut(indicador, categoria, geo="lima_este", sexo="total", edad="15-29", grupo="todos"):
    r = _encuesta("data/processed/integracion_tiempo_enut.csv", "ENUT 2024 (INEI), cálculo propio",
                  indicador=indicador, categoria=categoria, nivel_geografico=geo, sexo=sexo, grupo_edad=edad,
                  grupo=grupo)
    return r


def enut_c2(categoria, familia="participacion_semanal", geo="lima_este", sexo="total", edad="15-29"):
    return _encuesta("data/processed/capa2_uso_tiempo_enut.csv", "ENUT 2024 (INEI), cálculo propio",
                     familia=familia, categoria=categoria, nivel_geografico=geo, sexo=sexo, grupo_edad=edad)


def dato_joven(indicador, anio, desagregacion="total"):
    df = _csv("data/processed/capa1_indicadores_encuestas.csv")
    df = df[(df.nivel_geografico == "lima_metropolitana") & ~df.sin_dato & ~df.excluida_por_etiqueta_ambigua]
    f = _una(df, "capa1_indicadores_encuestas", indicador=indicador, anio=anio, desagregacion=desagregacion)
    precision = "referencial" if f.referencial else "confiable"
    return {"archivo": "data/processed/capa1_indicadores_encuestas.csv", "fuente": f"Dato Joven ({f.fuente})",
            "valor": f.valor, "ee": f.valor * f.cv / 100, "cv": f.cv, "n_muestral": np.nan, "precision": precision,
            "periodo": str(anio), "ambito": "Lima Metropolitana"}


def reunis(edad, sexo="total"):
    df = _csv("data/processed/capa1_poblacion_joven_distritos.csv")
    df = df[df.lima_este & (df.anio == 2026)]
    grupos = {"15-29": ["15 a 19", "20 a 24", "25 a 29"], "15-24": ["15 a 19", "20 a 24"], "15-19": ["15 a 19"],
              "20-24": ["20 a 24"], "25-29": ["25 a 29"]}
    m = df.grupo_edad.isin(grupos[edad]) & (df.sexo.isin(["hombre", "mujer"]) if sexo == "total" else df.sexo == sexo)
    return float(df[m].poblacion.sum())


def poblacion(edad, sexo="total"):
    return {"archivo": "data/processed/capa1_poblacion_joven_distritos.csv",
            "fuente": "Dato Joven: población joven (REUNIS/INEI)", "valor": reunis(edad, sexo), "periodo": "2026",
            "ambito": "Lima Este (suma de 7 distritos)", "precision": "no aplica"}


def base_encuesta(archivo, edad="15-29", sexo="total", fuente=""):
    f = _una(_csv(archivo), archivo, nivel_geografico="lima_este", grupo_edad=edad, sexo=sexo)
    return {"archivo": archivo, "fuente": fuente, "valor": f.poblacion, "ee": f.ee, "cv": 100 * f.ee / f.poblacion,
            "precision": "no aplica", "periodo": "2022-2025" if "enut" not in archivo else "2024",
            "ambito": "Lima Este (expansión de la encuesta)"}


def registro_anual(registro, anio):
    df = _csv("data/processed/capa1_registros_distrito_anio.csv")
    f = _una(df, "registros", registro=registro, nivel_geografico="lima_este_agregado", anio=anio)
    return {"archivo": "data/processed/capa1_registros_distrito_anio.csv", "fuente": "Dato Joven: registro "
            "administrativo", "valor": f.casos, "precision": "conteo", "periodo": str(anio),
            "ambito": "Lima Este (suma de 7 distritos)"}


def registro_distrito(registro, distrito, campo="tasa"):
    df = _csv("data/processed/capa1_registros_resumen.csv")
    f = _una(df, "registros_resumen", registro=registro, distrito=distrito)
    return {"archivo": "data/processed/capa1_registros_resumen.csv", "fuente": "Dato Joven: registro administrativo",
            "valor": f[campo], "precision": "conteo", "periodo": "2022-2025 (promedio anual; población 2026)",
            "ambito": distrito}


def registro_lm_mediana(registro):
    df = _csv("data/processed/capa1_registros_resumen.csv")
    f = df[df.registro == registro].iloc[0]
    return {"archivo": "data/processed/capa1_registros_resumen.csv", "fuente": "Dato Joven: registro administrativo",
            "valor": f.mediana_lima_metropolitana, "precision": "conteo", "periodo": "2022-2025",
            "ambito": "Lima Metropolitana (mediana de 43 distritos)"}


def registro_desagregado(registro, variable, categoria):
    df = _csv("data/processed/capa1_registros_distrito_desagregado.csv")
    f = _una(df, "desagregado", registro=registro, ubigeo="LIMA_ESTE", variable=variable, categoria=categoria)
    return {"archivo": "data/processed/capa1_registros_distrito_desagregado.csv",
            "fuente": "Dato Joven: registro administrativo", "valor": f.pct_del_distrito, "precision": "conteo",
            "periodo": "2022-2025", "ambito": "Lima Este (suma de 7 distritos)"}


def renoj(distrito=None, campo="organizaciones_acumuladas"):
    df = _csv("data/processed/capa1_renoj_resumen_distritos.csv")
    le = df[df.lima_este]
    valor = le[campo].sum() if distrito is None else _una(le, "renoj", distrito=distrito)[campo]
    return {"archivo": "data/processed/capa1_renoj_resumen_distritos.csv", "fuente": "Dato Joven: RENOJ",
            "valor": valor, "precision": "conteo", "periodo": "2019-2026 (acumulado)",
            "ambito": distrito or "Lima Este (suma de 7 distritos)"}


def renoj_mediana():
    df = _csv("data/processed/capa1_renoj_resumen_distritos.csv")
    d = df[df.nivel_geografico == "distrito"]
    return {"archivo": "data/processed/capa1_renoj_resumen_distritos.csv", "fuente": "Dato Joven: RENOJ",
            "valor": d.organizaciones_por_10mil_jovenes.median(), "precision": "conteo", "periodo": "2019-2026",
            "ambito": "Lima Metropolitana (mediana de 43 distritos)"}


def renoj_tema(tematica_1):
    df = _csv("data/processed/capa1_renoj_organizaciones.csv")
    le = df[df.lima_este]
    return {"archivo": "data/processed/capa1_renoj_organizaciones.csv", "fuente": "Dato Joven: RENOJ",
            "valor": le[le.tematica_1 == tematica_1].organizaciones.sum() if tematica_1 else 0,
            "precision": "conteo", "periodo": "2019-2026 (acumulado)", "ambito": "Lima Este (suma de 7 distritos)"}


def voluntariado(variable=None, valor=None):
    if variable is None:
        df = _csv("data/processed/capa1_voluntariado_resumen_distritos.csv")
        v = df[df.lima_este].personas_inscritas.sum()
    else:
        df = _csv("data/processed/capa1_voluntariado_distritos.csv")
        le = df[df.lima_este & (df.variable == variable)]
        v = 100 * le[le.valor == valor].personas.sum() / le.personas.sum()
    return {"archivo": "data/processed/capa1_voluntariado_distritos.csv", "fuente": "Dato Joven: Programa de "
            "Voluntariado Juvenil (inscritos)", "valor": v, "precision": "conteo", "periodo": "acumulado sin fecha",
            "ambito": "Lima Este (suma de 7 distritos)"}


def reunis_distrito(distrito):
    df = _csv("data/processed/capa1_poblacion_resumen.csv")
    f = _una(df[df.lima_este], "poblacion_resumen", distrito=distrito, anio=2026)
    return {"archivo": "data/processed/capa1_poblacion_resumen.csv",
            "fuente": "Dato Joven: población joven (REUNIS/INEI)", "valor": f.joven_15_29, "periodo": "2026",
            "ambito": distrito, "precision": "no aplica"}


def renoj_grupo(tematica):
    df = _csv("data/processed/capa1_renoj_organizaciones.csv")
    le = df[df.lima_este]
    return {"archivo": "data/processed/capa1_renoj_organizaciones.csv", "fuente": "Dato Joven: RENOJ",
            "valor": le[le.tematica == tematica].organizaciones.sum(), "precision": "conteo",
            "periodo": "2019-2026 (acumulado)", "ambito": "Lima Este (suma de 7 distritos)"}


def oferta(publico=None, tema=None, columna=None, valor=None):
    """Conteos del registro de la Capa 3 (actividades publicadas 2024-2026)."""
    df = _csv("fuentes/capa3_registro_oferta.csv")
    m = pd.Series(True, index=df.index)
    if publico:
        m &= df.incluye_15_29 == publico
    if tema:
        m &= df.tematica.str.split("; ").apply(lambda l: tema in l)
    if columna:
        m &= df[columna] == valor
    return {"archivo": "fuentes/capa3_registro_oferta.csv", "fuente": "Registro de oferta de la Capa 3 (notas "
            "publicadas)", "valor": int(m.sum()), "precision": "conteo", "periodo": "2024-2026",
            "ambito": "7 distritos de Lima Este"}


def visibilidad(distrito, anios):
    df = _csv("data/raw/capa3/gobpe_listado.csv")
    n = int(((df.distrito == distrito) & df.fecha.str[:4].isin([str(a) for a in anios])).sum())
    return {"archivo": "data/raw/capa3/gobpe_listado.csv", "fuente": "gob.pe: notas de prensa municipales",
            "valor": n, "precision": "conteo", "periodo": f"{min(anios)}-{max(anios)}", "ambito": distrito}


def ipsos(indicador, estudio_contiene):
    df = _csv("fuentes/capa2_estudios_ipsos.csv")
    f = df[(df.indicador == indicador) & df.estudio.str.contains(estudio_contiene, regex=False)]
    if len(f) != 1:
        raise ValueError(f"Ipsos: {len(f)} filas para {indicador}")
    f = f.iloc[0]
    return {"archivo": "fuentes/capa2_estudios_ipsos.csv", "fuente": f"Ipsos: {f.estudio}", "valor": f.valor_pct,
            "precision": "sin error publicado", "periodo": f.trabajo_de_campo, "ambito": f.cobertura}


# --- Catálogo ---------------------------------------------------------------------------------------------------
def E(id_, tema, datos, indicador, poblacion_, naturaleza, unidad="%", limitacion="", contar=None, base_personas=None,
      tipo_dato="dato observado"):
    """Una evidencia. `contar` = (edad, sexo) para convertir el % en personas con la población 2026 (Dato Joven)."""
    return {"id": id_, "tema": tema, "indicador": indicador, "poblacion": poblacion_, "naturaleza": naturaleza,
            "unidad": unidad, "limitacion": limitacion, "contar": contar, "tipo_dato": tipo_dato, **datos}


ENC = "encuesta representativa"
REG = "registro administrativo"
AUTO = "registro de autoselección (señal)"
MERC = "estudio de mercado (orientativo)"
DUP_LM = "Lima Este forma parte de Lima Metropolitana: la comparación entre ambas es descriptiva."


def catalogo():
    ev = [
        # Población
        E("E-001", "población", poblacion("15-29"), "Jóvenes de 15 a 29 años", "15-29 años", REG, "personas",
          "Proyección administrativa; las series por edad son inestables entre años (D5): solo nivel 2026."),
        E("E-002", "población", poblacion("15-19"), "Jóvenes de 15 a 19 años", "15-19 años", REG, "personas"),
        E("E-003", "población", poblacion("20-24"), "Jóvenes de 20 a 24 años", "20-24 años", REG, "personas"),
        E("E-004", "población", poblacion("25-29"), "Jóvenes de 25 a 29 años", "25-29 años", REG, "personas"),
        E("E-005", "población", poblacion("15-29", "mujer"), "Mujeres de 15 a 29 años", "mujeres 15-29 años", REG,
          "personas", "En 25-29 hay 56 % de mujeres, una composición poco habitual (D5): usar con cautela por sexo."),
        E("E-006", "población", poblacion("15-29", "hombre"), "Hombres de 15 a 29 años", "hombres 15-29 años", REG,
          "personas"),
        E("E-010", "población", reunis_distrito("San Juan de Lurigancho"), "Jóvenes de 15 a 29 años",
          "15-29 años", REG, "personas"),
        E("E-011", "población", reunis_distrito("Ate"), "Jóvenes de 15 a 29 años", "15-29 años", REG, "personas"),
        E("E-007", "población", base_encuesta("data/processed/integracion_bases_enaho.csv", fuente="ENAHO 2022-2025"),
          "Jóvenes de 15-29 según la expansión de la ENAHO (promedio anual)", "15-29 años", ENC, "personas",
          "Los factores de la encuesta no se calibran por distrito: el total de Lima Este es una estimación con error."),
        E("E-008", "población", base_encuesta("data/processed/integracion_bases_enapres.csv",
                                              fuente="ENAPRES 2022-2025, cap. 800A"),
          "Jóvenes de 15-29 según la expansión de la ENAPRES (promedio anual)", "15-29 años", ENC, "personas",
          "Ídem."),
        E("E-009", "población", base_encuesta("data/processed/integracion_bases_enut.csv", fuente="ENUT 2024"),
          "Jóvenes de 15-29 según la expansión de la ENUT", "15-29 años", ENC, "personas", "Ídem; muestra pequeña."),

        # Educación y acceso a estudios superiores (ENAHO, Lima Este)
        E("E-020", "educación", enaho_ed("educacion", "Asiste actualmente a educación básica o superior"),
          "Asiste a educación básica o superior", "15-29 años", ENC),
        E("E-021", "educación", enaho_ed("educacion", "Asiste actualmente a educación básica o superior", edad="15-19"),
          "Asiste a educación básica o superior", "15-19 años", ENC),
        E("E-022", "educación", enaho_ed("educacion", "Asiste actualmente a educación básica o superior", edad="25-29"),
          "Asiste a educación básica o superior", "25-29 años", ENC),
        E("E-023", "educación", segmento("base_preu", edad="15-24"),
          "No estudia y su nivel máximo es secundaria completa", "15-24 años", ENC,
          limitacion="Situación compatible con prepararse para la educación superior; no mide intención de estudiar.",
          contar=("15-24", "total")),
        E("E-024", "educación", segmento("base_preu_motivo_economico", edad="15-24"),
          "No estudia, secundaria completa y motivo principal: problemas económicos", "15-24 años", ENC,
          limitacion="Motivo principal (respuesta única); la pregunta solo se hace hasta los 24 años.",
          contar=("15-24", "total")),
        E("E-025", "educación", segmento("base_preu_motivo_economico_share", edad="15-24"),
          "Motivo principal: problemas económicos (entre quienes no estudian con secundaria completa)",
          "15-24 años sin estudiar con secundaria completa", ENC),
        E("E-026", "educación", segmento("base_preu_motivo_trabajo_share", edad="15-24"),
          "Motivo principal: está trabajando (entre quienes no estudian con secundaria completa)",
          "15-24 años sin estudiar con secundaria completa", ENC),
        E("E-027", "educación", segmento("base_preu_motivo_termino_o_academia_share", edad="15-24"),
          "Motivo principal: 'terminó sus estudios o asiste a academia preuniversitaria'",
          "15-24 años sin estudiar con secundaria completa", ENC,
          limitacion="Categoría del INEI que mezcla dos situaciones opuestas; no se puede separar."),
        E("E-028", "educación", segmento("base_preu_motivo_termino_o_academia_share", edad="16-19"),
          "Motivo principal: 'terminó sus estudios o asiste a academia preuniversitaria'",
          "16-19 años sin estudiar con secundaria completa", ENC, limitacion="Ídem."),
        E("E-029", "educación", segmento("base_preu", edad="16-19"),
          "No estudia y su nivel máximo es secundaria completa", "16-19 años", ENC,
          limitacion="La población 2026 no tiene el grupo 16-19: solo se estima con la expansión de la encuesta."),
        E("E-038", "educación", segmento("base_preu", sexo="hombre", edad="15-24"),
          "No estudia y su nivel máximo es secundaria completa", "hombres 15-24 años", ENC),
        E("E-039", "educación", segmento("base_preu", sexo="mujer", edad="15-24"),
          "No estudia y su nivel máximo es secundaria completa", "mujeres 15-24 años", ENC),
        E("E-030", "educación", segmento("estudia_otro_distrito", edad="20-24"),
          "Su centro de estudios está en otro distrito (entre quienes asisten)", "20-24 años que estudian", ENC,
          limitacion="Mide desplazamiento para estudiar, no distancia ni tiempo."),
        E("E-031", "educación", segmento("estudia_otro_distrito", edad="15-19"),
          "Su centro de estudios está en otro distrito (entre quienes asisten)", "15-19 años que estudian", ENC),
        E("E-033", "educación", enaho_ed("motivo_no_asistencia", "Está trabajando"),
          "Motivo principal para no estudiar: está trabajando", "15-24 años que no asisten", ENC,
          limitacion="La pregunta solo se hace hasta los 24 años (en el archivo figura como 15-29)."),
        E("E-034", "educación", enaho_ed("motivo_no_asistencia", "Problemas económicos"),
          "Motivo principal para no estudiar: problemas económicos", "15-24 años que no asisten", ENC,
          limitacion="Ídem."),
        E("E-035", "educación", enaho_ed("motivo_no_asistencia", "No le interesa o no le gusta estudiar"),
          "Motivo principal para no estudiar: no le interesa o no le gusta", "15-24 años que no asisten", ENC,
          limitacion="Ídem; motivo de respuesta única, probablemente subdeclarado."),
        E("E-036", "educación", enaho_ed("motivo_no_asistencia", "De vacaciones"),
          "Motivo principal para no estudiar: de vacaciones", "15-24 años que no asisten", ENC, limitacion="Ídem."),
        E("E-037", "educación", enaho_ed("motivo_no_asistencia",
                                         "Terminó sus estudios o asiste a academia preuniversitaria"),
          "Motivo principal para no estudiar: 'terminó sus estudios o asiste a academia'",
          "15-24 años que no asisten", ENC, limitacion="Ídem; categoría mixta del INEI."),
        E("E-032", "digital", enaho_ed("proposito_internet", "Educación formal y capacitación"),
          "Usa internet para educación formal o capacitación (entre usuarios)", "15-29 años usuarios", ENC),

        # Situación de estudio y trabajo (ENAHO, Lima Este)
        E("E-040", "empleo", segmento("estudia_y_trabaja"), "Estudia y trabaja", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-041", "empleo", segmento("solo_estudia"), "Solo estudia", "15-29 años", ENC, contar=("15-29", "total")),
        E("E-042", "empleo", segmento("solo_trabaja"), "Solo trabaja", "15-29 años", ENC,
          limitacion="No equivalente a 'solo trabaja' de Dato Joven (hasta 2 puntos de diferencia).",
          contar=("15-29", "total")),
        E("E-043", "empleo", segmento("ni_estudia_ni_trabaja"), "No estudia ni trabaja (definición del proyecto)",
          "15-29 años", ENC, limitacion="No equivalente a 'NINI' de Dato Joven: no se comparan.",
          contar=("15-29", "total")),
        E("E-044", "empleo", segmento("ni_estudia_ni_trabaja", sexo="mujer"),
          "No estudia ni trabaja (definición del proyecto)", "mujeres 15-29 años", ENC, contar=("15-29", "mujer")),
        E("E-045", "empleo", segmento("ni_estudia_ni_trabaja", sexo="hombre"),
          "No estudia ni trabaja (definición del proyecto)", "hombres 15-29 años", ENC, contar=("15-29", "hombre")),
        E("E-046", "empleo", segmento("desempleo"), "Tasa de desempleo", "15-29 años económicamente activos", ENC),
        E("E-047", "empleo", segmento("desempleo", edad="15-19"), "Tasa de desempleo",
          "15-19 años económicamente activos", ENC),
        E("E-048", "empleo", segmento("busca_trabajo"), "Busca trabajo (desocupado abierto)", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-049", "empleo", segmento("busca_o_quiere_trabajar"), "Sin trabajo y busca o quiere trabajar",
          "15-29 años", ENC, contar=("15-29", "total")),
        E("E-050", "empleo", segmento("busca_o_quiere_trabajar", sexo="mujer"), "Sin trabajo y busca o quiere trabajar",
          "mujeres 15-29 años", ENC, contar=("15-29", "mujer")),
        E("E-051", "empleo", segmento("busca_o_quiere_trabajar", sexo="hombre"),
          "Sin trabajo y busca o quiere trabajar", "hombres 15-29 años", ENC, contar=("15-29", "hombre")),
        E("E-052", "empleo", segmento("nn_busca"), "Busca trabajo (entre quienes no estudian ni trabajan)",
          "15-29 años que no estudian ni trabajan", ENC),
        E("E-053", "empleo", segmento("nn_hogar"), "Se dedica a los quehaceres del hogar (entre quienes no estudian ni "
          "trabajan)", "15-29 años que no estudian ni trabajan", ENC),
        E("E-054", "empleo", segmento("nn_hogar", sexo="mujer"), "Se dedica a los quehaceres del hogar (entre quienes "
          "no estudian ni trabajan)", "mujeres 15-29 años que no estudian ni trabajan", ENC),
        E("E-055", "empleo", segmento("nn_busca", sexo="mujer"), "Busca trabajo (entre quienes no estudian ni "
          "trabajan)", "mujeres 15-29 años que no estudian ni trabajan", ENC),
        E("E-056", "empleo", segmento("informal_ocupados"), "Empleo informal entre los ocupados",
          "15-29 años ocupados", ENC),
        E("E-057", "empleo", segmento("informal"), "Ocupado con empleo informal", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-058", "empleo", segmento("independiente_ocupados"), "Trabaja como independiente o empleador (entre los "
          "ocupados)", "15-29 años ocupados", ENC),
        E("E-059", "empleo", segmento("independiente"), "Trabaja como independiente o empleador", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-064", "empleo", segmento("informal_ocupados", sexo="hombre"), "Empleo informal entre los ocupados",
          "hombres 15-29 años ocupados", ENC),
        E("E-065", "empleo", segmento("informal_ocupados", sexo="mujer"), "Empleo informal entre los ocupados",
          "mujeres 15-29 años ocupadas", ENC),
        E("E-066", "empleo", segmento("independiente", sexo="hombre"), "Trabaja como independiente o empleador",
          "hombres 15-29 años", ENC),
        E("E-067", "empleo", segmento("independiente", sexo="mujer"), "Trabaja como independiente o empleadora",
          "mujeres 15-29 años", ENC),
        E("E-060", "tiempo", enut_c2("Trabajo remunerado y búsqueda de trabajo"),
          "Trabajó o buscó trabajo en la semana (diario)", "15-29 años", ENC),
        E("E-061", "tiempo", enut_c2("Trabajo remunerado y búsqueda de trabajo",
                                     familia="horas_semanales_entre_participantes"),
          "Horas semanales de trabajo remunerado o búsqueda (entre quienes trabajaron)", "15-29 años", ENC, "horas"),
        E("E-063", "tiempo", enut_c2("Estudio"), "Estudió en la semana (diario)", "15-29 años", ENC),

        # Mujeres jóvenes dedicadas al hogar (ENAHO, Lima Este)
        E("E-070", "hogar", segmento("hogar", sexo="mujer"),
          "No estudia ni trabaja y se dedica a los quehaceres del hogar", "mujeres 15-29 años", ENC,
          contar=("15-29", "mujer")),
        E("E-071", "hogar", segmento("hogar", sexo="hombre"),
          "No estudia ni trabaja y se dedica a los quehaceres del hogar", "hombres 15-29 años", ENC,
          contar=("15-29", "hombre")),
        E("E-072", "hogar", segmento("hogar", sexo="mujer", edad="25-29"),
          "No estudia ni trabaja y se dedica a los quehaceres del hogar", "mujeres 25-29 años", ENC),
        E("E-073", "hogar", segmento("hogar", sexo="mujer", edad="15-19"),
          "No estudia ni trabaja y se dedica a los quehaceres del hogar", "mujeres 15-19 años", ENC),
        E("E-074", "hogar", segmento("hogar_en_union", sexo="mujer"), "Conviviente o casada",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-075", "hogar", segmento("resto_en_union", sexo="mujer"), "Conviviente o casada",
          "otras mujeres 15-29", ENC),
        E("E-076", "hogar", segmento("hogar_ninos_0_5", sexo="mujer"), "Vive en un hogar con niños de 0 a 5 años",
          "mujeres 15-29 dedicadas al hogar", ENC, limitacion="No identifica si son sus hijos."),
        E("E-077", "hogar", segmento("resto_ninos_0_5", sexo="mujer"), "Vive en un hogar con niños de 0 a 5 años",
          "otras mujeres 15-29", ENC),
        E("E-078", "hogar", segmento("hogar_edad_25_29", sexo="mujer"), "Tiene 25-29 años",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-079", "hogar", segmento("hogar_secundaria_completa", sexo="mujer"), "Tiene al menos secundaria completa",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-080", "hogar", segmento("hogar_quiere_trabajar", sexo="mujer"), "Quería trabajar la semana anterior",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-081", "hogar", segmento("hogar_uso_internet", sexo="mujer"), "Usó internet el mes anterior",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-082", "hogar", segmento("hogar_internet_educacion", sexo="mujer"),
          "Usa internet para educación o capacitación (entre usuarias)", "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-083", "hogar", segmento("resto_internet_educacion", sexo="mujer"),
          "Usa internet para educación o capacitación (entre usuarias)", "otras mujeres 15-29", ENC),
        E("E-084", "hogar", segmento("hogar_hija", sexo="mujer"), "Es hija del jefe o jefa de hogar",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-085", "hogar", segmento("hogar_jefa_o_esposa", sexo="mujer"), "Es jefa de hogar o esposa/pareja del jefe",
          "mujeres 15-29 dedicadas al hogar", ENC),
        E("E-086", "tiempo", enut("horas_domestico_cuidado", "Semana", geo="lima_metropolitana", sexo="mujer",
                                  grupo="no trabajó ni estudió en la semana"),
          "Horas semanales de trabajo doméstico o de cuidado", "mujeres 15-29 que no trabajaron ni estudiaron en la "
          "semana del diario", ENC, "horas", "Lima Metropolitana; muestra pequeña (ver n); situación medida con el "
          "diario, no con las preguntas de empleo de la ENAHO."),
        E("E-087", "tiempo", enut("horas_domestico_cuidado", "Semana", geo="lima_metropolitana", sexo="mujer",
                                  grupo="trabajó o estudió en la semana"),
          "Horas semanales de trabajo doméstico o de cuidado", "mujeres 15-29 que trabajaron o estudiaron", ENC,
          "horas", "Lima Metropolitana."),
        E("E-088", "tiempo", enut_c2("Cuidado de otras personas del hogar"),
          "Cuidó a otras personas del hogar en la semana", "15-29 años", ENC),
        E("E-089", "tiempo", enut_c2("Cuidado de otras personas del hogar", geo="lima_metropolitana", sexo="mujer"),
          "Cuidó a otras personas del hogar en la semana", "mujeres 15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-090", "tiempo", enut_c2("Cuidado de otras personas del hogar", geo="lima_metropolitana", sexo="hombre"),
          "Cuidó a otras personas del hogar en la semana", "hombres 15-29 años", ENC, limitacion="Lima Metropolitana."),

        # Seguridad (ENAPRES, Lima Este)
        E("E-100", "seguridad", seguridad("noche_inseguro"), "Se siente inseguro/a caminando solo/a de noche en su "
          "zona o barrio", "15-29 años", ENC),
        E("E-101", "seguridad", seguridad("noche_inseguro", sexo="mujer"), "Se siente insegura caminando sola de noche "
          "en su zona o barrio", "mujeres 15-29 años", ENC),
        E("E-102", "seguridad", seguridad("noche_inseguro", sexo="hombre"), "Se siente inseguro caminando solo de "
          "noche en su zona o barrio", "hombres 15-29 años", ENC),
        E("E-103", "seguridad", seguridad("evito_salir_noche"), "Dejó o evitó salir de noche por temor a la "
          "delincuencia (últimos 12 meses)", "15-29 años", ENC, contar=("15-29", "total")),
        E("E-104", "seguridad", seguridad("evito_salir_noche", sexo="mujer"), "Dejó o evitó salir de noche por temor a "
          "la delincuencia (últimos 12 meses)", "mujeres 15-29 años", ENC),
        E("E-105", "seguridad", seguridad("evito_salir_noche", sexo="hombre"), "Dejó o evitó salir de noche por temor "
          "a la delincuencia (últimos 12 meses)", "hombres 15-29 años", ENC),
        E("E-106", "seguridad", seguridad("evito_llegar_tarde"), "Dejó o evitó llegar muy tarde a casa por temor a la "
          "delincuencia (últimos 12 meses)", "15-29 años", ENC),
        E("E-107", "seguridad", seguridad("evito_alguna"), "Dejó o evitó alguna actividad por temor a la delincuencia "
          "(últimos 12 meses)", "15-29 años", ENC),
        E("E-108", "seguridad", seguridad("noche_inseguro", geo="lima_metropolitana"), "Se siente inseguro/a caminando "
          "solo/a de noche en su zona o barrio", "15-29 años", ENC, limitacion=DUP_LM),

        # Cultura (ENAPRES, Lima Este)
        E("E-110", "cultura", enapres("Cine"), "Fue al cine en los últimos 12 meses", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-111", "cultura", enapres("Cine", sexo="mujer"), "Fue al cine en los últimos 12 meses", "mujeres 15-29",
          ENC),
        E("E-112", "cultura", enapres("Cine", sexo="hombre"), "Fue al cine en los últimos 12 meses", "hombres 15-29",
          ENC),
        E("E-113", "cultura", enapres("Cine", familia="forma_de_entrada", categoria="Pagada por otra persona"),
          "Su entrada al cine la pagó otra persona (entre quienes fueron)", "15-29 años que fueron al cine", ENC),
        E("E-114", "cultura", enapres("Cine", familia="motivo_no_asistencia", categoria="Falta de dinero"),
          "Motivo principal para no ir al cine: falta de dinero", "15-29 años que no fueron al cine", ENC),
        E("E-115", "cultura", enapres("Cine", familia="motivo_no_asistencia", categoria="Falta de interés"),
          "Motivo principal para no ir al cine: falta de interés", "15-29 años que no fueron al cine", ENC),
        E("E-116", "cultura", enapres("Cine", familia="motivo_no_asistencia", categoria="Falta de tiempo"),
          "Motivo principal para no ir al cine: falta de tiempo", "15-29 años que no fueron al cine", ENC),
        E("E-117", "cultura", enapres("Cine", edad="15-19"), "Fue al cine en los últimos 12 meses", "15-19 años", ENC),
        E("E-118", "cultura", enapres("Cine", edad="25-29"), "Fue al cine en los últimos 12 meses", "25-29 años", ENC),
        E("E-120", "cultura", enapres("Espectáculo musical (conciertos, festivales)"),
          "Fue a un concierto o festival musical en los últimos 12 meses", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-121", "cultura", enapres("Espectáculo musical (conciertos, festivales)", edad="15-19"),
          "Fue a un concierto o festival musical", "15-19 años", ENC),
        E("E-122", "cultura", enapres("Espectáculo musical (conciertos, festivales)", edad="20-24"),
          "Fue a un concierto o festival musical", "20-24 años", ENC),
        E("E-123", "cultura", enapres("Espectáculo musical (conciertos, festivales)", edad="25-29"),
          "Fue a un concierto o festival musical", "25-29 años", ENC),
        E("E-124", "cultura", enapres("Espectáculo musical (conciertos, festivales)", familia="forma_de_entrada",
                                      categoria="Comprada"),
          "Compró su entrada al concierto (entre quienes fueron)", "15-29 años que fueron", ENC),
        E("E-125", "cultura", enapres("Espectáculo musical (conciertos, festivales)", familia="motivo_no_asistencia",
                                      categoria="Falta de dinero"),
          "Motivo principal para no ir a conciertos: falta de dinero", "15-29 años que no fueron", ENC),
        E("E-126", "cultura", enapres("Espectáculo musical (conciertos, festivales)", familia="motivo_no_asistencia",
                                      categoria="Falta de interés"),
          "Motivo principal para no ir a conciertos: falta de interés", "15-29 años que no fueron", ENC),
        E("E-127", "cultura", enapres("Espectáculo musical (conciertos, festivales)", familia="motivo_no_asistencia",
                                      categoria="Falta de tiempo"),
          "Motivo principal para no ir a conciertos: falta de tiempo", "15-29 años que no fueron", ENC),
        E("E-128", "cultura", enapres("Espectáculo musical (conciertos, festivales)", geo="lima_metropolitana"),
          "Fue a un concierto o festival musical", "15-29 años", ENC, limitacion=DUP_LM),
        E("E-130", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)"),
          "Fue a un festival local o tradicional en los últimos 12 meses", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-131", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)",
                                      geo="lima_metropolitana"),
          "Fue a un festival local o tradicional", "15-29 años", ENC, limitacion=DUP_LM),
        E("E-132", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)",
                                      familia="forma_de_entrada", categoria="Entrada libre"),
          "Entró gratis al festival (entre quienes fueron)", "15-29 años que fueron", ENC),
        E("E-133", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)",
                                      familia="motivo_no_asistencia", categoria="Falta de interés"),
          "Motivo principal para no ir a festivales: falta de interés", "15-29 años que no fueron", ENC),
        E("E-134", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)", edad="15-19"),
          "Fue a un festival local o tradicional", "15-19 años", ENC),
        E("E-135", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)", edad="25-29"),
          "Fue a un festival local o tradicional", "25-29 años", ENC),
        E("E-139", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)", sexo="hombre"),
          "Fue a un festival local o tradicional", "hombres 15-29 años", ENC),
        E("E-159", "cultura", enapres("Festival local o tradicional (fiestas patronales, carnavales)", sexo="mujer"),
          "Fue a un festival local o tradicional", "mujeres 15-29 años", ENC),
        E("E-136", "cultura", enapres("Danza"), "Fue a un espectáculo de danza", "15-29 años", ENC),
        E("E-137", "cultura", enapres("Feria artesanal"), "Fue a una feria artesanal", "15-29 años", ENC),
        E("E-138", "cultura", enapres("Algún espectáculo o exposición en vivo (teatro, danza, circo, música, arte)"),
          "Fue a algún espectáculo o exposición en vivo", "15-29 años", ENC),
        E("E-140", "cultura", enapres("Biblioteca o sala de lectura"), "Fue a una biblioteca o sala de lectura",
          "15-29 años", ENC, contar=("15-29", "total")),
        E("E-141", "cultura", enapres("Biblioteca o sala de lectura", geo="lima_metropolitana"),
          "Fue a una biblioteca o sala de lectura", "15-29 años", ENC, limitacion=DUP_LM),
        E("E-142", "cultura", enapres("Feria del libro"), "Fue a una feria del libro", "15-29 años", ENC,
          contar=("15-29", "total")),
        E("E-143", "cultura", enapres("Feria del libro", familia="forma_de_entrada", categoria="Entrada libre"),
          "Entró gratis a la feria del libro (entre quienes fueron)", "15-29 años que fueron", ENC),
        E("E-144", "cultura", enapres("Feria del libro", familia="motivo_no_asistencia",
                                      categoria="No tiene información oportuna"),
          "Motivo principal para no ir a ferias del libro: no tuvo información oportuna", "15-29 años que no fueron",
          ENC),
        E("E-145", "cultura", enapres("Libros digitales", familia="bienes_culturales"), "Leyó o accedió a libros "
          "digitales", "15-29 años", ENC),
        E("E-146", "cultura", enapres("Libros impresos", familia="bienes_culturales"), "Leyó o accedió a libros "
          "impresos", "15-29 años", ENC),
        E("E-147", "cultura", enut_c2("Leer"), "Leyó en la semana (diario)", "15-29 años", ENC),
        E("E-148", "cultura", enapres("Biblioteca o sala de lectura", familia="forma_de_entrada",
                                      categoria="Entrada libre"),
          "Entró gratis a la biblioteca (entre quienes fueron)", "15-29 años que fueron", ENC),
        E("E-153", "cultura", enapres("Feria del libro", sexo="mujer"), "Fue a una feria del libro",
          "mujeres 15-29 años", ENC),
        E("E-154", "cultura", enapres("Feria del libro", sexo="hombre"), "Fue a una feria del libro",
          "hombres 15-29 años", ENC),
        E("E-155", "cultura", enapres("Feria del libro", edad="15-19"), "Fue a una feria del libro", "15-19 años", ENC),
        E("E-156", "cultura", enapres("Feria del libro", edad="25-29"), "Fue a una feria del libro", "25-29 años", ENC),
        E("E-157", "cultura", enapres("Monumento histórico", familia="patrimonio", edad="15-19"),
          "Visitó un monumento histórico", "15-19 años", ENC),
        E("E-158", "cultura", enapres("Monumento histórico", familia="patrimonio", edad="25-29"),
          "Visitó un monumento histórico", "25-29 años", ENC),
        E("E-150", "cultura", enapres("Monumento histórico", familia="patrimonio"), "Visitó un monumento histórico",
          "15-29 años", ENC, contar=("15-29", "total")),
        E("E-151", "cultura", enapres("Museo", familia="patrimonio"), "Visitó un museo", "15-29 años", ENC),
        E("E-152", "cultura", enapres("Sitio arqueológico", familia="patrimonio"), "Visitó un sitio arqueológico",
          "15-29 años", ENC),
        E("E-160", "digital", enapres("Videojuegos multijugador en línea", familia="bienes_culturales", sexo="hombre"),
          "Jugó videojuegos multijugador en línea", "hombres 15-29 años", ENC, contar=("15-29", "hombre")),
        E("E-161", "digital", enapres("Videojuegos multijugador en línea", familia="bienes_culturales", sexo="mujer"),
          "Jugó videojuegos multijugador en línea", "mujeres 15-29 años", ENC),
        E("E-162", "digital", enapres("Videojuegos en dispositivos móviles", familia="bienes_culturales",
                                      sexo="hombre"), "Jugó videojuegos en el celular", "hombres 15-29 años", ENC),
        E("E-163", "digital", enapres("Videojuegos en dispositivos móviles", familia="bienes_culturales",
                                      sexo="mujer"), "Jugó videojuegos en el celular", "mujeres 15-29 años", ENC),
        E("E-164", "digital", enapres("Videojuegos multijugador en línea", familia="bienes_culturales", edad="15-19"),
          "Jugó videojuegos multijugador en línea", "15-19 años", ENC),
        E("E-165", "digital", enapres("Videojuegos multijugador en línea", familia="bienes_culturales", edad="25-29"),
          "Jugó videojuegos multijugador en línea", "25-29 años", ENC),
        E("E-168", "digital", enapres("Videojuegos multijugador en línea", familia="bienes_culturales"),
          "Jugó videojuegos multijugador en línea", "15-29 años", ENC),
        E("E-169", "digital", enapres("Música por internet", familia="bienes_culturales"),
          "Escuchó música por internet", "15-29 años", ENC),
        E("E-166", "digital", enapres("Películas o video por internet", familia="bienes_culturales"),
          "Vio películas o video por internet", "15-29 años", ENC),
        E("E-167", "digital", enut_c2("Usar computadora, tablet o celular (internet, redes, juegos)"),
          "Usó computadora, tablet o celular en la semana (diario)", "15-29 años", ENC),

        # Deporte, participación y tiempo (ENUT)
        E("E-170", "deporte", enut("participacion_semanal", "Deporte y ejercicio físico"),
          "Hizo deporte o ejercicio en la semana (diario)", "15-29 años", ENC, contar=("15-29", "total")),
        E("E-171", "deporte", enut_c2("Deporte y ejercicio físico", geo="lima_metropolitana", sexo="hombre"),
          "Hizo deporte o ejercicio en la semana", "hombres 15-29 años", ENC,
          limitacion="Lima Metropolitana: la muestra de Lima Este no permite separar por sexo."),
        E("E-172", "deporte", enut_c2("Deporte y ejercicio físico", geo="lima_metropolitana", sexo="mujer"),
          "Hizo deporte o ejercicio en la semana", "mujeres 15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-173", "deporte", enut_c2("Deporte y ejercicio físico", edad="25-29"),
          "Hizo deporte o ejercicio en la semana", "25-29 años", ENC),
        E("E-174", "deporte", enut_c2("Deporte y ejercicio físico", geo="lima_metropolitana"),
          "Hizo deporte o ejercicio en la semana", "15-29 años", ENC, limitacion=DUP_LM),
        E("E-175", "participación", enut("participacion_semanal", "Voluntariado y ayuda a la comunidad u otros hogares"),
          "Hizo voluntariado o ayudó a la comunidad u otros hogares en la semana", "15-29 años", ENC,
          limitacion="Incluye la ayuda a familiares o vecinos de otros hogares: no es solo voluntariado."),
        E("E-190", "tiempo", enut_c2("Aficiones, artes y juegos"), "Dedicó tiempo a aficiones, artes o juegos en la "
          "semana", "15-29 años", ENC),
        E("E-191", "cultura", enut_c2("Asistir a eventos culturales, de entretenimiento o deportivos"),
          "Asistió a eventos culturales, de entretenimiento o deportivos en la semana", "15-29 años", ENC),
        E("E-192", "cultura", enut_c2("Asistir a eventos culturales, de entretenimiento o deportivos",
                                      geo="lima_metropolitana"),
          "Asistió a eventos culturales, de entretenimiento o deportivos en la semana", "15-29 años", ENC,
          limitacion=DUP_LM),
        E("E-176", "tiempo", enut_c2("Tiempo dedicado a pasatiempos", familia="satisfaccion_nada_o_poco_satisfecho"),
          "Poco o nada satisfecho con el tiempo para sus pasatiempos", "15-29 años", ENC),
        E("E-177", "tiempo", enut_c2("Cantidad de tiempo libre", familia="satisfaccion_nada_o_poco_satisfecho"),
          "Poco o nada satisfecho con la cantidad de su tiempo libre", "15-29 años", ENC),
        E("E-180", "tiempo", enut("disponible_en_bloque", "Lunes a viernes, 18:00-22:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones entre 18:00 y 22:00 (día de semana)", "15-29 años", ENC,
          limitacion="Disponibilidad observada en un día registrado; no es preferencia."),
        E("E-181", "tiempo", enut("disponible_en_bloque", "Lunes a viernes, 14:00-18:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones entre 14:00 y 18:00 (día de semana)", "15-29 años", ENC),
        E("E-182", "tiempo", enut("disponible_en_bloque", "Sábado, 14:00-18:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones el sábado entre 14:00 y 18:00", "15-29 años", ENC),
        E("E-183", "tiempo", enut("disponible_en_bloque", "Sábado, 18:00-22:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones el sábado entre 18:00 y 22:00", "15-29 años", ENC),
        E("E-184", "tiempo", enut("disponible_en_bloque", "Domingo, 14:00-18:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones el domingo entre 14:00 y 18:00", "15-29 años", ENC),
        E("E-185", "tiempo", enut("disponible_en_bloque", "Domingo, 09:00-13:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones el domingo entre 09:00 y 13:00", "15-29 años", ENC),
        E("E-186", "tiempo", enut("disponible_en_bloque", "Sábado, 09:00-13:00"),
          "Tiene al menos 2 horas seguidas sin obligaciones el sábado entre 09:00 y 13:00", "15-29 años", ENC),
        E("E-187", "tiempo", enut("disponible_en_bloque", "Lunes a viernes, 18:00-22:00", geo="lima_metropolitana",
                                  sexo="mujer"),
          "Tiene al menos 2 horas seguidas sin obligaciones entre 18:00 y 22:00 (día de semana)",
          "mujeres 15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-188", "tiempo", enut("disponible_en_bloque", "Lunes a viernes, 18:00-22:00", geo="lima_metropolitana",
                                  sexo="hombre"),
          "Tiene al menos 2 horas seguidas sin obligaciones entre 18:00 y 22:00 (día de semana)",
          "hombres 15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-189", "tiempo", enut("horas_no_comprometidas", "Un día de lunes a viernes"),
          "Horas sin obligaciones ni sueño en un día de semana (incluye comer, aseo y descanso)", "15-29 años", ENC,
          "horas"),

        # Salud, violencia y registros (Capa 1)
        E("E-200", "salud mental", dato_joven("EPISODIO DEPRESIVO", 2024, "mujer"), "Tuvo un episodio depresivo en los "
          "últimos 12 meses", "mujeres 15-29 años", ENC, limitacion="Lima Metropolitana; no hay dato de Lima Este."),
        E("E-201", "salud mental", dato_joven("EPISODIO DEPRESIVO", 2024, "hombre"), "Tuvo un episodio depresivo en "
          "los últimos 12 meses", "hombres 15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-202", "violencia", dato_joven("VIOLENCIA FAMILIAR (FÍSICA, PSICOLÓGICA Y/O SEXUAL) EN LOS ÚLTIMOS 12 MESES",
                                           2025),
          "Sufrió violencia de su esposo o compañero en los últimos 12 meses", "mujeres 15-29 años con pareja", ENC,
          limitacion="Lima Metropolitana; serie muy variable entre años (39 %, 52 %, 45 % y 31 % en 2022-2025)."),
        E("E-203", "violencia", registro_anual("violencia_atendida_cem", 2025), "Casos de violencia atendidos por los "
          "CEM (víctimas de 15-29 con domicilio en Lima Este)", "15-29 años", REG, "casos",
          "Mide atenciones, no prevalencia: depende del acceso y de la decisión de acudir."),
        E("E-204", "violencia", registro_desagregado("violencia_atendida_cem", "sexo_victima", "MUJER"),
          "Mujeres entre las víctimas atendidas", "víctimas de 15-29 atendidas", REG, "%", "Ídem."),
        E("E-205", "violencia", registro_desagregado("violencia_atendida_cem", "grupo_edad_victima", "15 a 19"),
          "Víctimas de 15-19 entre las atendidas", "víctimas de 15-29 atendidas", REG, "%", "Ídem."),
        E("E-206", "violencia", registro_desagregado("violencia_cem_por_tipo", "tipo_violencia", "Sexual"),
          "Casos de violencia sexual entre los atendidos", "víctimas de 15-29 atendidas", REG, "%", "Ídem."),
        E("E-207", "maternidad", registro_anual("maternidad_adolescente", 2025), "Nacimientos de madres de 15-19 con "
          "residencia en Lima Este", "mujeres 15-19 años", REG, "nacimientos",
          "Registra nacimientos, no embarazos."),
        E("E-208", "maternidad", registro_anual("maternidad_adolescente", 2019), "Nacimientos de madres de 15-19 con "
          "residencia en Lima Este", "mujeres 15-19 años", REG, "nacimientos"),
        E("E-209", "maternidad", registro_distrito("maternidad_adolescente", "El Agustino"),
          "Nacimientos de madres de 15-19 por 1 000 mujeres de 15-19", "mujeres 15-19 años", REG, "por 1 000"),
        E("E-210", "maternidad", registro_lm_mediana("maternidad_adolescente"),
          "Nacimientos de madres de 15-19 por 1 000 mujeres de 15-19", "mujeres 15-19 años", REG, "por 1 000"),
        E("E-213", "maternidad", registro_distrito("maternidad_adolescente", "Santa Anita"),
          "Nacimientos de madres de 15-19 por 1 000 mujeres de 15-19", "mujeres 15-19 años", REG, "por 1 000"),
        E("E-214", "maternidad", registro_distrito("maternidad_adolescente", "Ate"),
          "Nacimientos de madres de 15-19 por 1 000 mujeres de 15-19", "mujeres 15-19 años", REG, "por 1 000"),
        E("E-211", "maternidad", dato_joven("ALGUNA VEZ EMBARAZADAS", 2024), "Alguna vez estuvo embarazada",
          "mujeres 15-19 años", ENC, limitacion="Lima Metropolitana."),
        E("E-212", "salud", dato_joven("BEBIÓ EN LOS ÚLTIMOS 30 DÍAS", 2025), "Bebió alcohol en los últimos 30 días",
          "15-29 años", ENC, limitacion="Lima Metropolitana."),

        # Participación y organización (Capa 1)
        E("E-220", "participación", dato_joven("PARTICIPACIÓN EN ASOCIACIÓN U ORGANIZACIÓN", 2025),
          "Participa en alguna asociación u organización", "15-29 años", ENC, limitacion="Lima Metropolitana."),
        E("E-221", "participación", renoj(), "Organizaciones juveniles acreditadas (RENOJ)", "organizaciones", AUTO,
          "organizaciones", "Solo las acreditadas; no indica si siguen activas."),
        E("E-222", "participación", renoj("San Juan de Lurigancho", "organizaciones_por_10mil_jovenes"),
          "Organizaciones juveniles acreditadas por 10 000 jóvenes", "organizaciones", AUTO, "por 10 000"),
        E("E-223", "participación", renoj_mediana(), "Organizaciones juveniles acreditadas por 10 000 jóvenes",
          "organizaciones", AUTO, "por 10 000"),
        E("E-224", "participación", renoj_tema("Ciencia, tecnología y TICS"), "Organizaciones acreditadas de ciencia, "
          "tecnología y TIC", "organizaciones", AUTO, "organizaciones"),
        E("E-225", "participación", renoj_grupo("Cultura y arte"), "Organizaciones acreditadas de cultura y arte "
          "(temática agrupada)", "organizaciones", AUTO, "organizaciones"),
        E("E-219", "participación", renoj_tema("Deporte"), "Organizaciones acreditadas con temática principal de "
          "deporte", "organizaciones", AUTO, "organizaciones"),
        E("E-226", "participación", voluntariado(), "Personas inscritas en el Programa de Voluntariado Juvenil",
          "inscritos", AUTO, "personas", "Autoselección; acumulado sin fecha (D11, D18)."),
        E("E-227", "participación", voluntariado("SEXO", "Mujer"), "Mujeres entre los inscritos", "inscritos", AUTO),
        E("E-228", "participación", voluntariado("OCUPACION", "ESTUDIA"), "Solo estudian (entre los inscritos)",
          "inscritos", AUTO),
        E("E-229", "participación", renoj_tema("Democracia y Derechos Humanos"), "Organizaciones acreditadas de "
          "democracia y derechos humanos", "organizaciones", AUTO, "organizaciones"),

        # Digital (Capa 1)
        E("E-230", "digital", dato_joven("REDACTAR UN PROGRAMA INFORMÁTICO MEDIANTE EL USO DE LENGUAJE DE PROGRAMACIÓN "
                                         "ESPECIALIZADO", 2024), "Escribió un programa informático", "15-29 años", ENC,
          limitacion="Lima Metropolitana."),
        E("E-231", "digital", enaho_ed("proposito_internet", "Vender productos o servicios"), "Usa internet para vender "
          "productos o servicios (entre usuarios)", "15-29 años usuarios", ENC),

        # Ipsos (estudios de mercado antiguos, Perú urbano)
        E("E-240", "aspiraciones", ipsos("Tener su propio negocio y ser el jefe", "2020"),
          "Su trabajo ideal es tener su propio negocio y ser el jefe", "13-20 años", MERC,
          limitacion="11 ciudades del Perú urbano, 2020; no describe a Lima Este hoy (C2-D8)."),
        E("E-241", "aspiraciones", ipsos("Desea emprender", "2019"), "Desea emprender",
          "18-20 años sin negocio propio", MERC, limitacion="Perú urbano, 2019 (C2-D8)."),
        E("E-243", "aspiraciones", ipsos("Trabajaba en algo relacionado con su carrera", "2020"),
          "Trabajaba en algo relacionado con su carrera", "13-20 años que trabajaban", MERC,
          limitacion="11 ciudades del Perú urbano, 2020."),
        E("E-244", "diversión", ipsos("Salir a comer", "2019"), "Se divierte fuera de casa saliendo a comer",
          "13-20 años", MERC, limitacion="Perú urbano, 2019."),
        E("E-242", "diversión", ipsos("Tiene cuenta en TikTok", "2022"), "Tiene cuenta en TikTok",
          "18-25 años usuarios de internet", MERC, limitacion="Perú urbano, 2021-2022."),
        # Capa 3: conteos del registro de oferta (lo publicado, no la oferta real)
        E("E-300", "oferta", oferta(), "Actividades publicadas registradas", "todas", "oferta publicada",
          "actividades", "Depende de lo que cada institución publica (sesgo de visibilidad)."),
        E("E-301", "oferta", oferta("juventud"), "Actividades dirigidas a jóvenes", "juventud", "oferta publicada",
          "actividades"),
        E("E-302", "oferta", oferta("adolescentes"), "Actividades para niños y adolescentes", "adolescentes",
          "oferta publicada", "actividades"),
        E("E-303", "oferta", oferta("todo público"), "Actividades para todo público", "todo público",
          "oferta publicada", "actividades"),
        E("E-304", "oferta", oferta(columna="costo", valor="gratuito"), "Actividades gratuitas", "todas",
          "oferta publicada", "actividades"),
        E("E-305", "oferta", oferta(columna="modalidad", valor="presencial"), "Actividades presenciales", "todas",
          "oferta publicada", "actividades"),
        E("E-306", "oferta", oferta("juventud", "empleo y empleabilidad"), "Actividades para jóvenes: empleo",
          "juventud", "oferta publicada", "actividades"),
        E("E-307", "oferta", oferta("juventud", "participación y voluntariado"), "Actividades para jóvenes: "
          "participación y voluntariado", "juventud", "oferta publicada", "actividades"),
        E("E-308", "oferta", oferta("juventud", "educación y preparación preuniversitaria"), "Actividades para "
          "jóvenes: preparación preuniversitaria", "juventud", "oferta publicada", "actividades"),
        E("E-309", "oferta", oferta("juventud", "deporte"), "Actividades para jóvenes: deporte", "juventud",
          "oferta publicada", "actividades"),
        E("E-310", "oferta", oferta("juventud", "salud y salud mental"), "Actividades para jóvenes: salud y salud "
          "mental", "juventud", "oferta publicada", "actividades"),
        E("E-311", "oferta", oferta("juventud", "emprendimiento"), "Actividades para jóvenes: emprendimiento",
          "juventud", "oferta publicada", "actividades"),
        E("E-312", "oferta", oferta("juventud", "tecnología"), "Actividades para jóvenes: tecnología", "juventud",
          "oferta publicada", "actividades"),
        E("E-313", "oferta", oferta(tema="deporte"), "Actividades de deporte (todas las edades)", "todas",
          "oferta publicada", "actividades"),
        E("E-314", "oferta", oferta(tema="arte y cultura"), "Actividades de arte y cultura (todas las edades)", "todas",
          "oferta publicada", "actividades"),
        E("E-315", "oferta", oferta("juventud", "arte y cultura"), "Actividades para jóvenes: arte y cultura",
          "juventud", "oferta publicada", "actividades"),
        E("E-320", "visibilidad", visibilidad("Chaclacayo", [2024, 2025, 2026]), "Notas municipales en gob.pe con "
          "términos de juventud", "—", "cobertura de fuentes", "notas"),
        E("E-321", "visibilidad", visibilidad("San Juan de Lurigancho", [2024]), "Notas municipales en gob.pe con "
          "términos de juventud", "—", "cobertura de fuentes", "notas"),
    ]
    return ev


def _personas_dj(r):
    if not r["contar"] or pd.isna(r.get("ee")):
        return np.nan, np.nan
    edad, sexo = r["contar"]
    base = reunis(edad, sexo)
    return base * max(r["valor"] - 1.96 * r["ee"], 0) / 100, base * (r["valor"] + 1.96 * r["ee"]) / 100


def construir():
    filas = []
    for r in catalogo():
        r = dict(r)
        if pd.notna(r.get("ee")) and r.get("unidad") in ("%", "horas"):
            r["ic95_inf"], r["ic95_sup"] = r["valor"] - 1.96 * r["ee"], r["valor"] + 1.96 * r["ee"]
        r["personas_dj_inf"], r["personas_dj_sup"] = _personas_dj(r)
        if not r["contar"]:
            r.pop("personas_encuesta", None), r.pop("personas_encuesta_ee", None)
        periodo = str(r.get("periodo", ""))
        anio_final = max(int(x) for x in __import__("re").findall(r"\d{4}", periodo)) if any(
            c.isdigit() for c in periodo) else None
        r["antiguedad"] = "reciente (2022 o después)" if anio_final and anio_final >= 2022 else "anterior a 2022"
        r.setdefault("validacion", "")
        r["contar"] = "" if not r["contar"] else f"{r['contar'][0]} {r['contar'][1]}"
        filas.append(r)
    cols = ["id", "tema", "indicador", "poblacion", "ambito", "periodo", "valor", "unidad", "ee", "cv", "ic95_inf",
            "ic95_sup", "n_muestral", "precision", "personas_dj_inf", "personas_dj_sup", "personas_encuesta",
            "personas_encuesta_ee", "naturaleza", "tipo_dato", "validacion", "antiguedad", "fuente", "archivo",
            "limitacion"]
    df = pd.DataFrame(filas)
    for c in cols:
        if c not in df:
            df[c] = np.nan
    df = df[cols]
    if df.id.duplicated().any():
        raise ValueError(f"IDs duplicados: {df[df.id.duplicated()].id.tolist()}")
    return df
