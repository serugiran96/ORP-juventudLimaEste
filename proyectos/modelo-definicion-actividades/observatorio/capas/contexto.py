"""Capa 1 · Contexto: población, estudio y trabajo, seguridad, organizaciones, natalidad y datos extra."""

import pandas as pd

from .comun import CORTO, EDADES, LIMA_ESTE, RES, SEXOS, buscar, estimacion, leer, r1


# ---------------------------------------------------------------------------------------------------------
def poblacion():
    p = leer("capa1_poblacion_joven_distritos.csv")
    p = p[p.lima_este & (p.anio == 2026)].copy()
    p["grupo_edad"] = p.grupo_edad.str.replace(" a ", "-")
    r = leer("capa1_poblacion_resumen.csv")
    r = r[r.lima_este & (r.anio == 2026)].set_index("distrito")
    total_le = p.poblacion.sum()

    def resumen(sub, pob_total, nombre):
        jov = int(sub.poblacion.sum())
        muj = int(sub[sub.sexo == "mujer"].poblacion.sum())
        edad = {e: int(sub[sub.grupo_edad == e].poblacion.sum()) for e in EDADES}
        return {"nombre": nombre, "corto": CORTO.get(nombre, nombre), "jovenes": jov, "poblacion_total": int(pob_total),
                "pct_joven": r1(100 * jov / pob_total), "pct_de_lima_este": r1(100 * jov / total_le),
                "mujeres": muj, "hombres": jov - muj, "pct_mujeres": r1(100 * muj / jov),
                "pct_hombres": r1(100 * (jov - muj) / jov), "edad": edad,
                "pct_edad": {e: r1(100 * v / jov) for e, v in edad.items()}}

    distritos = [resumen(p[p.distrito == d], r.loc[d, "poblacion_total"], d) for d in LIMA_ESTE]
    total = resumen(p, r.loc[LIMA_ESTE, "poblacion_total"].sum(), "Lima Este")
    # Población por sexo y edad de Lima Este: base para convertir porcentajes de encuesta en personas.
    base = {}
    for s in SEXOS:
        sub = p if s == "total" else p[p.sexo == s]
        base[s] = {e: int(sub[sub.grupo_edad == e].poblacion.sum()) for e in EDADES}
    for s in SEXOS:
        base[s]["15-29"] = sum(base[s][e] for e in EDADES)
    ev = pd.read_csv(RES / "evidencias.csv").set_index("id")
    encuestas = {k: int(ev.loc[i, "valor"]) for k, i in {"enaho": "E-007", "enapres": "E-008", "enut": "E-009"}.items()}
    return {"anio": 2026, "total": total, "distritos": distritos, "base": base, "encuestas": encuestas}


