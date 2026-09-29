"""Modelo multicriterio de potencial de convocatoria de las alternativas de actividades.

Uso (desde la carpeta del proyecto):
    python scripts/modelo_actividades.py   # -> resultados/modelo_criterios.csv y resultados/modelo_actividades.csv

Cruza, para cada alternativa de resultados/fichas_actividad.csv, seis criterios que responden a preguntas distintas:

    necesidad      ¿Responde a una necesidad documentada de los jóvenes de Lima Este?
    publico        ¿A cuántos jóvenes de Lima Este podría llegar?
    practica       ¿Los jóvenes ya hacen algo parecido?
    convocatoria   ¿Actividades parecidas ya convocaron jóvenes?
    espacio        ¿La oferta actual deja espacio (no la duplica)?
    aliados        ¿Hay organizaciones juveniles del tema que puedan ayudar a convocar?

Cada criterio vale de 0 a 3 con reglas fijas que usan los códigos de la integración (necesidad, P0-P2, C0-C4),
el tamaño de los segmentos, el registro de oferta y el RENOJ. El puntaje es el promedio ponderado (0-100). Ningún
criterio decide solo: ni la cantidad de oferta ni el tamaño del público.

Lo que el modelo NO hace:
- No predice asistencia: ordena las alternativas según cuánto respaldo tienen en la evidencia disponible.
- No trata "sin evidencia" como evidencia negativa: un 0 significa que no hay evidencia a favor.
- Las barreras (horario, seguridad, costo, cuidado) no restan puntos: son condiciones de diseño que valen para todas
  las alternativas y se muestran aparte.
La solidez (porcentaje de la evidencia citada que es de Lima Este y precisa) se informa por separado.
Los protocolos y las poblaciones que requieren consulta directa no se puntúan.
"""

import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"

CRITERIOS = [
    ("necesidad", "Necesidad", "¿Responde a una necesidad documentada de los jóvenes de Lima Este?",
     "3: prevalencia o brecha de acceso medida en Lima Este · 2: registro de atención o situación documentada · "
     "1: objetivo institucional · 0: sin evidencia de necesidad. Una prevalencia medida solo en Lima Metropolitana "
     "vale 2.", "fichas_actividad.csv (necesidad_tipo, necesidad)"),
    ("publico", "Público potencial", "¿A cuántos jóvenes de Lima Este podría llegar?",
     "Límite inferior del segmento con la población 2026 de Dato Joven. 3: 250 mil o más · 2: 100 a 250 mil · "
     "1: 30 a 100 mil · 0: menos de 30 mil o no estimable.", "segmentos.csv"),
    ("practica", "Práctica o interés", "¿Los jóvenes ya hacen algo parecido?",
     "3: practican la misma actividad (P2) · 2: practican algo relacionado (P1) · 1: interés declarado en el tema, "
     "fuera de Lima Este (I1) · 0: sin evidencia (P0).", "fichas_actividad.csv (interes_codigo)"),
    ("convocatoria", "Convocatoria observada", "¿Actividades parecidas ya convocaron jóvenes?",
     "3: más interesados que cupos (C4) · 2: participación declarada comparable (C3) · 1: señales débiles (C2) · "
     "0: sin registros comparables (C0 o C1).", "fichas_actividad.csv (convocatoria_codigo)"),
    ("espacio", "Espacio en la oferta", "¿La oferta actual deja espacio para una actividad nueva?",
     "Actividades para jóvenes del registro de oferta relacionadas con la alternativa. 3: ninguna o una · "
     "2: dos o tres, o la oferta existente se llenó (C4) · 1: cuatro a seis · 0: siete o más.",
     "capa3_registro_oferta.csv, fichas_actividad.csv (actividades_c3)"),
    ("aliados", "Aliados para convocar", "¿Hay organizaciones juveniles del tema que puedan ayudar a convocar?",
     "Organizaciones juveniles acreditadas en Lima Este con temática relacionada (RENOJ). 3: 30 o más · "
     "2: 10 a 29 · 1: 1 a 9 · 0: ninguna.", "capa1_renoj_organizaciones.csv, fuentes/modelo_aliados.csv"),
]
PESOS = {"necesidad": 2, "publico": 2, "practica": 3, "convocatoria": 3, "espacio": 1, "aliados": 1}
ESCENARIOS = {
    "recomendado": ("Recomendado", PESOS),
    "igual": ("Todos pesan igual", {k: 1 for k in PESOS}),
    "necesidades": ("Necesidades primero", {"necesidad": 3, "publico": 2, "practica": 2, "convocatoria": 2,
                                             "espacio": 1, "aliados": 1}),
    "alcance": ("Alcance primero", {"necesidad": 1, "publico": 3, "practica": 2, "convocatoria": 2,
                                     "espacio": 1, "aliados": 1}),
}
NIVELES = [(60, "Mayor potencial"), (45, "Potencial medio"), (0, "Menor respaldo hoy")]
LIMA_ESTE_TXT = re.compile(r"Lima Este|SJL|San Juan de Lurigancho|Ate\b|Chaclacayo|El Agustino|La Molina|"
                           r"Lurigancho|Santa Anita")
