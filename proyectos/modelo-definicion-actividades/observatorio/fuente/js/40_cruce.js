/* Cruce de evidencia: el modelo multicriterio, la matriz, los grupos de jóvenes, los hallazgos y las evidencias */
const CR = D.cruce, MOD = CR.modelo, CRIT = MOD.criterios;
// Paleta de los seis criterios (validada: separación para daltonismo entre vecinos; contraste bajo compensado con etiquetas y tabla).
const COLOR_CRIT = { necesidad: "#e0402f", publico: "#3b4cc0", practica: "#14a38b", convocatoria: "#eda100", espacio: "#8a5cd6", aliados: "#e87ba4" };
const CAPA_CRIT = { necesidad: "Contexto", publico: "Contexto", practica: "Intereses", convocatoria: "Oferta", espacio: "Oferta", aliados: "Contexto" };
const CLASE_NIVEL = { "Mayor potencial": "n1", "Potencial medio": "n2", "Menor respaldo hoy": "n3" };
const refTxt = (s) => (s == null ? "" : String(s).replace(/(\d) \(referencial\)/g, "$1*").replace(/ \(referencial\)/g, "*"));

function puntajeCon(alt, pesos) {
  const tot = CRIT.reduce((a, c) => a + pesos[c.id], 0);
  return tot ? (100 * CRIT.reduce((a, c) => a + pesos[c.id] * alt.puntajes[c.id], 0)) / (3 * tot) : 0;
}
const nivelDe = (p) => MOD.niveles.find(([u]) => p >= u - 1e-9)[1];
const puntos = (n) => "●".repeat(n) + "○".repeat(3 - n);
const altCorta = (a) => a.actividad.replace(/\s*\(.*\)\s*$/, "");

Object.assign(S, { patTipo: "Todos", halCapa: "1", evBuscar: "", evVer: 25 });
Object.assign(CONTROLES, {
  patTipo: [["Todos", "Todos"], ["patrón", "Patrones"], ["brecha", "Brechas"], ["condición transversal", "Condiciones transversales"]],
  halCapa: [["1", "Contexto"], ["2", "Intereses"], ["3", "Oferta"]]
});

HERO.cruce = () => {
  $("hero-cruce").innerHTML = `<div class="v">${CRIT.length} criterios</div>
    <div class="l">cruzan <b>${num(CR.evidencias.length)}</b> evidencias de las tres capas para evaluar <b>${MOD.alternativas.length}</b> alternativas de actividades.</div>`;
};

// ---------------------------------------------------------------- El modelo
function renderCriterios() {
  const porCapa = ["Contexto", "Intereses", "Oferta"].map((c) => `<div class="fm-capa"><span>${c}</span>${CRIT.filter((k) => CAPA_CRIT[k.id] === c)
    .map((k) => `<i style="--c:${COLOR_CRIT[k.id]}">${esc(k.nombre)}</i>`).join("")}</div>`).join("");
  $("cr-flujo").innerHTML = `<div class="fm-bloque">${porCapa}</div><div class="fm-flecha">→</div>
    <div class="fm-paso"><b>0 a 3</b><span>por criterio, con reglas fijas</span></div><div class="fm-flecha">→</div>
    <div class="fm-paso"><b>0 a 100</b><span>promedio ponderado + solidez de la evidencia</span></div><div class="fm-flecha">→</div>
    <a class="fm-paso fm-final" href="#resultado"><b>Actividades</b><span>ordenadas por respaldo, sin predecir asistencia</span></a>`;
  $("cr-criterios").innerHTML = CRIT.map((k) => {
    const reglas = k.reglas.split(" · ");
    return `<article class="criterio" style="--c:${COLOR_CRIT[k.id]}">
      <div class="criterio-cab"><span class="criterio-capa">${CAPA_CRIT[k.id]}</span><span class="criterio-peso" title="Peso recomendado">Peso ${MOD.pesos.recomendado[k.id]}</span></div>
      <h4>${esc(k.nombre)}</h4><p class="criterio-q">${esc(k.pregunta)}</p>
      <ul>${reglas.map((r) => `<li>${esc(r)}</li>`).join("")}</ul>
      <p class="criterio-f">Fuente: ${esc(k.fuente)}</p></article>`;
  }).join("");
  const K = CR.condiciones;
  const cond = [
    ["Horario", `Domingo por la tarde y sábado por la noche`, `${pct(K.horario.domingo_tarde)} y ${pct(K.horario.sabado_noche)} tienen dos horas libres seguidas; un día de semana por la tarde, solo ${pct(K.horario.semana_tarde)}${K.horario.semana_tarde_ref ? "*" : ""}.`],
    ["Seguridad", "Si es de noche: lugar seguro y retorno acompañado", `${pct(K.seguridad.total)} se siente inseguro al caminar de noche por su barrio (mujeres: ${pct(K.seguridad.mujeres)}).`],
    ["Costo", "Gratis", `La falta de dinero es el motivo de ${pct(K.costo.dinero_cine)} para no ir al cine y de ${pct(K.costo.dinero_conciertos)} para no ir a conciertos; ${pct(K.costo.gratis_festival)} entró gratis a los festivales locales.`],
    ["Información", "Difundir con tiempo y por redes cercanas", `${pct(K.informacion.feria_libro)} no fue a una feria del libro porque no se enteró a tiempo.`],
    ["Cuidado", "Considerar a quienes cuidan niños", `${pct(K.cuidado.hogar_ninos)} de las mujeres jóvenes dedicadas al hogar vive con niños de 0 a 5 años (otras mujeres: ${pct(K.cuidado.otras_ninos)}).`]
  ];
  $("cr-condiciones").innerHTML = cond.map(([t, r, d]) => `<div class="cond"><span>${t}</span><b>${esc(r)}</b><p>${esc(d)}</p></div>`).join("");
}

