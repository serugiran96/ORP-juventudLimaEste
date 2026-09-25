"""Genera resultados/informe_final.md (segunda versión) a partir de las tablas de la integración.

Todo el contenido sale de resultados/*.csv (que genera integracion_construir.py). El resumen usa los mismos
marcadores {E-###} que el resto de la integración, así que el informe no tiene cifras escritas a mano. Las fichas se
presentan por línea temática: el informe no ordena las actividades por evidencia ni las califica.

Uso (desde la carpeta del proyecto, después de integracion_construir.py):
    python scripts/integracion_informe.py
"""
from pathlib import Path

import pandas as pd

import integracion_evidencias as IE
from integracion_construir import Render

PROY = Path(__file__).resolve().parent.parent
R = PROY / "resultados"
DISTRITOS = "Ate, Chaclacayo, El Agustino, La Molina, Lurigancho-Chosica, San Juan de Lurigancho y Santa Anita"

RESUMEN = [
    "**Cuántos son.** Dato Joven proyecta {E-001} jóvenes de 15 a 29 años en los siete distritos (2026); las encuestas "
    "del INEI estiman otros totales (entre {E-009} y {E-007}). Por eso las cantidades de este informe se dan con las "
    "dos bases y nunca como una cifra exacta.",
    "**Estudio y trabajo.** {E-043} de los jóvenes no estudia ni trabaja (definición del proyecto). Entre las mujeres "
    "de ese grupo, la situación más frecuente es dedicarse al hogar ({E-054}): son {E-070} de todas las mujeres "
    "jóvenes. {E-049} no tiene trabajo y busca o quiere trabajar, y {E-057} tiene un empleo informal (2022–2023).",
    "**Acceso a estudios superiores.** {E-023} de los jóvenes de 15–24 no estudia y su nivel máximo es secundaria "
    "completa; para un tercio de ellos el motivo principal es económico ({E-025}). No sabemos cuántos quieren "
    "continuar estudiando: ninguna fuente lo pregunta.",
    "**Qué hacen.** En el año, {E-110} fue al cine y {E-138} a algún espectáculo en vivo; {E-170} hizo deporte o "
    "ejercicio en la semana; {E-160} de los hombres juega videojuegos en línea. Lima Este va más que Lima "
    "Metropolitana a festivales locales ({E-130}) y bibliotecas ({E-140}), casi siempre gratis, y menos a conciertos "
    "({E-120}), casi siempre pagados.",
    "**Cuándo y con qué riesgo.** Las ventanas de tiempo libre son las noches de semana ({E-180}) y la tarde del "
    "domingo ({E-184}); de noche, {E-100} se siente inseguro caminando por su barrio ({E-101} de las mujeres) y "
    "{E-103} evitó salir de noche en el último año.",
    "**Convocatoria.** Casi nunca se puede observar: las cifras las declara quien organiza, sin cupos, y las cuatro "
    "señales de demanda son por ofertas concretas y gratuitas (una beca, unos talleres), que no se generalizan.",
]