AMBITO_LE = re.compile(r"Lima Este|7 distritos|Ate|Chaclacayo|Agustino|Molina|Lurigancho|Anita")


def lista(x):
    return [] if pd.isna(x) else [p.strip() for p in str(x).split(";") if p.strip()]


def mil(v):
    return f"{round(v / 1000):,}".replace(",", " ") + " mil"


def necesidad(f):
    base = {"prevalencia": 3, "brecha de acceso": 3, "registro de atención": 2, "situación documentada": 2,
            "objetivo institucional": 1, "sin evidencia": 0}
    tipos = lista(f.necesidad_tipo)
    # La prevalencia o brecha cuenta como medida fuera de Lima Este si el texto la sitúa primero en Lima Metropolitana.
    texto = str(f.necesidad)
    le, lm = LIMA_ESTE_TXT.search(texto), texto.find("Lima Metropolitana")
    fuera = lm >= 0 and (le is None or lm < le.start())
    medida = ("prevalencia", "brecha de acceso")
    p = max(base[t] - (1 if fuera and t in medida else 0) for t in tipos)
    dato = f.necesidad_tipo + (" (prevalencia medida en Lima Metropolitana)" if fuera and set(tipos) & set(medida) else "")
    return p, dato


def publico(f, seg):
    ids = lista(f.segmentos)
    if not ids:
        return 0, "no estimable"
    s = seg.loc[ids]
    i = s.personas_base_dato_joven_inf.idxmax()
    inf, sup = s.loc[i, "personas_base_dato_joven_inf"], s.loc[i, "personas_base_dato_joven_sup"]
    p = 3 if inf >= 250000 else 2 if inf >= 100000 else 1 if inf >= 30000 else 0
    return p, f"{mil(inf).replace(' mil', '')}–{mil(sup)} ({i})"


def practica(f):
    return {"P2": 3, "P1": 2, "I1": 1, "P0": 0}[f.interes_codigo], f.interes_codigo


def convocatoria(f):
    return {"C4": 3, "C3": 2, "C2": 1, "C1": 0, "C0": 0}[f.convocatoria_codigo], f.convocatoria_codigo


def espacio(f, oferta):
    ids = [i for i in lista(f.actividades_c3) if i in oferta.index]
    n = int((oferta.loc[ids, "incluye_15_29"] == "juventud").sum()) if ids else 0
    p = 3 if n <= 1 else 2 if n <= 3 else 1 if n <= 6 else 0
    lleno = f.convocatoria_codigo == "C4"
    if lleno:
        p = max(p, 2)
    return p, f"{n} actividad{'es' if n != 1 else ''} para jóvenes" + ("; la oferta se llenó (C4)" if lleno else "")


def aliados(f, renoj, mapa):
    temas = lista(mapa.get(f.id, ""))
    n = int(renoj[renoj.tematica_1.isin(temas)].organizaciones.sum()) if temas else 0
    p = 3 if n >= 30 else 2 if n >= 10 else 1 if n >= 1 else 0
    nombres = [t.replace("Otros (especifique) ", "") for t in temas]
    return p, (f"{n} organizaciones ({'; '.join(nombres)})" if temas else "sin temática relacionada")