// ---------------------------------------------------------------- Matriz
function renderMatriz() {
  $("cr-matriz-leyenda").innerHTML = `<span>Puntaje por criterio:</span>${[3, 2, 1, 0].map((n) => `<span class="ml-item"><i class="ml-celda" style="--c:${C.indigo};--a:${0.12 + 0.28 * n}">${puntos(n)}</i>${n === 3 ? "fuerte" : n === 2 ? "medio" : n === 1 ? "débil" : "sin evidencia a favor"}</span>`).join("")}`;
  const alts = MOD.alternativas.slice().sort((a, b) => puntajeCon(b, MOD.pesos.recomendado) - puntajeCon(a, MOD.pesos.recomendado));
  let h = `<table class="matriz"><thead><tr><th>Alternativa</th>${CRIT.map((k) => `<th><i style="background:${COLOR_CRIT[k.id]}"></i>${esc(k.nombre)}</th>`).join("")}<th>Puntaje</th><th title="Parte de la evidencia citada que es de Lima Este y precisa">Solidez</th></tr></thead><tbody>`;
  alts.forEach((a) => {
    const p = puntajeCon(a, MOD.pesos.recomendado), nv = nivelDe(p);
    h += `<tr data-ficha="${a.ficha}" tabindex="0"><td><span class="m-id">${a.ficha}</span>${esc(altCorta(a))}<small>${esc(a.linea)}</small></td>`;
    CRIT.forEach((k) => {
      const n = a.puntajes[k.id];
      h += `<td><span class="ml-celda" style="--c:${COLOR_CRIT[k.id]};--a:${n === 0 ? 0.06 : 0.14 + 0.28 * n}" title="${esc(k.nombre)}: ${esc(a.datos[k.id])}">${puntos(n)}</span></td>`;
    });
    h += `<td><span class="nivel ${CLASE_NIVEL[nv]}">${dec(p, 0)}</span></td><td class="m-sol" title="${a.solidez} % de la evidencia citada es de Lima Este y precisa">${a.solidez_nivel} · ${a.solidez} %</td></tr>`;
  });
  $("cr-matriz").innerHTML = h + "</tbody></table>";
  const t2 = alts.slice(0, 2);
  const top = t2.map((a) => `<b>${esc(altCorta(a).toLowerCase())}</b>`).join(" y ");
  const ambas = t2.every((a) => a.puntajes.necesidad === 3 && a.puntajes.convocatoria === 3);
  const yLista = (xs) => (xs.length > 1 ? xs.slice(0, -1).join(", ") + " y " + xs[xs.length - 1] : xs[0] || "");
  const cult = alts.filter((a) => a.puntajes.practica === 3 && a.puntajes.convocatoria <= 1).map((a) => esc(altCorta(a).toLowerCase()));
  const nec = alts.filter((a) => a.puntajes.necesidad >= 2 && a.puntajes.practica === 0 && a.puntajes.convocatoria <= 1).map((a) => esc(altCorta(a).toLowerCase()));
  $("cr-matriz-lectura").innerHTML = `Las dos alternativas con más respaldo son ${top}${ambas ? ": combinan una necesidad medida en Lima Este con convocatoria observada (más interesados que cupos)" : ""}. ${cult.length ? `En ${yLista(cult)} la práctica es la más alta (los jóvenes ya hacen esa misma actividad), pero hay poca evidencia de que una oferta organizada convoque. ` : ""}${nec.length ? `En cambio, ${yLista(nec)} responden a una necesidad documentada, pero ninguna fuente muestra práctica relacionada ni convocatoria comparable.` : ""}`;
}
$("cr-matriz").addEventListener("click", (ev) => { const tr = ev.target.closest("[data-ficha]"); if (tr) location.hash = tr.dataset.ficha; });
$("cr-matriz").addEventListener("keydown", (ev) => { const tr = ev.target.closest("[data-ficha]"); if (tr && ev.key === "Enter") location.hash = tr.dataset.ficha; });

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
