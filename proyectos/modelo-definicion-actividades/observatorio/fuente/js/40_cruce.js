/* Cruce de evidencia: el modelo de convocatoria por público, la matriz, los grupos de jóvenes, los hallazgos y las evidencias */
const CR = D.cruce, MOD = CR.modelo, TIPOS = MOD.tipos, PUB = MOD.publicos;
const PUB_K = Object.fromEntries(PUB.map((p) => [p.k, p]));
// "Ya la hacen" y "frenados" (validado: separación para daltonismo; el ámbar se compensa con etiquetas y tabla).
const COLOR_YA = "#3b4cc0", COLOR_FR = "#eda100";
const GRUPO = { actividad: "Actividades", servicio: "Servicios" };
const CONV_TXT = { C4: "más interesados que cupos", C3: "participación comparable", C2: "señales débiles", C1: "solo anuncios", C0: "sin registros" };
const sinDato = (s) => !s || (s[0] == null && s[1] == null);
const refTxt = (s) => (s == null ? "" : String(s).replace(/(\d) \(referencial\)/g, "$1*").replace(/ \(referencial\)/g, "*"));
const yLista = (xs) => (xs.length > 1 ? xs.slice(0, -1).join(", ") + " y " + xs[xs.length - 1] : xs[0] || "");

// Formato de personas: "136 mil", "4,2 mil".
const milC = (v) => (v == null ? "—" : v >= 9950 ? mil(v) : dec(v / 1000, 1) + NB + "mil");
const pubCorto = (p) => `${p.sexo === "mujer" ? "Mujeres" : "Hombres"} ${p.edad.replace("-", "–")}`;
const pubLargo = (p) => grupoTxt(p.sexo, p.edad);
const bloqueTxt = (b) => { const [dia, h] = b.split(", "); const [a, z] = h.split("-"); return `${dia.toLowerCase()} de ${a} a ${z}`; };

// Suma del embudo para un conjunto de públicos: {ya, fr, tot} en personas.
function filtrarPublicos(sexo, edad) { return PUB.filter((p) => (sexo === "total" || p.sexo === sexo) && (edad === "todas" || p.edad === edad)); }
function convDe(t, pubs) {
  let ya = 0, fr = 0;
  pubs.forEach((p) => { const s = t.seg[p.k]; if (s) { ya += s[2]; fr += s[3]; } });
  return { ya, fr, tot: ya + fr };
}
function principalDe(t, pubs) {
  return pubs.filter((p) => t.seg[p.k]).sort((a, b) => (t.seg[b.k][2] + t.seg[b.k][3]) - (t.seg[a.k][2] + t.seg[a.k][3]))[0];
}

Object.assign(S, { patTipo: "Todos", halCapa: "1", evBuscar: "", evVer: 25, ejTipo: "A-01", ejPub: "mujer|25-29", matVista: "conv" });
Object.assign(CONTROLES, {
  patTipo: [["Todos", "Todos"], ["patrón", "Patrones"], ["brecha", "Brechas"], ["condición transversal", "Condiciones transversales"]],
  halCapa: [["1", "Contexto"], ["2", "Intereses"], ["3", "Oferta"]],
  ejPub: PUB.map((p) => [p.k, pubCorto(p)]),
  matVista: [["conv", "Jóvenes convocables"], ["pct", "% que la hace o la haría"]]
});

HERO.cruce = () => {
  $("hero-cruce").innerHTML = `<div class="v">6 públicos</div>
    <div class="l">mujeres y hombres de 15 a 19, 20 a 24 y 25 a 29 años, cruzados con <b>${TIPOS.length}</b> actividades y servicios.</div>`;
};