# ---------------------------------------------------------------------------------------------------------
def estudio(base):
    seg = leer("integracion_enaho_segmentos.csv")
    seg = seg[seg.nivel_geografico == "lima_este"]
    edu = leer("web_educacion_enaho.csv")
    edades = ["15-29"] + EDADES

    def s_(indicador, sexo, edad, pob=True, periodo="2022-2025"):
        f = buscar(seg, indicador=indicador, sexo=sexo, grupo_edad=edad, periodo=periodo)
        return estimacion(f, base[sexo][edad] if pob else None)

    def e_(categoria, sexo, edad, geo="lima_este", pob=True):
        f = buscar(edu, nivel_geografico=geo, categoria=categoria, sexo=sexo, grupo_edad=edad)
        return estimacion(f, base[sexo][edad] if (pob and geo == "lima_este") else None)

    situacion, asistencia, nivel, empleo = {}, {}, {}, {}
    for s in SEXOS:
        situacion[s], asistencia[s], nivel[s], empleo[s] = {}, {}, {}, {}
        for e in edades:
            situacion[s][e] = {k: s_(k, s, e) for k in
                               ["solo_estudia", "estudia_y_trabaja", "solo_trabaja", "ni_estudia_ni_trabaja"]}
            asistencia[s][e] = {
                "estudia": e_("Estudia (cualquier nivel)", s, e), "universidad": e_("Universidad", s, e),
                "instituto": e_("Instituto (superior no universitaria)", s, e), "escolar": e_("Escolar", s, e),
                "lm_estudia": e_("Estudia (cualquier nivel)", s, e, "lima_metropolitana"),
                "lm_universidad": e_("Universidad", s, e, "lima_metropolitana"),
                "lm_instituto": e_("Instituto (superior no universitaria)", s, e, "lima_metropolitana")}
            nivel[s][e] = {
                "sin_secundaria": e_("Sin secundaria completa", s, e), "secundaria": e_("Secundaria completa", s, e),
                "tecnica": e_("Superior técnica (incompleta o completa)", s, e),
                "universitaria": e_("Superior universitaria o posgrado (incompleta o completa)", s, e),
                "sin_superior": e_("Sin educación superior", s, e),
                "superior_completa": e_("Superior completa", s, e),
                "lm_sin_superior": e_("Sin educación superior", s, e, "lima_metropolitana")}
            empleo[s][e] = {"desempleo": s_("desempleo", s, e, pob=False), "busca_trabajo": s_("busca_trabajo", s, e)}
        empleo[s]["15-29"]["informal_ocupados"] = s_("informal_ocupados", s, "15-29", pob=False, periodo="2022-2023")
        empleo[s]["15-29"]["independiente_ocupados"] = s_("independiente_ocupados", s, "15-29", pob=False)
    nini = {s: {k: s_(f"nn_{k}", s, "15-29", pob=False) for k in ["busca", "quiere", "hogar", "estudiando"]}
            for s in SEXOS}
    nini["mujer"]["hogar_del_total"] = s_("hogar", "mujer", "15-29")
    return {"situacion": situacion, "asistencia": asistencia, "nivel": nivel, "nini": nini, "empleo": empleo}


# ---------------------------------------------------------------------------------------------------------
def seguridad(base):
    g = leer("integracion_seguridad_enapres.csv")
    out = {}
    for ind, periodo in [("noche_inseguro", "2022-2025"), ("evito_alguna", "2022-2024"),
                         ("evito_salir_noche", "2022-2024"), ("evito_llegar_tarde", "2022-2024")]:
        sub = g[(g.indicador == ind) & (g.periodo == periodo)]
        out[ind] = {"periodo": periodo}
        for geo, clave in [("lima_este", "le"), ("lima_metropolitana", "lm")]:
            out[ind][clave] = {}
            for s in SEXOS:
                out[ind][clave][s] = estimacion(buscar(sub, nivel_geografico=geo, sexo=s, grupo_edad="15-29"),
                                                base[s]["15-29"] if geo == "lima_este" else None)
            for e in EDADES + ["30+"]:
                out[ind][clave][e] = estimacion(buscar(sub, nivel_geografico=geo, sexo="total", grupo_edad=e))
    reg = leer("capa1_registros_resumen.csv")
    cem = reg[(reg.registro == "violencia_atendida_cem") & reg.lima_este]
    anual = leer("capa1_registros_distrito_anio.csv")
    serie = anual[(anual.registro == "violencia_atendida_cem") & (anual.nivel_geografico == "lima_este_agregado")]
    out["cem"] = {
        "distritos": [{"nombre": f.distrito, "corto": CORTO.get(f.distrito, f.distrito), "tasa": r1(f.tasa),
                       "casos": int(f.casos_2022_2025)} for f in cem.itertuples()],
        "mediana_lm": r1(cem.mediana_lima_metropolitana.iloc[0]),
        "tasa_le": r1(10000 * cem.promedio_anual.sum() / cem.poblacion_2026.sum()),
        "serie": [{"anio": int(f.anio), "casos": int(f.casos)} for f in serie.itertuples() if pd.isna(f.periodo_parcial)]}
    return out


