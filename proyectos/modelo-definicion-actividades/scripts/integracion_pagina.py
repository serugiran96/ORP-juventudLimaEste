"""Genera resultados/informe_final.html, la versión web del informe (segunda versión).

Usa las mismas tablas y el mismo resumen que scripts/integracion_informe.py, así que la página no se aparta del
informe en Markdown ni tiene cifras escritas a mano. Las fichas se presentan por línea temática y los códigos se
muestran con un estilo neutro: la página no ordena ni califica las actividades. El archivo no incluye las etiquetas
<html> ni <head> porque la plataforma de publicación las agrega.

Uso (desde la carpeta del proyecto, después de integracion_informe.py):
    python scripts/integracion_pagina.py
"""
import html
import re
from pathlib import Path

from integracion_informe import CAPAS, DISTRITOS, LEYENDAS, cargar

PROY = Path(__file__).resolve().parent.parent
SALIDA = PROY / "resultados" / "informe_final.html"
e = html.escape
REF = re.compile(r"\b(H[123]-\d{2}|PT-\d{2}|F-\d{2}|S-\d{2})\b")


def enlazar(texto):
    return REF.sub(lambda m: f'<a class="code" href="#{m.group(1)}">{m.group(1)}</a>', e(str(texto)))


def negritas(texto):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(texto))


def chip(codigo):
    return f'<span class="chip">{e(str(codigo))}</span>' if isinstance(codigo, str) and codigo else ""