// ---------------------------------------------------------------- El modelo
function renderCriterios() {
  const P = MOD.pasos;
  const signo = ["", "×", "×", "="];
  $("cr-embudo").innerHTML = P.map((p, i) => `${i ? `<div class="em-signo" aria-hidden="true">${signo[i]}</div>` : ""}
    <article class="em-paso${i === P.length - 1 ? " em-final" : ""}">
      <span class="em-n">${i < P.length - 1 ? `Paso ${i + 1}` : "Resultado"}</span>
      <h4>${esc(p.nombre)}</h4>
      <p class="em-q">${esc(p.pregunta)}</p>
      <p class="em-como">${esc(p.como_se_mide)}</p>
      <p class="em-f">${esc(p.fuente)}</p>
    </article>`).join("");

  // Ejemplo paso a paso (actividad y público elegidos)
  const sel = $("ej-tipo");
  if (!sel.options.length) {
    sel.innerHTML = ["actividad", "servicio"].map((g) => `<optgroup label="${GRUPO[g]}">${TIPOS.filter((t) => t.grupo === g && t.medido)
      .sort((a, b) => b.total - a.total).map((t) => `<option value="${t.id}">${esc(t.tipo)}</option>`).join("")}</optgroup>`).join("");
    sel.addEventListener("change", () => { S.ejTipo = sel.value; renderEjemplo(); });
  }
  sel.value = S.ejTipo;
  renderEjemplo();

  // Los seis públicos
  const sit = (p) => {
    const s = p.sit, ops = [["solo_estudia", "solo estudia"], ["solo_trabaja", "solo trabaja"], ["estudia_y_trabaja", "estudia y trabaja"], ["ni_estudia_ni_trabaja", "no estudia ni trabaja"]];
    const [k, t] = ops.sort((a, b) => (s[b[0]] || 0) - (s[a[0]] || 0))[0];
    return `${pct(s[k], 0)} ${t}${p.sexo === "mujer" && s.hogar >= 10 ? ` · ${pct(s.hogar, 0)} se dedica al hogar` : ""}`;
  };
  const maxL = Math.max(...PUB.map((p) => p.libre));
  $("cr-publicos").innerHTML = `<div class="pb-fila pb-cab"><span>Público</span><span>Jóvenes en 2026</span><span>Tiempo libre el domingo de 14:00 a 18:00</span><span>Evita salir de noche</span><span>A qué se dedica la mayoría</span></div>` +
    PUB.map((p) => `<div class="pb-fila"><b>${pubCorto(p)}</b><span class="n">${num(p.pob)}</span>
      <span class="pb-barra"><i style="width:${(100 * p.libre) / maxL}%"></i><em>${pct(p.libre, 0)}</em></span>
      <span class="n">${pct(p.evita, 0)}</span><span>${sit(p)}</span></div>`).join("");

  const K = CR.condiciones;
  const cond = [
    ["Horario", "Domingo por la tarde", `Es el mejor horario para los seis públicos: ${pct(K.horario.domingo_tarde)} de los jóvenes tiene dos horas libres seguidas. Le sigue el sábado por la noche (${pct(K.horario.sabado_noche)}); un día de semana por la tarde, solo ${pct(K.horario.semana_tarde)}${K.horario.semana_tarde_ref ? "*" : ""}.`],
    ["Seguridad", "Si es de noche: lugar seguro y retorno acompañado", `${pct(K.seguridad.total)} se siente inseguro al caminar de noche por su barrio (mujeres: ${pct(K.seguridad.mujeres)}; hombres: ${pct(K.seguridad.hombres)}).`],
    ["Costo", "Gratis", `La falta de dinero es el motivo de ${pct(K.costo.dinero_cine)} para no ir al cine y de ${pct(K.costo.dinero_conciertos)} para no ir a conciertos.`],
    ["Información", "Difundir con tiempo y por redes", `${pct(K.informacion.feria_libro)} no fue a una feria del libro porque no se enteró a tiempo. Casi todos los jóvenes usan internet para comunicarse.`],
    ["Cuidado", "Considerar a quienes cuidan niños", `${pct(K.cuidado.hogar_ninos)} de las mujeres jóvenes dedicadas al hogar vive con niños de 0 a 5 años (otras mujeres: ${pct(K.cuidado.otras_ninos)}).`]
  ];
  $("cr-condiciones").innerHTML = cond.map(([t, r, d]) => `<div class="cond"><span>${t}</span><b>${esc(r)}</b><p>${esc(d)}</p></div>`).join("");
}

