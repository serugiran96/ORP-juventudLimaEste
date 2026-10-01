"""Cruce de evidencia y Actividades: modelo de convocatoria por público, segmentos, patrones, evidencias y fichas.

El modelo se calcula en scripts/modelo_actividades.py (resultados/modelo_*.csv); aquí solo se ordena para la página.
"""

import pandas as pd

from .comun import FUENTES, PROC, RES, limpio, lista


def _num(v):
    return None if pd.isna(v) else float(v)


def _modelo():
    pasos = pd.read_csv(RES / "modelo_criterios.csv")
    m = pd.read_csv(RES / "modelo_actividades.csv")
    p = pd.read_csv(RES / "modelo_publicos.csv")
    perf = pd.read_csv(RES / "modelo_perfil_publicos.csv")
    bloques = [c for c in perf.columns if c.startswith("bloque_")]
    distritos = [c for c in perf.columns if c.startswith("distrito_")]
    nombres_bloque = ["Lunes a viernes, 14:00-18:00", "Lunes a viernes, 18:00-22:00", "Sábado, 09:00-13:00", "Sábado, 14:00-18:00",
                      "Sábado, 18:00-22:00", "Domingo, 09:00-13:00", "Domingo, 14:00-18:00"]
    publicos = [{"k": f"{r.sexo}|{r.edad}", "sexo": r.sexo, "edad": r.edad, "pob": int(r.poblacion), "libre": r.tiempo_libre,
                 "mejor": r.mejor_bloque, "bloques": [r[b] for b in bloques], "evita": r.evita_salir_noche,
                 "inseguro": r.inseguro_noche,
                 "sit": {k: _num(r[k]) for k in ["solo_estudia", "estudia_y_trabaja", "solo_trabaja", "ni_estudia_ni_trabaja", "hogar"]},
                 "dist": {d.replace("distrito_", ""): r[d] for d in distritos}} for _, r in perf.iterrows()]
    tipos = []
    for r in m.to_dict("records"):
        x = p[p.id == r["id"]]
        tipos.append({
            "id": r["id"], "tipo": r["tipo"], "grupo": r["grupo"], "linea": r["linea"], "formato": r["formato_sostenido"],
            "ficha": limpio(r["ficha"]), "medido": bool(r["medido"]), "relacion": r["relacion"], "factor": r["factor"],
            "fren_medidos": bool(r["frenados_medidos"]),
            "prac": {"v": _num(r["prac_valor"]), "p": limpio(r["prac_precision"]), "fuente": limpio(r["prac_fuente"])},
            "fren": {"v": _num(r["fren_valor"]), "fuente": limpio(r["fren_fuente"]), "dinero": _num(r["fren_dinero"]),
                     "info": _num(r["fren_informacion"]), "oferta": _num(r["fren_oferta"])},
            "total": _num(r["convocables"]), "lo": _num(r["convocables_inf"]), "hi": _num(r["convocables_sup"]),
            "pct": _num(r["pct_jovenes"]), "mujeres": _num(r["pct_mujeres"]), "principal": limpio(r["publico_principal"]),
            "puesto": _num(r["puesto"]), "plo": _num(r["puesto_inf"]), "phi": _num(r["puesto_sup"]),
            "conv": {"codigo": r["conv_codigo"], "detalle": limpio(r["conv_detalle"])}, "nec": r["necesidad"],
            "ofertas": lista(r["oferta_ids"]),
            # Por público: [% ya la hace, % frenados, convocables que ya la hacen, convocables frenados]
            "seg": {f"{s.sexo}|{s.edad}": [_num(s.ya), _num(s.frenados), s.conv_ya, s.conv_frenados] for s in x.itertuples()}})
    return {"pasos": [{k: limpio(v) for k, v in r.items()} for r in pasos.to_dict("records")], "bloques": nombres_bloque,
            "publicos": publicos, "tipos": tipos}


