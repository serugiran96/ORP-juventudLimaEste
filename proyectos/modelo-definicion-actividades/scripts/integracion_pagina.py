"""Genera resultados/informe_final.html, la versión web del informe final, a partir de las tablas del cruce.

Usa las mismas tablas que scripts/integracion_informe.py (hallazgos, patrones y propuestas), así que la página no
se aparta del informe en Markdown. Es el contenido de la página publicada para compartir con el equipo; el archivo
no incluye la etiqueta <html> ni <head> porque la plataforma de publicación las agrega.

Uso (desde la carpeta del proyecto):
    python scripts/integracion_pagina.py
"""
import html
import re
from pathlib import Path

import pandas as pd

PROY = Path(__file__).resolve().parent.parent
R = PROY / "resultados"
SALIDA = PROY / "resultados" / "informe_final.html"
hall = pd.read_csv(R / "hallazgos_integrados.csv")
pat = pd.read_csv(R / "patrones.csv")
prop = pd.read_csv(R / "propuestas.csv").fillna("").set_index("id")
H = hall.set_index("id")

e = html.escape
CODIGO = re.compile(r"\b(H[123]-\d{2}|PT-\d{2})\b")


def enlazar(texto):
    """Escapa el texto y convierte los códigos de hallazgo en enlaces al catálogo."""
    return CODIGO.sub(lambda m: f'<a class="code" href="#{m.group(1)}">{m.group(1)}</a>', e(texto))


NIVELES = ["sin evidencia", "bajo", "medio", "alto"]
GRUPOS = [
    ("A", "Con respaldo en las tres dimensiones", "Necesidad documentada, práctica o interés relacionados y participación declarada con cifras en actividades similares en Lima Este. Son las apuestas más sólidas, aunque su convocatoria no está demostrada.", ["P01", "P02"]),
    ("B", "Práctica alta en Lima Este, convocatoria por medir", "Lo que los jóvenes ya hacen, medido con precisión en Lima Este, sin evidencia local de que una actividad organizada los convoque. Son las mejores candidatas para pilotos que midan la convocatoria.", ["P04", "P05", "P06"]),
    ("C", "Evidencia parcial", "Sustento en alguna dimensión, pero descansan sobre todo en hipótesis. Conviene validarlas antes de invertir.", ["P03", "P08", "P10", "P09", "P07"]),
    ("D", "Componente transversal", "Necesidad documentada sin evidencia de interés: se integra en otras actividades, no como actividad independiente.", ["P11"]),
]
ORDEN = [pid for *_, ids in GRUPOS for pid in ids]


def nivel(v):
    return f'<span class="lvl l{NIVELES.index(v)}">{e(v)}</span>'


# ---------------------------------------------------------------- matriz
filas_matriz = "\n".join(
    f"""<tr><th scope="row"><a href="#{pid}"><span class="pid">{pid}</span> {e(prop.loc[pid, 'propuesta'])}</a></th>
<td>{nivel(prop.loc[pid, 'nivel_necesidad'])}</td><td>{nivel(prop.loc[pid, 'nivel_interes'])}</td><td>{nivel(prop.loc[pid, 'nivel_convocatoria'])}</td></tr>"""
    for pid in ORDEN)


# ---------------------------------------------------------------- fichas
def lista_h(celda):
    ids = [x.strip() for x in celda.split(";") if x.strip()]
    if not ids:
        return '<p class="muted">Ninguna fuente mide este aspecto.</p>'
    return "<ul>" + "".join(
        f'<li><a class="code" href="#{i}">{i}</a> <span class="ev">{e(H.loc[i, "tipo_evidencia"])} · {e(H.loc[i, "geografia"])}</span><br>{e(H.loc[i, "enunciado"])}</li>'
        for i in ids) + "</ul>"