function renderEjemplo() {
  const t = TIPOS.find((x) => x.id === S.ejTipo), p = PUB_K[S.ejPub], s = t.seg[p.k];
  if (sinDato(s)) {
    $("ej-embudo").innerHTML = "";
    $("ej-lectura").innerHTML = `La encuesta no mide <b>${esc(t.tipo.toLowerCase())}</b> para ${pubLargo(p)}. Elige otro público.`;
    return;
  }
  const dem = (s[0] || 0) + (s[1] || 0), conLibre = (p.pob * dem) / 100, conv = s[2] + s[3];
  const fila = (ancho, cifra, txt, clase) => `<div class="ej-fila ${clase || ""}"><div class="ej-barra"><i style="width:${Math.max(ancho, 0.6)}%"></i></div><b>${cifra}</b><span>${txt}</span></div>`;
  const partes = [];
  if (s[0]) partes.push(`${pct(s[0])} ya la hace`);
  if (s[1]) partes.push(`${pct(s[1])} no la hace solo por falta de dinero, información u oferta`);
  $("ej-embudo").innerHTML =
    fila(100, num(p.pob), `${pubLargo(p)} viven en Lima Este`) +
    fila(dem, num(conLibre), `la hacen o la harían: ${pct(dem)} (${partes.join("; ") || "sin dato"})`, "ej-2") +
    fila((dem * p.libre) / 100, num(conv), `además tienen libre el ${bloqueTxt(p.mejor)}: ${pct(p.libre)}`, "ej-3");
  const notas = [];
  if (t.factor < 1) notas.push("La encuesta mide una práctica parecida, no la misma actividad: cuenta la mitad.");
  if (!t.fren_medidos) notas.push("Ninguna encuesta pregunta por qué no la hacen: el número es un piso.");
  $("ej-lectura").innerHTML = `<b>${esc(t.tipo)}</b> podría convocar a unas <b>${num(Math.round(conv / 100) * 100)}</b> ${pubLargo(p).replace(/^(las|los) /, "")}. ${notas.join(" ")}`;
}

// ---------------------------------------------------------------- Matriz: cada tipo, público por público
function renderMatriz() {
  const pct_ = S.matVista === "pct";
  $("cr-matriz-leyenda").innerHTML = pct_
    ? `<span>Cada celda: % del público que la hace o la haría si es gratis, cercana y bien difundida (sin contar el tiempo libre). Más oscuro = más alto.</span>`
    : `<span>Cada celda: jóvenes convocables, en miles. Más oscuro = más jóvenes (la escala de servicios es aparte).</span>`;
  const valor = (t, p) => { const s = t.seg[p.k]; if (sinDato(s)) return null; return pct_ ? (s[0] || 0) + (s[1] || 0) : s[2] + s[3]; };
  const cab = `<thead><tr><th rowspan="2">Tipo</th><th colspan="3" class="mt-sexo">Mujeres</th><th colspan="3" class="mt-sexo">Hombres</th><th rowspan="2">${pct_ ? "15 a 29" : "Total"}</th></tr>
    <tr>${PUB.map((p) => `<th>${p.edad.replace("-", "–")}</th>`).join("")}</tr></thead>`;
  let body = "";
  ["actividad", "servicio"].forEach((g) => {
    const xs = TIPOS.filter((t) => t.grupo === g).sort((a, b) => (b.total || -1) - (a.total || -1));
    const max = Math.max(...xs.flatMap((t) => PUB.map((p) => valor(t, p) || 0)));
    body += `<tr class="mt-grupo"><td colspan="8">${GRUPO[g]}</td></tr>`;
    xs.forEach((t) => {
      body += `<tr data-alt="${t.id}" tabindex="0"><td><span class="m-id">${t.id}</span>${esc(t.tipo)}</td>`;
      if (!t.medido) { body += `<td colspan="7"><span class="ml-celda ml-na mt-na">Ninguna encuesta la mide: no se ordena</span></td></tr>`; return; }
      PUB.forEach((p) => {
        const v = valor(t, p);
        if (v == null) { body += `<td><span class="ml-celda ml-na" title="La encuesta no lo mide para este público">—</span></td>`; return; }
        body += `<td><span class="ml-celda" style="--c:${C.indigo};--a:${(0.05 + 0.75 * v / max).toFixed(2)};${v / max > 0.55 ? "color:#fff" : ""}" title="${esc(pubCorto(p))}: ${pct_ ? pct(v) : num(v) + " jóvenes"}">${pct_ ? dec(v, 0) : dec(v / 1000, 1)}</span></td>`;
      });
      const tot = pct_ ? (100 * PUB.reduce((s, p) => s + p.pob * ((t.seg[p.k][0] || 0) + (t.seg[p.k][1] || 0)) / 100, 0)) / PUB.reduce((s, p) => s + p.pob, 0) : t.total;
      body += `<td><b>${pct_ ? pct(tot, 0) : milC(tot)}</b></td></tr>`;
    });
  });
  $("cr-matriz").innerHTML = `<table class="matriz mt">${cab}<tbody>${body}</tbody></table>`;
  const top = PUB.map((p) => {
    const t = TIPOS.filter((x) => x.grupo === "actividad" && x.medido).sort((a, b) => (b.seg[p.k][2] + b.seg[p.k][3]) - (a.seg[p.k][2] + a.seg[p.k][3]))[0];
    return `${pubCorto(p).toLowerCase()}: <b>${esc(t.tipo.toLowerCase())}</b>`;
  });
  $("cr-matriz-lectura").innerHTML = `La actividad que más convoca a cada público: ${yLista(top)}. Haz clic en una fila para ver su ficha.`;
}
$("cr-matriz").addEventListener("click", (ev) => { const tr = ev.target.closest("[data-alt]"); if (tr) location.hash = tr.dataset.alt; });
$("cr-matriz").addEventListener("keydown", (ev) => { const tr = ev.target.closest("[data-alt]"); if (tr && ev.key === "Enter") location.hash = tr.dataset.alt; });
TABLAS.crMatriz = () => [["ID", "Tipo", "Grupo"].concat(PUB.map((p) => `${pubCorto(p)}: convocables`), ["Total", "Rango (margen de error)"]),
  TIPOS.filter((t) => t.medido).map((t) => [t.id, t.tipo, GRUPO[t.grupo]].concat(PUB.map((p) => num(t.seg[p.k][2] + t.seg[p.k][3])), [num(t.total), `${num(t.lo)}–${num(t.hi)}`]))];

