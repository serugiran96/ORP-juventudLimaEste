"""Cruce de evidencia y Actividades: modelo multicriterio, segmentos, patrones, evidencias y fichas.

El modelo se calcula en scripts/modelo_actividades.py (resultados/modelo_*.csv); aquí solo se ordena para la página.
"""

import pandas as pd

from .comun import PROC, RES, limpio, lista

CRITERIOS = ["necesidad", "publico", "practica", "convocatoria", "espacio", "aliados"]


def _num(v):
    return None if pd.isna(v) else float(v)


def _modelo():
    crit = pd.read_csv(RES / "modelo_criterios.csv")
    m = pd.read_csv(RES / "modelo_actividades.csv")
    escenarios = {"recomendado": "Recomendado", "igual": "Todos pesan igual", "necesidades": "Necesidades primero",
                  "alcance": "Alcance primero"}
    pesos = {e: {r.criterio: int(r[f"peso_{e}"]) for _, r in crit.iterrows()} for e in escenarios}
    criterios = [{"id": r.criterio, "nombre": r.nombre, "pregunta": r.pregunta, "reglas": r.reglas, "fuente": r.fuente}
                 for r in crit.itertuples()]
    alternativas = []
    for r in m.to_dict("records"):
        alternativas.append({
            "ficha": r["ficha"], "actividad": r["actividad"], "linea": r["linea"], "tipo": r["tipo_ficha"],
            "puntajes": {c: int(r[f"{c}_puntaje"]) for c in CRITERIOS}, "datos": {c: r[f"{c}_dato"] for c in CRITERIOS},
            "solidez": int(r["solidez_pct"]), "solidez_nivel": r["solidez_nivel"], "n_evidencias": int(r["n_evidencias"]),
            "puestos": {e: int(r[f"puesto_{e}"]) for e in escenarios}, "puesto_min": int(r["puesto_min"]),
            "puesto_max": int(r["puesto_max"]), "nivel_estable": bool(r["nivel_estable"])})
    return {"criterios": criterios, "pesos": pesos, "escenarios": escenarios, "alternativas": alternativas,
            "niveles": [[60, "Mayor potencial"], [45, "Potencial medio"], [0, "Menor respaldo hoy"]]}


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