def pagina(t):
    hall, pat, seg, fichas = t["hallazgos_integrados"], t["patrones"], t["segmentos"], t["fichas_actividad"]
    cadena, comp, cambios = t["fichas_cadena"], t["fichas_componentes"], t["cambios_primera_version"]

    resumen = "".join(f"<li>{negritas(b)}</li>" for b in t["resumen"])
    leyendas = "".join(
        f'<div class="leg"><h3>{e(n)}</h3><dl>' + "".join(f"<dt>{chip(c)}</dt><dd>{e(s)}</dd>" for c, s in filas)
        + "</dl></div>" for n, filas in LEYENDAS.items())
    mapa = "".join(
        f'<tr><th scope="row"><a href="#{r.id}"><span class="pid">{r.id}</span> {e(r.actividad)}</a></th>'
        f"<td>{e(r.tipo_ficha)}</td><td>{e(r.necesidad_tipo)}</td><td>{chip(r.interes_codigo)}</td>"
        f"<td>{e(r.alcance_tipo)}</td><td>{chip(r.convocatoria_codigo)}</td></tr>" for r in fichas.itertuples())

    bloques = []
    for linea, grupo in fichas.groupby("linea", sort=False):
        arts = []
        for f in grupo.itertuples():
            pasos = cadena[cadena.ficha == f.id].sort_values("orden")
            dl = "".join(
                f'<div class="kv{" hyp" if p.orden == 10 else ""}{" ok" if p.orden == 9 else ""}"><dt>{p.orden}. '
                f'{e(p.paso)} {chip(p.codigo if isinstance(p.codigo, str) else "")}</dt><dd>{e(p.texto)}</dd></div>'
                for p in pasos.itertuples())
            comps = "".join(f"<tr><td>{e(c.componente)}</td><td>{e(c.estado)}</td>"
                            f"<td>{e(c.nota) if isinstance(c.nota, str) else ''}</td></tr>"
                            for c in comp[comp.ficha == f.id].itertuples())
            arts.append(f"""<article class="prop" id="{f.id}">
  <header><span class="pid">{f.id}</span><h4>{e(f.actividad)}</h4></header>
  <p class="meta">{e(f.tipo_ficha)} · primera versión: {e(f.origen_v1)} · auditoría: {e(f.resultado_auditoria)}</p>
  <dl>{dl}</dl>
  <div class="tbl"><table class="comp"><thead><tr><th>Componente</th><th>Estado</th><th>Nota</th></tr></thead>
  <tbody>{comps}</tbody></table></div>
  <details><summary>Piloto, dónde y trazabilidad</summary><div class="trace">
    <p><strong>Cómo validarla:</strong> {e(f.validacion_piloto)}</p>
    <p><strong>Dónde (criterio operativo, no de demanda):</strong> {e(f.donde)}</p>
    <p><strong>Cambio frente a la primera versión:</strong> {e(f.cambio_v1)}</p>
    <p class="ref">Evidencias: {e(f.evidencias)} · Capa 3: {e(f.actividades_c3) if isinstance(f.actividades_c3, str) else '—'}</p>
  </div></details>
</article>""")
        bloques.append(f'<section class="grupo"><h3>{e(linea)}</h3>{"".join(arts)}</section>')

    patrones = "".join(
        f"""<li id="{r.id}"><div class="pat-head"><span class="code-static">{r.id}</span><span class="tag">{e(r.tipo)}</span>
<strong>{e(r.tema)}</strong></div><p><span class="lbl">Dato observado</span> {e(r.dato_observado)}</p>
<p><span class="lbl">Interpretación</span> {e(r.interpretacion)}</p>
<p class="caut"><span class="lbl">No permite afirmar</span> {e(r.no_permite_afirmar)}</p>
<p class="refs">{enlazar(r.hallazgos)}</p></li>""" for r in pat.itertuples())
    segmentos = "".join(f'<tr id="{r.id}"><td class="pid">{r.id}</td><td>{e(r.segmento)}</td><td>{e(r.texto)}</td>'
                        f"<td>{e(str(r.periodo))}</td><td>{enlazar(r.fichas)}</td></tr>" for r in seg.itertuples())
    catalogo = "".join(
        f'<section class="cat"><h3>{CAPAS[c]}</h3><ol class="hlist">' + "".join(
            f'<li id="{r.id}"><span class="code-static">{r.id}</span><div><p>{e(r.enunciado)}</p>'
            f'<p class="meta">{e(r.geografia)} · {e(str(r.periodo))} · {e(r.precision)} · {e(r.estado_v2)}</p>'
            f'<p class="meta"><span>No permite afirmar:</span> {e(r.no_permite)}</p></div></li>'
            for r in hall[hall.capa == c].itertuples()) + "</ol></section>" for c in CAPAS)
    tabla_cambios = "".join(f"<tr><td class=\"pid\">{e(r.v1)}</td><td>{e(r.v1_nombre)}</td><td>{e(r.resultado)}</td>"
                            f"<td>{enlazar(r.fichas_v2)}</td><td>{e(r.cambio)}</td></tr>" for r in cambios.itertuples())
    distritos = "".join(f"<span>{d.strip()}</span>" for d in DISTRITOS.replace(" y ", ", ").split(","))

    return f"""<title>Juventudes de Lima Este</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="masthead">
  <p class="eyebrow">Análisis para la Organización Rita Poma · segunda versión · 25 de septiembre de 2026</p>
  <h1>Juventudes de Lima Este</h1>
  <p class="dek">Qué evidencia existe para cada tipo de actividad: a qué jóvenes aplica, cuántos son, qué hacen, qué participación se ha observado, qué barreras hay y qué falta validar. Sin ranking: cada dimensión se lee por separado.</p>
  <div class="districts">{distritos}</div>
</header>

<section class="block"><h2 id="resumen">Resumen</h2><ul class="summary">{resumen}</ul></section>

<section class="block"><h2 id="leer">Cómo leer este informe</h2>
<p class="lead">Cada cifra remite a <span class="ref">resultados/evidencias.csv</span> y al archivo de datos que la produjo. Las cifras con precisión limitada llevan la marca <em>(referencial)</em>; las no publicables no se citan. Las cantidades de personas se dan con dos bases que no se combinan: la población 2026 de Dato Joven y el total que estima la propia encuesta.</p>
<div class="legends">{leyendas}</div></section>

<section class="block"><h2 id="mapa">Mapa de la evidencia</h2>
<p class="lead">Una fila por ficha, en orden temático. <strong>No es un ranking:</strong> las columnas no se suman ni se comparan entre filas.</p>
<div class="matrix tbl"><table><thead><tr><th>Ficha</th><th>Tipo</th><th>Necesidad</th><th>Interés o práctica</th><th>Alcance</th><th>Convocatoria</th></tr></thead><tbody>{mapa}</tbody></table></div></section>

<section class="block"><h2 id="fichas">Fichas de actividades</h2>
<p class="lead">Cada ficha sigue la misma cadena: necesidad → población → interés o práctica → alcance → oferta → participación → barreras → vacíos → qué podemos afirmar → qué es hipótesis. Los componentes que no tienen evidencia se separan de los que sí.</p>
{''.join(bloques)}</section>

<section class="block"><h2 id="segmentos">Segmentos: a quién aplica y cuántos son</h2>
<div class="tbl"><table><thead><tr><th>ID</th><th>Segmento</th><th>Tamaño</th><th>Periodo</th><th>Fichas</th></tr></thead><tbody>{segmentos}</tbody></table></div></section>

<section class="block"><h2 id="patrones">Patrones, brechas y condiciones transversales</h2><ol class="pats">{patrones}</ol></section>

<section class="block"><h2 id="pendiente">Qué no sabemos y cómo averiguarlo</h2>
<ul class="limits">
<li><strong>Interés en participar en actividades concretas:</strong> ninguna fuente lo pregunta a los jóvenes de Lima Este.</li>
<li><strong>Horarios preferidos, distancia aceptable y disposición a pagar:</strong> solo hay disponibilidad observada y desplazamiento de quienes estudian.</li>
<li><strong>Intención de continuar estudios</strong> y cuántos ya se preparan en academias.</li>
<li><strong>Salud mental e inseguridad por distrito</strong>; salud mental en Lima Este.</li>
<li><strong>Convocatoria real de la oferta existente:</strong> las cifras son declaradas y casi nunca informan cupos.</li>
</ul>
<ol class="steps">
<li><strong>Consulta directa a jóvenes de Lima Este</strong>, que incluya a las mujeres dedicadas al hogar en sus hogares o espacios comunitarios.</li>
<li><strong>Registros administrativos de convocatoria</strong> (acceso a la información pública): inscritos, asistentes, cupos y listas de espera por edad y sexo.</li>
<li><strong>Pilotos pequeños</strong> con los indicadores de cada ficha, definidos antes de empezar.</li>
</ol></section>

<section class="block"><h2 id="cambios">Cambios respecto de la primera versión</h2>
<p class="lead">Los niveles alto/medio/bajo se reemplazaron por categorías descriptivas con reglas escritas, y se corrigieron errores detectados en una auditoría metodológica.</p>
<div class="tbl"><table><thead><tr><th>V1</th><th>Propuesta</th><th>Resultado</th><th>Fichas</th><th>Cambio</th></tr></thead><tbody>{tabla_cambios}</tbody></table></div></section>

<section class="block"><h2 id="catalogo">Catálogo de hallazgos</h2>{catalogo}</section>

<footer>Fuentes: Dato Joven (Observatorio Nacional de Juventud); ENAHO, ENAPRES y ENUT (INEI), procesadas por el proyecto; Ipsos; notas de prensa de las siete municipalidades y de entidades públicas. Método: <span class="ref">fuentes/metodologia_integracion.md</span>.</footer>
</div>
"""