def ficha(pid):
    p = prop.loc[pid]
    campos = [("Para quién", p.segmento), ("Por qué", p.sustento), ("Barreras relevantes", p.barreras),
              ("Qué sabemos de su convocatoria", p.convocatoria),
              ("Qué sigue siendo hipótesis", p.hipotesis), ("Cómo validarla", p.validacion),
              ("Dónde podría pilotearse", p.donde), ("Cautelas", p.cautelas)]
    dl = "".join(f'<div class="kv{" hyp" if k.startswith("Qué sigue") else ""}"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in campos)
    return f"""<article class="prop" id="{pid}">
  <header><span class="pid">{pid}</span><h4>{e(p.propuesta)}</h4></header>
  <p class="desc">{e(p.descripcion)}</p>
  <div class="levels" aria-label="Nivel de evidencia">
    <span><small>Necesidad</small>{nivel(p.nivel_necesidad)}</span>
    <span><small>Interés o práctica</small>{nivel(p.nivel_interes)}</span>
    <span><small>Convocatoria</small>{nivel(p.nivel_convocatoria)}</span>
  </div>
  <dl>{dl}</dl>
  <details><summary>Hallazgos que la sustentan</summary>
    <div class="trace">
      <h5>Capa 1 · necesidades</h5>{lista_h(p.hallazgos_c1)}
      <h5>Capa 2 · intereses y hábitos</h5>{lista_h(p.hallazgos_c2)}
      <h5>Capa 3 · oferta y convocatoria</h5>{lista_h(p.hallazgos_c3)}
    </div>
  </details>
</article>"""


bloques = "\n".join(
    f"""<section class="grupo" aria-labelledby="g{letra}"><div class="grupo-head"><span class="glyph">{letra}</span><div><h3 id="g{letra}">{e(t)}</h3><p>{e(d)}</p></div></div>
{''.join(ficha(pid) for pid in ids)}</section>"""
    for letra, t, d, ids in GRUPOS)

# ---------------------------------------------------------------- patrones
TIPO_CLASE = {"patrón": "t-pat", "brecha": "t-bre", "condición de diseño": "t-dis"}
patrones = "\n".join(
    f"""<li id="{r.id}"><div class="pat-head"><span class="code-static">{r.id}</span><span class="chip {TIPO_CLASE[r.tipo]}">{e(r.tipo)}</span><strong>{e(r.tema)}</strong></div>
<p>{e(r.enunciado)}</p><p class="caut"><span>Cautela</span> {e(r.cautela)}</p>
<p class="refs">{' '.join(f'<a class="code" href="#{x.strip()}">{x.strip()}</a>' for x in r.hallazgos.split(';'))}</p></li>"""
    for r in pat.itertuples())

# ---------------------------------------------------------------- catálogo
CAPAS = {1: "Capa 1 · contexto y necesidades", 2: "Capa 2 · intereses, hábitos y aspiraciones", 3: "Capa 3 · oferta y convocatoria"}
catalogo = "\n".join(
    f"""<section class="cat" aria-labelledby="cat{c}"><h3 id="cat{c}">{CAPAS[c]}</h3><ol class="hlist">"""
    + "".join(
        f"""<li id="{r.id}"><span class="code-static">{r.id}</span><div><p>{e(r.enunciado)}</p>
<p class="meta">{e(r.tipo_evidencia)} · {e(r.poblacion)} · {e(r.geografia)} · {e(r.periodo)} · {e(r.precision)}</p>
<p class="meta"><span>No permite afirmar:</span> {e(r.no_permite)}</p>
<p class="meta ref">{e(r.referencia)}</p></div></li>"""
        for r in hall[hall.capa == c].itertuples())
    + "</ol></section>"
    for c in (1, 2, 3))

CSS = """
:root{
  --bg:#f4f6f8; --surface:#ffffff; --ink:#141a22; --ink-2:#4b5566; --ink-3:#6b7485; --line:#dde2e9; --line-2:#c8cfd9;
  --accent:#2a78d6; --accent-ink:#1c5aa6; --l0:#eceff3; --l1:#cddff5; --l2:#86b4ec; --l3:#2a78d6;
  --l0-ink:#4b5566; --l1-ink:#1d3350; --l2-ink:#0f2440; --l3-ink:#ffffff;
  --pat:#2a78d6; --bre:#b8562a; --dis:#3f7f6b; --hyp:#fff6e5; --hyp-line:#e3b865;
  --display:"Archivo","Arial Narrow",Arial,sans-serif; --body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#101318; --surface:#171b22; --ink:#e7ebf1; --ink-2:#aeb6c4; --ink-3:#8b94a4; --line:#262c36; --line-2:#343c48;
    --accent:#5c9ce8; --accent-ink:#8cbaf2; --l0:#20252e; --l1:#223a58; --l2:#2f5c96; --l3:#4a8ce0;
    --l0-ink:#aeb6c4; --l1-ink:#d6e5f8; --l2-ink:#eef4fc; --l3-ink:#0b1320;
    --pat:#5c9ce8; --bre:#e08a5e; --dis:#6fb79e; --hyp:#2a2415; --hyp-line:#8a6d2f;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#101318; --surface:#171b22; --ink:#e7ebf1; --ink-2:#aeb6c4; --ink-3:#8b94a4; --line:#262c36; --line-2:#343c48;
  --accent:#5c9ce8; --accent-ink:#8cbaf2; --l0:#20252e; --l1:#223a58; --l2:#2f5c96; --l3:#4a8ce0;
  --l0-ink:#aeb6c4; --l1-ink:#d6e5f8; --l2-ink:#eef4fc; --l3-ink:#0b1320;
  --pat:#5c9ce8; --bre:#e08a5e; --dis:#6fb79e; --hyp:#2a2415; --hyp-line:#8a6d2f;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.6;padding-inline:20px;padding-block:0 64px}
.wrap{max-width:900px;margin:0 auto}
a{color:var(--accent-ink)}
a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
h1,h2,h3,h4{font-family:var(--display);font-stretch:88%;line-height:1.15;text-wrap:balance;margin:0}
h2{font-size:1.75rem;font-weight:700;margin-block:0 16px}
h3{font-size:1.2rem;font-weight:700}
h4{font-size:1.1rem;font-weight:700}
p{margin:0}
.muted{color:var(--ink-3)}
.code,.code-static{font-family:var(--mono);font-size:.78em;font-weight:500;letter-spacing:.01em}
.code{text-decoration:none;background:var(--l0);color:var(--ink-2);padding:1px 5px;border-radius:4px;white-space:nowrap}
.code:hover{background:var(--l1);color:var(--l1-ink)}
.code-static{color:var(--ink-3)}
section.block{padding-block:48px 8px;border-top:1px solid var(--line)}
section.block>*+*{margin-top:16px}
.lead{max-width:68ch;color:var(--ink-2)}

/* cabecera */
.masthead{padding-block:56px 32px;display:grid;gap:16px}
.eyebrow{font-family:var(--mono);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.masthead h1{font-size:clamp(2.4rem,7vw,4rem);font-weight:800;letter-spacing:-.01em}
.dek{font-size:1.15rem;color:var(--ink-2);max-width:62ch}
.districts{display:flex;flex-wrap:wrap;gap:6px}
.districts span{font-size:.8rem;border:1px solid var(--line-2);border-radius:999px;padding:2px 10px;color:var(--ink-2)}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:8px}
.facts div{background:var(--surface);padding:14px 16px;display:grid;gap:2px}
.facts b{font-family:var(--display);font-stretch:88%;font-size:1.7rem;font-variant-numeric:tabular-nums}
.facts span{font-size:.85rem;color:var(--ink-2);line-height:1.35}

/* resumen */
.summary{list-style:none;margin:0;padding:0;display:grid;gap:12px;max-width:72ch}
.summary li{padding-left:18px;position:relative}
.summary li::before{content:"";position:absolute;left:0;top:.7em;width:8px;height:2px;background:var(--accent)}
.rules{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.rules div{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.93rem}
.rules b{display:block;font-family:var(--display);font-stretch:88%;font-size:1rem;margin-bottom:2px}
.tbl{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;vertical-align:top;padding:9px 10px;border-bottom:1px solid var(--line)}
thead th{font-family:var(--mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:500}

/* capas */
.layers{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.layer{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;display:grid;gap:10px;align-content:start}
.layer h3{font-size:1.05rem}
.layer .q{font-size:.85rem;color:var(--ink-3)}
.layer ul{margin:0;padding-left:18px;display:grid;gap:8px;font-size:.92rem}

/* matriz */
.matrix{background:var(--surface);border:1px solid var(--line);border-radius:10px}
.matrix table{min-width:620px}
.matrix th[scope=row] a{color:var(--ink);text-decoration:none;font-weight:500}
.matrix th[scope=row] a:hover{text-decoration:underline}
.matrix td{width:118px;text-align:center}
.matrix tbody tr:last-child>*{border-bottom:0}
.pid{font-family:var(--mono);font-size:.78rem;color:var(--ink-3);margin-right:4px}
.lvl{display:inline-block;min-width:92px;text-align:center;font-size:.8rem;font-weight:600;border-radius:5px;padding:3px 8px}
.l0{background:var(--l0);color:var(--l0-ink)} .l1{background:var(--l1);color:var(--l1-ink)}
.l2{background:var(--l2);color:var(--l2-ink)} .l3{background:var(--l3);color:var(--l3-ink)}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:.85rem;color:var(--ink-2);align-items:center}

/* grupos y fichas */
.grupo{display:grid;gap:14px;margin-top:32px}
.grupo-head{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start}
.glyph{font-family:var(--display);font-stretch:88%;font-weight:800;font-size:1.4rem;width:40px;height:40px;display:grid;place-items:center;border:2px solid var(--ink);border-radius:50%}
.grupo-head p{color:var(--ink-2);font-size:.95rem;max-width:68ch;margin-top:4px}
.prop{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px;display:grid;gap:14px;scroll-margin-top:16px}
.prop header{display:flex;gap:8px;align-items:baseline}
.prop header .pid{font-size:.85rem}
.desc{color:var(--ink-2);max-width:72ch}
.levels{display:flex;flex-wrap:wrap;gap:10px 18px}
.levels span{display:grid;gap:3px}
.levels small{font-family:var(--mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.prop dl{margin:0;display:grid;gap:10px}
.kv{display:grid;grid-template-columns:190px 1fr;gap:12px;font-size:.94rem}
.kv dt{font-weight:600;color:var(--ink)}
.kv dd{margin:0;color:var(--ink-2)}
.kv.hyp{background:var(--hyp);border-left:3px solid var(--hyp-line);padding:8px 10px;border-radius:0 6px 6px 0}
details summary{cursor:pointer;font-weight:600;font-size:.92rem;color:var(--accent-ink)}
.trace{display:grid;gap:6px;margin-top:10px;font-size:.9rem}
.trace h5{font-family:var(--mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin:8px 0 0;font-weight:500}
.trace ul{margin:0;padding-left:0;list-style:none;display:grid;gap:8px}
.trace .ev{font-size:.78rem;color:var(--ink-3)}

/* patrones */
.pats{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.pats li{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:8px;scroll-margin-top:16px}
.pat-head{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.chip{font-size:.72rem;font-weight:600;border-radius:999px;padding:1px 9px;border:1px solid currentColor}
.t-pat{color:var(--pat)} .t-bre{color:var(--bre)} .t-dis{color:var(--dis)}
.caut{font-size:.9rem;color:var(--ink-2)}
.caut span{font-family:var(--mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin-right:4px}
.refs{display:flex;flex-wrap:wrap;gap:4px}

/* listas finales */
.design{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;list-style:none;margin:0;padding:0}
.design li{border-top:2px solid var(--ink);padding-top:8px;font-size:.93rem;color:var(--ink-2)}
.design b{display:block;color:var(--ink);font-family:var(--display);font-stretch:88%;font-size:1.02rem}
.steps{margin:0;padding-left:22px;display:grid;gap:10px;max-width:72ch}
.limits{margin:0;padding-left:20px;display:grid;gap:8px;max-width:72ch;color:var(--ink-2)}

/* catálogo */
.cat{margin-top:24px}
.hlist{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:0}
.hlist li{display:grid;grid-template-columns:64px 1fr;gap:10px;padding-block:12px;border-top:1px solid var(--line);scroll-margin-top:16px}
.hlist li:target{background:var(--l0);border-radius:6px}
.hlist .code-static{padding-top:3px}
.hlist p{font-size:.94rem}
.meta{font-size:.8rem;color:var(--ink-3);margin-top:4px}
.meta span{font-weight:600}
.ref{font-family:var(--mono);font-size:.74rem}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:.85rem;color:var(--ink-3)}

@media (max-width:760px){
  .facts{grid-template-columns:repeat(2,1fr)}
  .layers,.rules,.design{grid-template-columns:1fr}
  .kv{grid-template-columns:1fr;gap:2px}
  body{padding-inline:16px}
}
@media (prefers-reduced-motion: reduce){*{scroll-behavior:auto}}
html{scroll-behavior:smooth}
"""

pagina = f"""<title>Juventudes de Lima Este</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>{CSS}</style>
<div class="wrap">

<header class="masthead">
  <p class="eyebrow">Análisis para la Organización Rita Poma · 25 de septiembre de 2026</p>
  <h1>Juventudes de Lima Este</h1>
  <p class="dek">Qué necesitan, qué hacen, qué se les ofrece y qué actividades podrían convocarlos: el cruce de tres capas de evidencia en siete distritos, con propuestas que remiten a cada dato que las sustenta.</p>
  <div class="districts"><span>Ate</span><span>Chaclacayo</span><span>El Agustino</span><span>La Molina</span><span>Lurigancho-Chosica</span><span>San Juan de Lurigancho</span><span>Santa Anita</span></div>
  <div class="facts">
    <div><b>712 mil</b><span>jóvenes de 15 a 29 años (2026)</span></div>
    <div><b>44 de 151</b><span>actividades publicadas se dirigen a jóvenes</span></div>
    <div><b>4</b><span>señales de demanda, todas por ofertas concretas y gratuitas</span></div>
    <div><b>11</b><span>propuestas; ninguna con convocatoria demostrada</span></div>
  </div>
</header>

<section class="block" aria-labelledby="resumen">
  <h2 id="resumen">Resumen</h2>
  <ul class="summary">
    <li><strong>San Juan de Lurigancho y Ate concentran el 69 % de los jóvenes</strong> de los siete distritos (<a class="code" href="#H1-01">H1-01</a>).</li>
    <li><strong>Estudio y empleo compiten por el tiempo y el dinero.</strong> Entre quienes no estudian en Lima Este, 31 % trabaja y 28 % menciona problemas económicos; solo 2 % no estudia por falta de interés (<a class="code" href="#H2-12">H2-12</a>). En Lima Metropolitana, el desempleo juvenil es de 11,7 % y el 22 % de las mujeres jóvenes no estudia ni trabaja (<a class="code" href="#H1-06">H1-06</a>, <a class="code" href="#H1-07">H1-07</a>).</li>
    <li><strong>Lo que hacen, medido en Lima Este:</strong> 93 % usa pantallas cada semana, 63 % va al cine en el año, 45 % a espectáculos en vivo, 46 % juega en el celular y 28 % hace deporte cada semana, con una brecha grande por sexo (<a class="code" href="#H2-01">H2-01</a>, <a class="code" href="#H2-02">H2-02</a>, <a class="code" href="#H2-07">H2-07</a>, <a class="code" href="#H2-08">H2-08</a>).</li>
    <li><strong>La oferta publicada casi termina a los 17 años.</strong> Lo dirigido a jóvenes se concentra en empleo, voluntariado y preparación preuniversitaria; para 18–29 casi no hay deporte, cultura ni tecnología (<a class="code" href="#H3-01">H3-01</a>, <a class="code" href="#H3-02">H3-02</a>).</li>
    <li><strong>La convocatoria casi nunca se puede observar.</strong> Las cifras las declara quien organiza, y las únicas señales de demanda son por una beca o unos talleres gratuitos concretos, que no se generalizan (<a class="code" href="#H3-06">H3-06</a>, <a class="code" href="#H3-08">H3-08</a>, <a class="code" href="#H3-12">H3-12</a>).</li>
    <li><strong>Las propuestas más respaldadas</strong> son la preparación preuniversitaria con orientación y becas y la empleabilidad y primer empleo. <strong>Deporte para 18–29, cultura urbana y música en vivo, y cine</strong> tienen práctica alta en Lima Este y son las mejores candidatas para pilotos que midan la convocatoria.</li>
    <li><strong>Todas las propuestas son hipótesis de convocatoria:</strong> deben validarse con una consulta a jóvenes y pilotos con indicadores definidos de antemano.</li>
  </ul>
</section>

<section class="block" aria-labelledby="leer">
  <h2 id="leer">Cómo leer este informe</h2>
  <p class="lead">El análisis tiene tres capas. Cada afirmación lleva un código (<span class="code-static">H1-</span>, <span class="code-static">H2-</span>, <span class="code-static">H3-</span>) que lleva al hallazgo, con su fuente, su población y lo que no permite afirmar.</p>
  <div class="rules">
    <div><b>La ausencia de oferta no es demanda</b>Que no se encontrara una actividad solo dice que no se publicó.</div>
    <div><b>La frecuencia de oferta no es interés</b>Muchas actividades de un tema reflejan las decisiones de quien organiza.</div>
    <div><b>Una señal de demanda vale para su oferta</b>Más postulantes que becas es demanda por esa beca, no interés general por la formación.</div>
    <div><b>Lo infantil no se generaliza</b>Las cifras de talleres para 6–17 años no describen a los jóvenes de 15–29.</div>
  </div>
  <div class="tbl"><table>
    <thead><tr><th>Tipo de evidencia</th><th>Qué permite afirmar</th></tr></thead>
    <tbody>
      <tr><td>Representativa de Lima Este</td><td>Estimación de los siete distritos juntos con encuestas del INEI; nunca por distrito.</td></tr>
      <tr><td>Representativa de Lima Metropolitana</td><td>Describe a los 43 distritos; se cita como contexto, no como Lima Este.</td></tr>
      <tr><td>Registro administrativo distrital</td><td>Nacimientos o casos atendidos por distrito; depende del acceso a los servicios.</td></tr>
      <tr><td>Señal</td><td>Personas u organizaciones autoseleccionadas y estudios de mercado antiguos.</td></tr>
      <tr><td>Oferta · participación declarada · demanda observada</td><td>Lo publicado, las cifras que da quien organiza y las señales de más interesados que cupos.</td></tr>
    </tbody>
  </table></div>
</section>

<section class="block" aria-labelledby="capas">
  <h2 id="capas">Lo que sabemos, capa por capa</h2>
  <div class="layers">
    <div class="layer"><h3>1 · Contexto y necesidades</h3><p class="q">Dato Joven, ENAHO</p><ul>
      <li>~712 mil jóvenes; un tercio de 15–19 años (<a class="code" href="#H1-01">H1-01</a>).</li>
      <li>Pocas organizaciones juveniles acreditadas en los distritos más poblados; ninguna de deporte (<a class="code" href="#H1-02">H1-02</a>).</li>
      <li>Desempleo de 11,7 %, informalidad de 65 %, 22 % de mujeres jóvenes sin estudio ni empleo (Lima Metropolitana; <a class="code" href="#H1-06">H1-06</a>, <a class="code" href="#H1-07">H1-07</a>).</li>
      <li>Episodio depresivo en 21,6 % de las mujeres jóvenes (Lima Metropolitana; <a class="code" href="#H1-08">H1-08</a>).</li>
      <li>Un tercio dejó de hacer actividades por la delincuencia (<a class="code" href="#H1-10">H1-10</a>).</li>
      <li>Maternidad adolescente sobre la mediana en El Agustino, Santa Anita y Ate (<a class="code" href="#H1-13">H1-13</a>).</li>
    </ul></div>
    <div class="layer"><h3>2 · Intereses y hábitos</h3><p class="q">ENUT, ENAPRES, ENAHO, Ipsos</p><ul>
      <li>Cine 63 %, espectáculos en vivo 45 %, conciertos 21 % (Lima Este; <a class="code" href="#H2-07">H2-07</a>).</li>
      <li>46 % juega en el celular, 35 % en línea (<a class="code" href="#H2-08">H2-08</a>).</li>
      <li>Deporte semanal 28 %; 49 % de los hombres y 20 % de las mujeres (<a class="code" href="#H2-02">H2-02</a>).</li>
      <li>El dinero frena el cine y los conciertos; "no hay oferta" casi no aparece como motivo (<a class="code" href="#H2-09">H2-09</a>).</li>
      <li>La mitad estudia y más de la mitad trabaja: el tiempo es escaso (<a class="code" href="#H2-06">H2-06</a>).</li>
      <li>El deseo de emprender solo se midió en 2019–2020 (<a class="code" href="#H2-13">H2-13</a>).</li>
    </ul></div>
    <div class="layer"><h3>3 · Oferta y convocatoria</h3><p class="q">Notas municipales y de entidades públicas, 2024–2026</p><ul>
      <li>151 actividades: 44 para jóvenes, 53 para niños y adolescentes, 51 para todo público (<a class="code" href="#H3-01">H3-01</a>).</li>
      <li>180 alumnos en la academia gratuita de Chosica; 100 becarios en El Agustino (<a class="code" href="#H3-05">H3-05</a>).</li>
      <li>Hackathon en SJL con 400 inscripciones (<a class="code" href="#H3-10">H3-10</a>).</li>
      <li>Cultura urbana ofrecida, sin cifras de asistencia juvenil (<a class="code" href="#H3-13">H3-13</a>).</li>
      <li>Chaclacayo casi no publica; SJL no tiene notas de 2024 (<a class="code" href="#H3-18">H3-18</a>).</li>
    </ul></div>
  </div>
</section>

<section class="block" aria-labelledby="patrones">
  <h2 id="patrones">Patrones, brechas y condiciones de diseño</h2>
  <p class="lead">Una <strong>brecha</strong> es la distancia entre una necesidad o práctica documentada y la oferta visible; no prueba que los jóvenes quieran la actividad que falta.</p>
  <ol class="pats">{patrones}</ol>
</section>

<section class="block" aria-labelledby="propuestas">
  <h2 id="propuestas">Propuestas de actividades</h2>
  <p class="lead">Cada propuesta se califica por separado en tres dimensiones. <strong>Necesidad:</strong> ¿hay una necesidad documentada en ese segmento? <strong>Interés o práctica:</strong> ¿los jóvenes ya hacen algo parecido? <strong>Convocatoria:</strong> ¿hay evidencia de que una actividad así convoque jóvenes en Lima Este? No se combinan en un puntaje.</p>
  <div class="legend"><span>Nivel:</span> {nivel("sin evidencia")} {nivel("bajo")} {nivel("medio")} {nivel("alto")}</div>
  <div class="matrix tbl"><table>
    <thead><tr><th>Propuesta</th><th>Necesidad</th><th>Interés o práctica</th><th>Convocatoria</th></tr></thead>
    <tbody>{filas_matriz}</tbody>
  </table></div>
  {bloques}
</section>

<section class="block" aria-labelledby="diseno">
  <h2 id="diseno">Condiciones para cualquier actividad</h2>
  <ul class="design">
    <li><b>Gratuita o de costo mínimo</b>El dinero limita el estudio y el acceso a cine y conciertos; las cuatro señales de demanda son de ofertas gratuitas (<a class="code" href="#PT-09">PT-09</a>).</li>
    <li><b>Corta y en horarios posibles</b>Fines de semana o bloques breves: la mitad estudia y más de la mitad trabaja (<a class="code" href="#PT-08">PT-08</a>).</li>
    <li><b>Cerca y segura</b>Horarios diurnos, espacios seguros y recorridos cortos, sobre todo para mujeres (<a class="code" href="#PT-10">PT-10</a>).</li>
    <li><b>Segmentada por edad</b>15–17 llegan por colegios; 18–24 buscan estudio y primer empleo; 25–29, empleo (<a class="code" href="#PT-02">PT-02</a>, <a class="code" href="#PT-12">PT-12</a>).</li>
    <li><b>Con enfoque en mujeres jóvenes</b>Más necesidades documentadas y menos práctica deportiva: medir su participación en cada piloto (<a class="code" href="#PT-06">PT-06</a>).</li>
    <li><b>Con difusión propia</b>Redes, colegios, institutos y organizaciones juveniles; no depender de la comunicación municipal (<a class="code" href="#PT-11">PT-11</a>).</li>
  </ul>
</section>

<section class="block" aria-labelledby="siguientes">
  <h2 id="siguientes">Próximos pasos</h2>
  <ol class="steps">
    <li><strong>Consulta breve a jóvenes de Lima Este</strong> en colegios, institutos, redes y organizaciones del RENOJ: interés en las actividades propuestas, horarios, distancia, costo y canal de información.</li>
    <li><strong>Pilotos pequeños</strong> de los grupos A y B con indicadores definidos de antemano: inscritos frente a cupos, asistencia a la primera y cuarta sesión, perfil de quienes llegan y canal por el que se enteraron.</li>
    <li><strong>Contacto directo con las municipalidades</strong>, sobre todo Chaclacayo, Ate y SJL, para conocer su oferta, cupos e inscritos.</li>
    <li><strong>Decidir qué escalar</strong> con los resultados de la consulta y los pilotos.</li>
  </ol>
</section>

<section class="block" aria-labelledby="limites">
  <h2 id="limites">Límites</h2>
  <ul class="limits">
    <li>No hay datos por distrito sobre intereses o prácticas: las encuestas representan a Lima Este en conjunto o a Lima Metropolitana.</li>
    <li>Ninguna fuente pregunta a los jóvenes de Lima Este qué actividades harían.</li>
    <li>La oferta registrada no es un censo: depende de lo que cada municipalidad publica, y la de organizaciones sociales casi no aparece.</li>
    <li>Las cifras de participación son declaradas, aproximadas y no comparables entre sí.</li>
    <li>Empleo, salud mental y seguridad se conocen para Lima Metropolitana, no para Lima Este.</li>
    <li>Las encuestas llegan a 2024 o 2025.</li>
  </ul>
</section>

<section class="block" aria-labelledby="catalogo">
  <h2 id="catalogo">Catálogo de hallazgos</h2>
  <p class="lead">Los 49 hallazgos que sustentan patrones y propuestas, con su tipo de evidencia, población, geografía, periodo y precisión, lo que no permiten afirmar y dónde verificarlos en el repositorio del proyecto.</p>
  {catalogo}
</section>

<footer>Fuentes: Dato Joven (Observatorio Nacional de Juventud); ENAHO, ENAPRES y ENUT (INEI); Ipsos; notas de prensa de las siete municipalidades, SERPAR, SENAJU, MTPE, IPD, Ministerio de Cultura, DEVIDA y Municipalidad de Lima. Trazabilidad técnica: <span class="ref">resultados/</span> y <span class="ref">fuentes/metodologia_integracion.md</span> del repositorio ORP-juventudLimaEste.</footer>
</div>
"""

SALIDA.write_text(pagina)
print(f"resultados/informe_final.html: {len(pagina) // 1024} KB")