// ---------------------------------------------------------------- Grupos de jóvenes
function renderSegmentos() {
  const s = CR.segmentos.filter((x) => x.dj[0] != null).slice().sort((a, b) => b.dj[1] - a.dj[1]);
  g("g-cr-segmentos").setOption(opc({
    grid: { left: 16, right: 80, top: 8, bottom: 20, containLabel: true },
    xAxis: { type: "value", min: 0, splitLine: { lineStyle: { color: C.linea } }, axisLabel: { color: C.tinta3, fontSize: 11, formatter: (v) => (v ? num(v / 1000) + NB + "mil" : "0") } },
    yAxis: ejeCat(s.map((x) => x.segmento), { axisLabel: { color: C.tinta2, fontSize: 12, width: 330, overflow: "break", lineHeight: 15 } }),
    tooltip: { formatter: (p) => { const x = s[p.dataIndex]; return tt(x.segmento, [{ v: `${num(x.dj[0] / 1000)}–${mil(x.dj[1])}`, n: `${dec(x.pct)} % de ${esc(x.ref.replace("-", "–"))} (${x.periodo})<br>${esc(x.fuente)}` }]); } },
    series: [
      { id: "base", type: "bar", stack: "r", data: s.map((x) => x.dj[0]), itemStyle: { color: "transparent" }, barMaxWidth: 14, silent: true, tooltip: { show: false } },
      { id: "rango", type: "bar", stack: "r", barMaxWidth: 14, data: s.map((x) => ({ value: x.dj[1] - x.dj[0], itemStyle: { color: x.fichas.some((f) => f.startsWith("F-")) ? C.indigo : C.gris2 } })),
        itemStyle: { borderRadius: 7 }, label: { show: true, position: "right", color: C.tinta, fontSize: 12, fontWeight: 600, formatter: (p) => `${num(s[p.dataIndex].dj[0] / 1000)}–${mil(s[p.dataIndex].dj[1])}` } }
    ]
  }), { replaceMerge: ["series"] });
  const a = s[0], z = s[s.length - 1];
  $("cr-seg-lectura").innerHTML = `El grupo más grande es el de <b>${esc(a.segmento.toLowerCase())}</b> (${num(a.dj[0] / 1000)}–${mil(a.dj[1])}); el más pequeño, <b>${esc(z.segmento.toLowerCase())}</b> (${num(z.dj[0] / 1000)}–${mil(z.dj[1])}). En índigo, los grupos a los que se dirige alguna alternativa; en gris, los que describen condiciones (tiempo o seguridad).`;
}
TABLAS.crSegmentos = () => [["ID", "Grupo", "%", "IC 95 %", "Periodo", "Personas (Dato Joven)", "Alternativas"], CR.segmentos.map((x) => [x.id, x.segmento, pct(x.pct), `${dec(x.lo)}–${dec(x.hi)}`, x.periodo, x.dj[0] != null ? `${num(x.dj[0] / 1000)}–${mil(x.dj[1])}` : "—", x.fichas.join(", ")])];