def solidez(f, ev):
    ids = [i for i in lista(f.evidencias) if i in ev.index]
    e = ev.loc[ids]
    buena = e.ambito.str.contains(AMBITO_LE) & e.precision.isin(["confiable", "conteo", "sin error publicado", "no aplica"])
    pct = round(100 * buena.mean()) if len(e) else 0
    return pct, ("alta" if pct >= 85 else "media" if pct >= 60 else "baja"), len(e)


def puntaje(fila, pesos):
    return round(100 * sum(pesos[c] * fila[f"{c}_puntaje"] for c in pesos) / (3 * sum(pesos.values())), 1)


def main():
    fichas = pd.read_csv(RES / "fichas_actividad.csv")
    seg = pd.read_csv(RES / "segmentos.csv").set_index("id")
    ev = pd.read_csv(RES / "evidencias.csv").set_index("id")
    oferta = pd.read_csv(RAIZ / "fuentes" / "capa3_registro_oferta.csv").set_index("id")
    renoj = pd.read_csv(RAIZ / "data" / "processed" / "capa1_renoj_organizaciones.csv")
    renoj = renoj[renoj.lima_este]
    mapa = pd.read_csv(RAIZ / "fuentes" / "modelo_aliados.csv").fillna("").set_index("ficha").temas_renoj.to_dict()

    filas = []
    for f in fichas.itertuples():
        if f.tipo_ficha in ("protocolo transversal", "población que requiere consulta directa"):
            continue
        r = {"ficha": f.id, "actividad": f.actividad, "linea": f.linea, "tipo_ficha": f.tipo_ficha}
        for clave, (p, dato) in {"necesidad": necesidad(f), "publico": publico(f, seg), "practica": practica(f),
                                 "convocatoria": convocatoria(f), "espacio": espacio(f, oferta),
                                 "aliados": aliados(f, renoj, mapa)}.items():
            r[f"{clave}_puntaje"], r[f"{clave}_dato"] = p, dato
        r["solidez_pct"], r["solidez_nivel"], r["n_evidencias"] = solidez(f, ev)
        filas.append(r)
    m = pd.DataFrame(filas)
    for clave, (_, pesos) in ESCENARIOS.items():
        m[f"puntaje_{clave}"] = m.apply(lambda x: puntaje(x, pesos), axis=1)
        m[f"puesto_{clave}"] = m[f"puntaje_{clave}"].rank(ascending=False, method="min").astype(int)
    puestos = m[[f"puesto_{c}" for c in ESCENARIOS]]
    m["puesto_min"], m["puesto_max"] = puestos.min(axis=1), puestos.max(axis=1)
    m["nivel"] = m.puntaje_recomendado.apply(lambda v: next(n for u, n in NIVELES if v >= u))
    niveles_esc = pd.DataFrame({c: m[f"puntaje_{c}"].apply(lambda v: next(n for u, n in NIVELES if v >= u))
                                for c in ESCENARIOS})
    m["nivel_estable"] = niveles_esc.nunique(axis=1) == 1
    m = m.sort_values(["puntaje_recomendado", "ficha"], ascending=[False, True])
    m.to_csv(RES / "modelo_actividades.csv", index=False)

    crit = pd.DataFrame([{"criterio": c, "nombre": n, "pregunta": q, "reglas": r, "fuente": s, "peso_recomendado": PESOS[c],
                          **{f"peso_{e}": ESCENARIOS[e][1][c] for e in ESCENARIOS if e != "recomendado"}}
                         for c, n, q, r, s in CRITERIOS])
    crit.to_csv(RES / "modelo_criterios.csv", index=False)

    cols = ["ficha", "actividad"] + [f"{c}_puntaje" for c in PESOS] + ["puntaje_recomendado", "puesto_min",
                                                                       "puesto_max", "nivel", "nivel_estable",
                                                                       "solidez_nivel"]
    print(m[cols].to_string(index=False))


if __name__ == "__main__":
    main()