# ---------------------------------------------------------------------------------------------------------
def organizaciones():
    w = leer("web_participacion_enaho.csv")
    enaho = {}
    for geo, clave in [("lima_este", "le"), ("lima_metropolitana", "lm")]:
        sub = w[(w.nivel_geografico == geo) & (w.categoria == "Participa en algún grupo u organización")]
        enaho[clave] = {s: estimacion(buscar(sub, sexo=s, grupo_edad="15-29")) for s in SEXOS}
        for e in EDADES:
            enaho[clave][e] = estimacion(buscar(sub, sexo="total", grupo_edad=e))
        tipos = w[(w.nivel_geografico == geo) & (w.familia == "tipo_entre_participantes") & (w.sexo == "total")
                  & (w.grupo_edad == "15-29")]
        enaho[clave]["tipos"] = [{"nombre": f.categoria, **estimacion(f._asdict())} for f in tipos.itertuples()]
        papel = w[(w.nivel_geografico == geo) & (w.familia == "papel") & (w.sexo == "total") & (w.grupo_edad == "15-29")]
        enaho[clave]["papel"] = [{"nombre": f.categoria, **estimacion(f._asdict())} for f in papel.itertuples()]

    o = leer("capa1_renoj_organizaciones.csv")
    le = o[o.lima_este]
    cuenta = lambda col, n=None: [{"nombre": k, "n": int(v)} for k, v in
                                  le.groupby(col).organizaciones.sum().sort_values(ascending=False).head(n).items()]
    rr = leer("capa1_renoj_resumen_distritos.csv")
    renoj = {"total": int(le.organizaciones.sum()), "anios": [int(le.anio_acreditacion.min()), int(le.anio_acreditacion.max())],
             "tipo": cuenta("detalle_tipo", 6), "tema": cuenta("tematica_1", 8),
             "por_anio": [{"anio": int(k), "n": int(v)} for k, v in le.groupby("anio_acreditacion").organizaciones.sum().items()],
             "distritos": [{"nombre": f.distrito, "corto": CORTO.get(f.distrito, f.distrito),
                            "n": int(f.organizaciones_acumuladas), "por_10mil": r1(f.organizaciones_por_10mil_jovenes)}
                           for f in rr[rr.lima_este].itertuples()],
             "mediana_lm": r1(rr[rr.nivel_geografico == "distrito"].organizaciones_por_10mil_jovenes.median())}

    v = leer("capa1_voluntariado_distritos.csv")
    v = v[v.lima_este]
    inscritos = int(v[v.variable == "SEXO"].personas.sum())

    def si(var):
        sub = v[v.variable == var]
        return r1(100 * sub[sub.valor.str.upper() == "SI"].personas.sum() / sub.personas.sum())

    def dist(var):
        sub = v[v.variable == var].groupby("valor").personas.sum().sort_values(ascending=False)
        return [{"nombre": k, "pct": r1(100 * n / sub.sum())} for k, n in sub.items()]

    temas = {"EDUCACIÓN": "Educación", "MEDIO_AMBIENTE": "Medio ambiente", "CULTURA": "Cultura", "SALUD": "Salud",
             "CIENCIA": "Ciencia", "DEMOCRACIA": "Democracia", "DEPORTE": "Deporte", "ECONOMÍA": "Economía"}
    intereses = {"EDUCACIÓN_INTEGRAL": "Educación integral", "POBLACIONES_SITUACIÓN_VULNERABILIDAD": "Poblaciones vulnerables",
                 "PARTICIPACIÓN_JUVENIL_MEDIANTE_EL_DEPORTE,_EL_ARTE_Y_LA_CULTURA": "Deporte, arte y cultura",
                 "SALUD_MENTAL_Y_BIENESTAR": "Salud mental y bienestar", "PARTICIPACIÓN_CIUDADANA": "Participación ciudadana",
                 "EDUCACIÓN_PARA_LA_EMPLEABILIDAD": "Empleabilidad"}
    voluntariado = {
        "inscritos": inscritos,
        "pct_mujeres": next(d["pct"] for d in dist("SEXO") if d["nombre"] == "Mujer"),
        "participa_org_juvenil": si("PARTICIPA_ORGANIZACIÓN_JUVENIL"),
        "participa_voluntariado": si("PARTICIPA_VOLUNTARIADO"),
        "experiencia": si("EXPERIENCIA_VOLUNTARIADO"),
        "consejo_juventud": si("PARTICIPA_CONSEJO_DE_JUVENTUD"),
        "temas_experiencia": sorted([{"nombre": n, "pct": si(f"EXPERIENCIA_VOLUNTARIADO_{k}")} for k, n in temas.items()],
                                    key=lambda d: -d["pct"]),
        "temas_interes": sorted([{"nombre": n, "pct": si(f"INTERES_VOLUNTARIADO_{k}")} for k, n in intereses.items()],
                                key=lambda d: -d["pct"]),
        "ocupacion": dist("OCUPACION"), "modalidad": dist("MODALIDAD_VOLUNTARIADO"), "edad": dist("RANGO_EDAD")}
    return {"enaho": enaho, "renoj": renoj, "voluntariado": voluntariado}