// ---------------------------------------------------------------- Hallazgos
function renderHallazgos() {
  const p = CR.patrones.filter((x) => S.patTipo === "Todos" || x.tipo === S.patTipo);
  $("cr-patrones").innerHTML = p.map((x) => `<article class="patron-c">
      <div class="patron-cab"><span class="tipo-chip">${esc(x.tipo)}</span><h4>${esc(x.tema)}</h4><span class="m-id">${x.id}</span></div>
      <div class="patron-cols">
        <div><span>Dato observado</span><p>${esc(refTxt(x.dato_observado))}</p></div>
        <div><span>Qué significa</span><p>${esc(refTxt(x.interpretacion))}</p></div>
        <div class="p-no"><span>Qué no permite afirmar</span><p>${esc(refTxt(x.no_permite_afirmar))}</p></div>
      </div></article>`).join("");
  const h = CR.hallazgos.filter((x) => String(x.capa) === S.halCapa);
  $("cr-hallazgos").innerHTML = h.map((x) => `<div class="hal"><span class="m-id">${x.id}</span><div><p>${esc(refTxt(x.enunciado))}</p>
      <small><b>No permite afirmar:</b> ${esc(refTxt(x.no_permite))} · ${esc(x.dimension)} · ${esc(x.geografia)} · ${esc(x.periodo)}</small></div></div>`).join("");
}

// ---------------------------------------------------------------- Evidencias
function valorEv(e) {
  if (e.valor == null) return "—";
  const r = e.precision === "referencial" ? "*" : "";
  if (e.unidad === "%") return pct(e.valor, e.precision === "sin error publicado" ? 0 : 1) + r;
  if (e.unidad === "horas") return dec(e.valor) + NB + "h" + r;
  if (e.unidad === "por 1 000" || e.unidad === "por 10 000") return dec(e.valor) + " " + e.unidad;
  return num(e.valor) + (e.unidad && !["personas"].includes(e.unidad) ? " " + e.unidad : "");
}
function renderEvidencias() {
  const q = S.evBuscar.trim().toLowerCase();
  const f = CR.evidencias.filter((e) => !q || `${e.id} ${e.tema} ${e.indicador} ${e.poblacion} ${e.ambito} ${e.fuente}`.toLowerCase().includes(q));
  $("ev-conteo").textContent = `${num(f.length)} evidencias`;
  $("cr-evidencias").innerHTML = `<table class="tabla-ev"><thead><tr><th>ID</th><th>Indicador</th><th>Población</th><th>Ámbito</th><th>Periodo</th><th>Valor</th><th>IC 95 %</th><th>Precisión</th><th>Fuente</th></tr></thead><tbody>${f.slice(0, S.evVer).map((e) => `<tr><td class="m-id">${e.id}</td><td>${esc(e.indicador)}<small>${esc(e.tema)}</small></td><td>${esc(e.poblacion || "")}</td><td>${esc(e.ambito)}</td><td>${esc(e.periodo)}</td><td class="n">${valorEv(e)}</td><td class="n">${e.lo != null ? `${dec(e.lo)}–${dec(e.hi)}` : ""}</td><td>${esc(e.precision)}</td><td><small>${esc(e.fuente)}</small></td></tr>`).join("")}</tbody></table>`;
  $("ev-mas").hidden = f.length <= S.evVer;
}
$("ev-buscar").addEventListener("input", (ev) => { S.evBuscar = ev.target.value; S.evVer = 25; renderEvidencias(); });
$("ev-mas").addEventListener("click", () => { S.evVer += 50; renderEvidencias(); });

Object.assign(RENDER, { criterios: renderCriterios, matriz: renderMatriz, segmentos: renderSegmentos, hallazgos: renderHallazgos, evidencias: renderEvidencias });