LEYENDAS = {
    "Necesidad": [
        ("prevalencia", "Encuesta representativa que mide el problema en la población."),
        ("brecha de acceso", "Situación medida que limita el acceso a algo (por ejemplo, no estudia y solo tiene "
                             "secundaria completa)."),
        ("registro de atención", "Casos atendidos o registrados: dependen del acceso a servicios, no miden "
                                 "prevalencia."),
        ("situación documentada", "Situación medida que no es por sí misma una necesidad declarada."),
        ("objetivo institucional", "Lo que la organización quiere cambiar; no es una necesidad medida en los "
                                   "jóvenes."),
        ("sin evidencia", "Ninguna fuente mide una necesidad relacionada (lo esperable en cultura u ocio)."),
    ],
    "Interés o práctica": [
        ("P0", "Sin evidencia."),
        ("P1", "Práctica relacionada: dominio más amplio u otro formato."),
        ("P2", "Práctica de la misma actividad, en el mismo formato."),
        ("I1", "Interés declarado en el tema (solo Ipsos 2019–2022, fuera de Lima Este)."),
        ("I2", "Interés declarado en participar en la actividad propuesta: no existe en ninguna fuente."),
    ],
    "Convocatoria": [
        ("C0", "Sin evidencia: no se encontró actividad comparable con datos. No es evidencia negativa."),
        ("C1", "Solo oferta, sin información de participación."),
        ("C2", "Participación declarada sin cifra o con segmento o territorio solo parcialmente comparables."),
        ("C3", "Participación declarada con cifra, en segmento y territorio comparables."),
        ("C4", "Demanda observada (más interesados que cupos) en una oferta comparable; vale solo para esa oferta."),
        ("no aplica", "Protocolos y poblaciones que requieren consulta: no convocan."),
    ],
    "Alcance potencial": [
        ("amplia", "La evidencia se refiere a toda la juventud y la actividad no exige una condición particular."),
        ("segmento identificable", "La actividad es para una condición medible; se da su tamaño."),
        ("desconocido", "No hay denominador: alcance no estimable con la evidencia disponible."),
    ],
}
CAPAS = {1: "Capa 1 · contexto y necesidades", 2: "Capa 2 · intereses, hábitos y barreras",
         3: "Capa 3 · oferta y convocatoria"}


def cargar():
    t = {n: pd.read_csv(R / f"{n}.csv") for n in ["hallazgos_integrados", "patrones", "segmentos", "fichas_actividad",
                                                   "fichas_cadena", "fichas_componentes", "cambios_primera_version"]}
    rd = Render(IE.construir(), pd.read_csv(PROY / "fuentes" / "capa3_registro_oferta.csv"))
    t["resumen"] = [rd.texto(b, "resumen") for b in RESUMEN]
    f = t["fichas_actividad"]
    conteo = f.tipo_ficha.value_counts()
    t["resumen"].append(
        f"**Fichas de actividades.** {len(f)} fichas por actividad y segmento, presentadas por tema y sin puntaje: "
        f"{conteo.get('actividad de convocatoria abierta', 0)} actividades de convocatoria abierta, "
        f"{conteo.get('intervención segmentada', 0)} intervenciones segmentadas, "
        f"{conteo.get('protocolo transversal', 0)} protocolo transversal y "
        f"{conteo.get('población que requiere consulta directa', 0)} población que requiere consulta directa (mujeres "
        "jóvenes dedicadas al hogar). Ninguna tiene interés declarado en participar (I2): es la principal pregunta "
        "pendiente, y solo una consulta directa a jóvenes de Lima Este puede responderla.")
    return t


def md_tabla(filas, cab):
    s = "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n"
    return s + "".join("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in f) + " |\n"
                       for f in filas)


