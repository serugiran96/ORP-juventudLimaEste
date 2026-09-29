"""Capa 3 · Oferta: registro de actividades publicadas (2024-2026), convocatoria declarada y visibilidad."""

import pandas as pd

from .comun import CORTO, FUENTES, LIMA_ESTE, RAIZ, RES, limpio, lista

PUBLICO = {"juventud": "Jóvenes", "adolescentes": "Niños y adolescentes", "todo público": "Todo público",
           "no indica": "No indica", "no": "Fuera de 15–29"}


def construir():
    o = pd.read_csv(FUENTES / "capa3_registro_oferta.csv")
    registros = []
    for r in o.itertuples():
        registros.append({
            "id": r.id, "nombre": r.nombre, "distritos": lista(r.distrito), "temas": lista(r.tematica),
            "tipo": r.tipo_oferta, "publico": PUBLICO.get(r.incluye_15_29, r.incluye_15_29), "publico_txt": limpio(r.publico_declarado),
            "edad": [limpio(r.edad_min), limpio(r.edad_max)], "costo": r.costo, "modalidad": r.modalidad, "anio": int(r.anio),
            "evidencia": r.evidencia, "cifra_n": limpio(r.cifra_n), "cifra_tipo": limpio(r.cifra_tipo), "cifra_texto": limpio(r.cifra_texto),
            "senal": limpio(r.senal_demanda), "organizador": limpio(r.organizador), "tipo_organizador": limpio(r.tipo_organizador),
            "url": lista(str(r.fuente_url).replace(" | ", ";"))[0] if not pd.isna(r.fuente_url) else None})
    g = pd.read_csv(RAIZ / "data" / "raw" / "capa3" / "gobpe_listado.csv")
    g["anio"] = g.fecha.astype(str).str[:4]
    vis = g.groupby(["distrito", "anio"]).size().reset_index(name="n")
    visibilidad = [{"nombre": d, "corto": CORTO.get(d, d),
                    "por_anio": {a: int(n) for a, n in zip(vis[vis.distrito == d].anio, vis[vis.distrito == d].n)}}
                   for d in LIMA_ESTE]
    ev = pd.read_csv(RES / "evidencias.csv").set_index("id")
    return {"registros": registros, "visibilidad": visibilidad, "anios_vis": sorted(vis.anio.unique().tolist()),
            "periodo": [int(o.anio.min()), int(o.anio.max())], "consulta": str(o.fecha_consulta.max()),
            "chaclacayo": int(ev.loc["E-320", "valor"]), "sjl_2024": int(ev.loc["E-321", "valor"])}