def _fichas():
    f = pd.read_csv(RES / "fichas_actividad.csv")
    comp = pd.read_csv(RES / "fichas_componentes.csv")
    conv = pd.read_csv(RES / "fichas_convocatoria.csv")
    out = {}
    for r in f.to_dict("records"):
        cid = r["id"]
        out[cid] = {k: limpio(r[k]) for k in ["id", "linea", "actividad", "tipo_ficha", "segmentos", "necesidad_tipo", "necesidad",
                                                "poblacion", "interes_codigo", "interes", "salto_inferencial", "alcance_tipo",
                                                "alcance", "oferta", "convocatoria_codigo", "convocatoria_detalle_codigo",
                                                "convocatoria", "barreras", "vacios", "afirmaciones", "hipotesis",
                                                "validacion_piloto", "donde", "evidencias", "cambio_v1", "origen_v1"]}
        out[cid]["componentes"] = [{"componente": c.componente, "estado": c.estado, "nota": limpio(c.nota)}
                                   for c in comp[comp.ficha == cid].itertuples()]
        out[cid]["registros"] = [{"id": c.actividad_c3, "nombre": c.nombre, "distrito": c.distrito, "publico": c.publico,
                                  "evidencia": c.evidencia_c3, "cifra": _num(c.cifra_declarada), "cifra_tipo": limpio(c.cifra_tipo),
                                  "codigo": c.codigo, "nota": limpio(c.nota)} for c in conv[conv.ficha == cid].itertuples()]
    return out


def _evidencias():
    e = pd.read_csv(RES / "evidencias.csv")
    return [{"id": r.id, "tema": r.tema, "indicador": r.indicador, "poblacion": limpio(r.poblacion), "ambito": r.ambito,
             "periodo": str(r.periodo), "valor": _num(r.valor), "unidad": r.unidad, "lo": _num(r.ic95_inf), "hi": _num(r.ic95_sup),
             "precision": r.precision, "fuente": r.fuente, "limitacion": limpio(r.limitacion)} for r in e.itertuples()]


def _condiciones():
    """Condiciones que valen para todas las alternativas (barreras medidas convertidas en requisitos de diseño)."""
    ev = pd.read_csv(RES / "evidencias.csv").set_index("id")
    t = pd.read_csv(PROC / "integracion_tiempo_enut.csv")
    b = t[(t.indicador == "disponible_en_bloque") & (t.nivel_geografico == "lima_este") & (t.sexo == "total")
          & (t.grupo == "todos") & (t.grupo_edad == "15-29")].set_index("categoria")
    c = pd.read_csv(PROC / "capa2_cultura_enapres.csv")
    c = c[(c.nivel_geografico == "lima_este") & (c.periodo == "2022-2025") & (c.sexo == "total") & (c.grupo_edad == "15-29")
          & (c.familia == "forma_de_entrada") & (c.categoria == "Entrada libre")].set_index("item")
    v = lambda i: float(ev.loc[i, "valor"])
    return {
        "horario": {"domingo_tarde": float(b.loc["Domingo, 14:00-18:00", "valor"]), "sabado_noche": float(b.loc["Sábado, 18:00-22:00", "valor"]),
                    "semana_noche": float(b.loc["Lunes a viernes, 18:00-22:00", "valor"]),
                    "semana_tarde": float(b.loc["Lunes a viernes, 14:00-18:00", "valor"]),
                    "semana_tarde_ref": b.loc["Lunes a viernes, 14:00-18:00", "precision"] == "referencial"},
        "seguridad": {"total": v("E-100"), "mujeres": v("E-101"), "hombres": v("E-102")},
        "costo": {"dinero_cine": v("E-114"), "dinero_conciertos": v("E-125"),
                  "gratis_festival": float(c.loc["Festival local o tradicional (fiestas patronales, carnavales)", "valor"]),
                  "gratis_biblioteca": float(c.loc["Biblioteca o sala de lectura", "valor"])},
        "informacion": {"feria_libro": v("E-144")},
        "cuidado": {"hogar_ninos": v("E-076"), "otras_ninos": v("E-077")},
        "tiempo": {"poco_satisfecho": v("E-177")}}


def construir():
    seg = pd.read_csv(RES / "segmentos.csv")
    segmentos = [{"id": r.id, "segmento": r.segmento, "pct": _num(r.porcentaje), "lo": _num(r.ic95_inf), "hi": _num(r.ic95_sup),
                  "ref": r.poblacion_de_referencia, "periodo": r.periodo, "dj": [_num(r.personas_base_dato_joven_inf), _num(r.personas_base_dato_joven_sup)],
                  "enc": _num(r.personas_encuesta), "fichas": lista(r.fichas), "fuente": r.fuente} for r in seg.itertuples()]
    pat = pd.read_csv(RES / "patrones.csv")
    patrones = [{k: limpio(v) for k, v in r.items()} for r in pat.to_dict("records")]
    hal = pd.read_csv(RES / "hallazgos_integrados.csv")
    hallazgos = [{k: limpio(v) for k, v in r.items()} for r in hal.to_dict("records")]
    return {"modelo": _modelo(), "fichas": _fichas(), "segmentos": segmentos, "patrones": patrones, "hallazgos": hallazgos,
            "evidencias": _evidencias(), "condiciones": _condiciones()}