def informe(t):
    hall, pat, seg, fichas = t["hallazgos_integrados"], t["patrones"], t["segmentos"], t["fichas_actividad"]
    cadena, comp, cambios = t["fichas_cadena"], t["fichas_componentes"], t["cambios_primera_version"]
    out = [f"# Juventudes de Lima Este: evidencia para definir actividades\n",
           f"**Organización Rita Poma · Informe del análisis, segunda versión · 25 de septiembre de 2026**\n",
           f"Siete distritos: {DISTRITOS}. Jóvenes de 15 a 30 años (las fuentes llegan a 29). Periodo prioritario: "
           "2022–2026.\n",
           "Esta versión reemplaza a la del mismo día tras una auditoría metodológica (`fuentes/auditoria_integracion.md`). "
           "Los cambios están en la sección 8.\n", "## Resumen\n"]
    out += [f"- {b}" for b in t["resumen"]]

    out += ["\n## 1. Cómo leer este informe\n",
            "Cada ficha responde, por separado: qué necesidad existe, a quién aplica y cuántos son, qué práctica o "
            "interés se observó, qué oferta existe, qué evidencia hay de participación, qué barreras hay, qué no "
            "sabemos, qué podemos afirmar y qué es solo hipótesis. **Las dimensiones no se suman ni se comparan entre "
            "fichas**: una ficha con práctica de la misma actividad y sin datos de convocatoria no es mejor ni peor que "
            "otra con demanda observada y sin interés medido; responden a preguntas distintas.\n",
            "**Ámbito.** Lima Este (siete distritos juntos, estimación propia con encuestas del INEI; nunca por "
            "distrito), Lima Metropolitana (contexto), Perú urbano (estudios de mercado antiguos) y distrito (registros "
            "administrativos). Las cifras con precisión limitada llevan la marca *(referencial)*; las no publicables no "
            "se citan.\n",
            "**Cantidades.** Se dan dos estimaciones que no se combinan: el porcentaje aplicado a la población 2026 de "
            "Dato Joven, y el total que estima la propia encuesta. Difieren porque las encuestas no se calibran por "
            "distrito y la proyección de Dato Joven es inestable por edad.\n"]
    for nombre, filas in LEYENDAS.items():
        out.append(f"**{nombre}**\n")
        out.append(md_tabla(filas, ["Código", "Significado"]))

    out.append("\n## 2. Lo que sabemos, capa por capa\n")
    for c, titulo in CAPAS.items():
        out.append(f"### {titulo}\n")
        for r in hall[hall.capa == c].itertuples():
            out.append(f"- **{r.id}.** {r.enunciado}  \n  *{r.geografia} · {r.periodo} · {r.precision}. No permite "
                       f"afirmar: {r.no_permite}*")
        out.append("")

    out.append("## 3. Patrones, brechas y condiciones transversales\n")
    out.append("Cada patrón separa el dato observado, su interpretación y lo que no permite afirmar.\n")
    for r in pat.itertuples():
        out.append(f"**{r.id} · {r.tema}** ({r.tipo})\n")
        out.append(f"- *Dato observado:* {r.dato_observado}\n- *Interpretación:* {r.interpretacion}\n"
                   f"- *No permite afirmar:* {r.no_permite_afirmar}\n- *Hallazgos:* {r.hallazgos}\n")

    out.append("## 4. Segmentos: a quién aplica y cuántos son\n")
    out.append(md_tabla([(r.id, r.segmento, r.texto, r.periodo, r.fichas) for r in seg.itertuples()],
                        ["ID", "Segmento", "Tamaño", "Periodo", "Fichas"]))

    out.append("\n## 5. Mapa de la evidencia\n")
    out.append("Una fila por ficha, en orden temático. **No es un ranking:** cada columna se lee por separado.\n")
    out.append(md_tabla([(r.id, r.actividad, r.tipo_ficha, r.necesidad_tipo, r.interes_codigo, r.alcance_tipo,
                          r.convocatoria_codigo) for r in fichas.itertuples()],
                        ["Ficha", "Actividad", "Tipo", "Necesidad", "Interés o práctica", "Alcance", "Convocatoria"]))

    out.append("\n## 6. Fichas de actividades\n")
    for linea, grupo in fichas.groupby("linea", sort=False):
        out.append(f"### {linea}\n")
        for f in grupo.itertuples():
            out.append(f"#### {f.id}. {f.actividad}\n")
            out.append(f"*{f.tipo_ficha.capitalize()} · primera versión: {f.origen_v1} · resultado de la auditoría: "
                       f"{f.resultado_auditoria}*\n")
            pasos = cadena[cadena.ficha == f.id].sort_values("orden")
            out.append(md_tabla([(f"{p.orden}. {p.paso}", p.codigo if isinstance(p.codigo, str) else "", p.texto)
                                 for p in pasos.itertuples()], ["Paso", "Código", "Evidencia"]))
            cf = comp[comp.ficha == f.id]
            out.append("\n**Componentes**\n")
            out.append(md_tabla([(c.componente, c.estado, c.nota if isinstance(c.nota, str) else "")
                                 for c in cf.itertuples()], ["Componente", "Estado", "Nota"]))
            out.append(f"\n- **Cómo validarla en un piloto:** {f.validacion_piloto}\n- **Dónde (criterio operativo, no "
                       f"de demanda):** {f.donde}\n- **Cambio frente a la primera versión:** {f.cambio_v1}\n"
                       f"- **Trazabilidad:** evidencias {f.evidencias}; actividades de la Capa 3 "
                       f"{f.actividades_c3 if isinstance(f.actividades_c3, str) else '—'}.\n")

    out.append("## 7. Qué no sabemos y cómo averiguarlo\n")
    out += ["- **Interés en participar en actividades concretas (I2):** ninguna fuente lo pregunta a los jóvenes de "
            "Lima Este.",
            "- **Horarios preferidos, distancia aceptable y disposición a pagar:** solo hay disponibilidad observada y "
            "desplazamiento de quienes estudian.",
            "- **Intención de continuar estudios** y cuántos ya se preparan en academias.",
            "- **Salud mental e inseguridad por distrito**; salud mental en Lima Este.",
            "- **Convocatoria real de la oferta existente:** las cifras son declaradas y casi nunca informan cupos.\n",
            "**Cómo averiguarlo:**\n",
            "1. **Consulta directa a jóvenes de Lima Este**, que incluya a las mujeres dedicadas al hogar en sus hogares "
            "o espacios comunitarios: qué actividades y formatos harían, horarios, distancia, cuidado infantil, costo, "
            "canales, intención de estudiar y seguridad para salir de noche.",
            "2. **Registros administrativos de convocatoria** (solicitudes de acceso a la información pública a "
            "municipalidades, SENAJU e IPD): inscritos, asistentes, cupos y listas de espera por edad y sexo.",
            "3. **Pilotos pequeños** con los indicadores de cada ficha, definidos antes de empezar. Los umbrales los "
            "decide el equipo; no salen de los datos.\n"]

    out.append("## 8. Cambios respecto de la primera versión\n")
    out.append(md_tabla([(r.v1, r.v1_nombre, r.resultado, r.fichas_v2, r.cambio) for r in cambios.itertuples()],
                        ["Primera versión", "Propuesta", "Resultado", "Fichas", "Cambio"]))
    out.append("\nLos niveles alto/medio/bajo se reemplazaron por categorías descriptivas con reglas escritas. Se "
               "corrigieron errores de la primera versión: los motivos para no estudiar eran de 15–24 años (no de "
               "15–29), las temáticas del RENOJ ocultaban organizaciones de ciudadanía y tecnología, y varias "
               "prácticas relacionadas figuraban como interés 'alto'. El detalle está en la columna `cambio_v2` de "
               "`resultados/hallazgos_integrados.csv`.\n")

    out.append("## 9. Fuentes y método\n")
    out.append("Dato Joven (Observatorio Nacional de Juventud); microdatos del INEI procesados por el proyecto: ENAHO "
               "2022–2025 (Módulos 02, 03 y 05), ENAPRES 2022–2025 (capítulos de cultura y de seguridad ciudadana) y "
               "ENUT 2024; estudios de Ipsos 2019–2022; notas de prensa de las siete municipalidades y de entidades "
               "públicas (2024–2026). Método, reglas, categorías y validaciones: `fuentes/metodologia_integracion.md`. "
               "Cada cifra remite a `resultados/evidencias.csv` y, desde ahí, al archivo de datos que la produjo.\n")
    return "\n".join(out)


if __name__ == "__main__":
    texto = informe(cargar())
    (R / "informe_final.md").write_text(texto)
    print(f"resultados/informe_final.md: {len(texto.splitlines())} líneas")