# ---------------------------------------------------------------------------------------------------------
def natalidad():
    reg = leer("capa1_registros_resumen.csv")
    m = reg[(reg.registro == "maternidad_adolescente") & reg.lima_este]
    anual = leer("capa1_registros_distrito_anio.csv")
    serie = anual[(anual.registro == "maternidad_adolescente") & (anual.nivel_geografico == "lima_este_agregado")]
    return {"distritos": [{"nombre": f.distrito, "corto": CORTO.get(f.distrito, f.distrito), "tasa": r1(f.tasa),
                           "casos": int(f.casos_2022_2025), "promedio": r1(f.promedio_anual, 0)} for f in m.itertuples()],
            "mediana_lm": r1(m.mediana_lima_metropolitana.iloc[0]),
            "tasa_le": r1(1000 * m.promedio_anual.sum() / m.poblacion_2026.sum()),
            "serie": [{"anio": int(f.anio), "casos": int(f.casos)} for f in serie.itertuples() if pd.isna(f.periodo_parcial)],
            "parcial": [{"anio": int(f.anio), "casos": int(f.casos), "periodo": f.periodo_parcial}
                        for f in serie.itertuples() if not pd.isna(f.periodo_parcial)]}


# ---------------------------------------------------------------------------------------------------------
EXCLUIR_EXTRA = {"Otro", "Otros", "Una vez a la semana", "Cabina publica", "Existencia de partidos políticos",
                 "Falta de cobertura de sistema de seguridad social", "Falta de vivienda", "Nini", "Ninis"}


RENOMBRAR_EXTRA = {"Pea": "Población económicamente activa (PEA)", "Años escolaridad": "Años de escolaridad",
                   "Movil": "Accede a internet desde el celular", "Hogar": "Accede a internet desde el hogar",
                   "Trabajo": "Accede a internet desde el trabajo",
                   "Establecimiento educativo": "Accede a internet desde el centro de estudios"}


def datos_extra():
    """Indicadores de Lima Metropolitana (Dato Joven). El resumen recorta los nombres largos a 60 caracteres:
    se recupera el nombre completo y el tablero (el contexto de la pregunta) de capa1_indicadores_encuestas."""
    r = leer("capa1_resumen_lima_metropolitana.csv")
    ind = leer("capa1_indicadores_encuestas.csv")
    ind = ind[ind.nivel_geografico == "lima_metropolitana"].drop_duplicates("indicador")
    tableros = dict(zip(ind.indicador.str.lower(), ind.tablero))
    completos = list(ind.indicador)
    filas = []
    for f in r.itertuples(index=False):
        d = dict(zip(r.columns, f))
        if d["indicador"] in EXCLUIR_EXTRA:
            continue
        nombre = d["indicador"]
        if len(nombre) >= 55:
            largo = [n for n in completos if n.lower().startswith(nombre.lower())]
            if largo:
                nombre = largo[0][0] + largo[0][1:].lower()
        tablero = tableros.get(nombre.lower(), "")
        nombre = RENOMBRAR_EXTRA.get(nombre, nombre)
        filas.append({"dimension": d["dimensión"], "tablero": tablero, "indicador": nombre, "poblacion": d["población"],
                      "anios": d["años"], "inicial": r1(d["valor inicial"]), "valor": r1(d["último valor"]),
                      "unidad": d["unidad"], "cambio": r1(d["cambio"]), "distinguible": d["cambio distinguible"],
                      "referencial": d["referencial"] == "sí", "mujeres": r1(d["mujeres"]), "hombres": r1(d["hombres"]),
                      "peru": r1(d["Perú"]), "fuente": d["fuente"]})
    return filas


def construir():
    pob = poblacion()
    return {"poblacion": pob, "estudio": estudio(pob["base"]), "seguridad": seguridad(pob["base"]),
            "organizaciones": organizaciones(), "natalidad": natalidad(), "extra": datos_extra()}