CSS = """
:root{
  --bg:#f4f6f8; --surface:#ffffff; --ink:#141a22; --ink-2:#4b5566; --ink-3:#6b7485; --line:#dde2e9; --line-2:#c8cfd9;
  --accent:#2a78d6; --accent-ink:#1c5aa6; --chip:#eceff3; --chip-ink:#2b3442; --hyp:#fff6e5; --hyp-line:#e3b865;
  --ok:#eaf4ef; --ok-line:#5f9e84;
  --display:"Archivo","Arial Narrow",Arial,sans-serif; --body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#101318; --surface:#171b22; --ink:#e7ebf1; --ink-2:#aeb6c4; --ink-3:#8b94a4; --line:#262c36; --line-2:#343c48;
    --accent:#5c9ce8; --accent-ink:#8cbaf2; --chip:#232a34; --chip-ink:#d6dde8; --hyp:#2a2415; --hyp-line:#8a6d2f;
    --ok:#15241e; --ok-line:#4f8a72;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#101318; --surface:#171b22; --ink:#e7ebf1; --ink-2:#aeb6c4; --ink-3:#8b94a4; --line:#262c36; --line-2:#343c48;
  --accent:#5c9ce8; --accent-ink:#8cbaf2; --chip:#232a34; --chip-ink:#d6dde8; --hyp:#2a2415; --hyp-line:#8a6d2f;
  --ok:#15241e; --ok-line:#4f8a72;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.6;padding-inline:20px;padding-block:0 64px}
.wrap{max-width:920px;margin:0 auto}
a{color:var(--accent-ink)}
a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
h1,h2,h3,h4{font-family:var(--display);font-stretch:88%;line-height:1.15;text-wrap:balance;margin:0}
h2{font-size:1.75rem;font-weight:700;margin-block:0 16px}
h3{font-size:1.2rem;font-weight:700}
h4{font-size:1.1rem;font-weight:700}
p{margin:0}
.code,.code-static{font-family:var(--mono);font-size:.78em;font-weight:500}
.code{text-decoration:none;background:var(--chip);color:var(--ink-2);padding:1px 5px;border-radius:4px;white-space:nowrap}
.code-static{color:var(--ink-3)}
.chip{display:inline-block;font-family:var(--mono);font-size:.76rem;font-weight:500;background:var(--chip);color:var(--chip-ink);border:1px solid var(--line-2);border-radius:5px;padding:0 6px;white-space:nowrap}
section.block{padding-block:48px 8px;border-top:1px solid var(--line)}
section.block>*+*{margin-top:16px}
.lead{max-width:70ch;color:var(--ink-2)}
.ref{font-family:var(--mono);font-size:.8em}
.masthead{padding-block:56px 32px;display:grid;gap:16px}
.eyebrow{font-family:var(--mono);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.masthead h1{font-size:clamp(2.4rem,7vw,4rem);font-weight:800;letter-spacing:-.01em}
.dek{font-size:1.1rem;color:var(--ink-2);max-width:64ch}
.districts{display:flex;flex-wrap:wrap;gap:6px}
.districts span{font-size:.8rem;border:1px solid var(--line-2);border-radius:999px;padding:2px 10px;color:var(--ink-2)}
.summary{list-style:none;margin:0;padding:0;display:grid;gap:12px;max-width:74ch}
.summary li{padding-left:18px;position:relative}
.summary li::before{content:"";position:absolute;left:0;top:.7em;width:8px;height:2px;background:var(--accent)}
.legends{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.leg{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.leg h3{font-size:1rem;margin-bottom:8px}
.leg dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 10px;font-size:.88rem}
.leg dd{margin:0;color:var(--ink-2)}
.tbl{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
thead th{font-family:var(--mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:500}
.matrix{background:var(--surface);border:1px solid var(--line);border-radius:10px}
.matrix table{min-width:720px}
.matrix th[scope=row] a{color:var(--ink);text-decoration:none;font-weight:500}
.pid{font-family:var(--mono);font-size:.78rem;color:var(--ink-3)}
.grupo{display:grid;gap:14px;margin-top:28px}
.prop{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px;display:grid;gap:12px;scroll-margin-top:16px}
.prop header{display:flex;gap:8px;align-items:baseline}
.prop dl{margin:0;display:grid;gap:8px}
.kv{display:grid;grid-template-columns:220px 1fr;gap:12px;font-size:.93rem;padding:6px 0;border-top:1px solid var(--line)}
.kv dt{font-weight:600}
.kv dd{margin:0;color:var(--ink-2)}
.kv.hyp{background:var(--hyp);border-left:3px solid var(--hyp-line);padding:8px 10px;border-radius:0 6px 6px 0}
.kv.ok{background:var(--ok);border-left:3px solid var(--ok-line);padding:8px 10px;border-radius:0 6px 6px 0}
.comp{font-size:.85rem}
.meta{font-size:.8rem;color:var(--ink-3)}
.meta span{font-weight:600}
details summary{cursor:pointer;font-weight:600;font-size:.9rem;color:var(--accent-ink)}
.trace{display:grid;gap:6px;margin-top:10px;font-size:.9rem;color:var(--ink-2)}
.pats{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.pats li{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;scroll-margin-top:16px;font-size:.93rem}
.pat-head{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tag{font-size:.72rem;border:1px solid var(--line-2);border-radius:999px;padding:0 8px;color:var(--ink-2)}
.lbl{font-family:var(--mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin-right:4px}
.caut{color:var(--ink-2)}
.refs{display:flex;flex-wrap:wrap;gap:4px}
.limits,.steps{margin:0;padding-left:20px;display:grid;gap:8px;max-width:74ch;color:var(--ink-2)}
.cat{margin-top:24px}
.hlist{list-style:none;margin:12px 0 0;padding:0}
.hlist li{display:grid;grid-template-columns:64px 1fr;gap:10px;padding-block:12px;border-top:1px solid var(--line);scroll-margin-top:16px}
.hlist li:target{background:var(--chip);border-radius:6px}
.hlist p{font-size:.93rem}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:.85rem;color:var(--ink-3)}
@media (max-width:760px){
  .legends{grid-template-columns:1fr}
  .kv{grid-template-columns:1fr;gap:2px}
  body{padding-inline:16px}
}
"""

if __name__ == "__main__":
    contenido = pagina(cargar())
    SALIDA.write_text(contenido)
    print(f"resultados/informe_final.html: {len(contenido) // 1024} KB")
