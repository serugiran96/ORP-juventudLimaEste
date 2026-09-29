/* Capa 3 · Oferta: explorar el registro, público, convocatoria declarada y visibilidad */
const OF = D.oferta;
const REG = OF.registros;
const DIST_OF = D.contexto.poblacion.distritos.slice().sort((a, b) => b.jovenes - a.jovenes);
const COLOR_PUBLICO = { "Jóvenes": C.rojo, "Niños y adolescentes": C.indigo, "Todo público": C.gris2, "No indica": C.gris, "Fuera de 15–29": C.gris };
const COLOR_EVIDENCIA = { "oferta": C.gris2, "participación declarada": C.indigo2, "demanda observada": C.rojo };
const cap1 = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : s);

Object.assign(S, { ofDistrito: "Todos", ofPublico: "Todos", ofCosto: "Todos", ofTema: null, ofBuscar: "", ofVer: 12 });
Object.assign(CONTROLES, {
  ofDistrito: [["Todos", "Todos"]].concat(DIST_OF.map((d) => [d.nombre, d.corto])),
  ofPublico: [["Todos", "Todos"], ["Jóvenes", "Jóvenes"], ["Niños y adolescentes", "Niños y adolescentes"], ["Todo público", "Todo público"]],
  ofCosto: [["Todos", "Todos"], ["gratuito", "Gratis"], ["pagado", "Pagado"], ["no indica", "No indica"]]
});

HERO.oferta = () => {
  const jov = REG.filter((r) => r.publico === "Jóvenes").length;
  $("hero-oferta").innerHTML = `<div class="v">${num(REG.length)}</div>
    <div class="l">actividades publicadas entre ${OF.periodo[0]} y ${OF.periodo[1]}; <b>${num(jov)}</b> dirigidas a jóvenes.</div>`;
};

function ofFiltrados(ignorarTema) {
  const q = S.ofBuscar.trim().toLowerCase();
  return REG.filter((r) => (S.ofDistrito === "Todos" || r.distritos.includes(S.ofDistrito))
    && (S.ofPublico === "Todos" || r.publico === S.ofPublico)
    && (S.ofCosto === "Todos" || r.costo === S.ofCosto || (S.ofCosto === "pagado" && r.costo === "mixto"))
    && (ignorarTema || !S.ofTema || r.temas.includes(S.ofTema))
    && (!q || `${r.nombre} ${r.organizador || ""} ${r.temas.join(" ")} ${r.distritos.join(" ")}`.toLowerCase().includes(q)));
}
function contar(lista, clave) {
  const m = new Map();
  lista.forEach((r) => [].concat(clave(r)).forEach((k) => { if (k) m.set(k, (m.get(k) || 0) + 1); }));
  return [...m.entries()].sort((a, b) => b[1] - a[1]);
}

function tarjetaOferta(r, compacta) {
  const cifra = r.cifra_n != null ? `<div class="of-cifra"><b>${num(r.cifra_n)}</b> ${esc(r.cifra_tipo || "")}</div>`
    : r.cifra_texto ? `<div class="of-cifra"><span>${esc(r.cifra_texto)}</span></div>` : "";
  return `<article class="of-item${compacta ? " compacta" : ""}">
    <div class="of-meta">${esc(r.distritos.join(" · "))} · ${r.anio}</div>
    <h4>${esc(r.nombre)}</h4>
    <div class="of-tags"><span class="tag-p" style="--c:${COLOR_PUBLICO[r.publico] || C.gris}">${esc(r.publico)}</span>
      <span class="tag-s">${esc(cap1(r.tipo))}</span><span class="tag-s">${esc(r.costo === "gratuito" ? "Gratis" : cap1(r.costo))}</span>
      ${r.evidencia !== "oferta" ? `<span class="tag-s tag-e" style="--c:${COLOR_EVIDENCIA[r.evidencia]}">${esc(cap1(r.evidencia))}</span>` : ""}</div>
    ${cifra}
    ${!compacta ? `<div class="of-temas">${r.temas.map((t) => esc(t)).join(" · ")}</div>` : ""}
    ${r.url ? `<a class="of-fuente" href="${esc(r.url)}" target="_blank" rel="noopener">Ver fuente ↗</a>` : ""}
  </article>`;
}

// ---------------------------------------------------------------- Explorar
function renderExplorar() {
  const f = ofFiltrados(false), sinTema = ofFiltrados(true);
  const n = (fn) => f.filter(fn).length;
  $("of-tiles").innerHTML = [
    tile({ clase: "oscuro", v: num(f.length), l: "actividades con estos filtros" }),
    tile({ v: num(n((r) => r.publico === "Jóvenes")), l: "dirigidas a jóvenes" }),
    tile({ v: num(n((r) => r.costo === "gratuito")), l: "gratuitas" }),
    tile({ v: num(n((r) => r.evidencia === "participación declarada")), l: "con participación declarada" }),
    tile({ clase: "acento", v: num(n((r) => r.evidencia === "demanda observada")), l: "con demanda observada (más interesados que cupos)" })
  ].join("");
  const temas = contar(sinTema, (r) => r.temas);
  g("g-of-temas").setOption(opc({
    grid: { left: 16, right: 44, top: 6, bottom: 4, containLabel: true },
    xAxis: Object.assign(ejeVal(undefined, ""), { show: false }), yAxis: ejeCat(temas.map((t) => cap1(t[0]))),
    tooltip: { formatter: (p) => tt(p.name, [{ v: num(p.value), n: "actividades (clic para filtrar)" }]) },
    series: [{ id: "t", type: "bar", barMaxWidth: 16, data: temas.map(([t, c]) => ({ value: c, itemStyle: { color: S.ofTema === t ? C.rojo : C.indigo, opacity: S.ofTema && S.ofTema !== t ? 0.45 : 1 } })),
      itemStyle: { borderRadius: [0, 8, 8, 0] }, label: etiquetaPunta((p) => num(p.value)), cursor: "pointer" }]
  }), { replaceMerge: ["series"] });
  if (!graficos["g-of-temas"]._click) {
    g("g-of-temas").on("click", (p) => {
      const t = contar(ofFiltrados(true), (r) => r.temas)[p.dataIndex][0];
      S.ofTema = S.ofTema === t ? null : t; S.ofVer = 12; renderExplorar();
    });
    graficos["g-of-temas"]._click = true;
  }
  $("of-tema-activo").textContent = S.ofTema ? `Tema: ${cap1(S.ofTema)} · clic de nuevo para quitar` : "Haz clic en un tema para filtrar";
  const ev = ["oferta", "participación declarada", "demanda observada"].map((k) => [k, n((r) => r.evidencia === k)]);
  g("g-of-evidencia").setOption(opc({
    grid: { left: 16, right: 44, top: 6, bottom: 4, containLabel: true },
    xAxis: Object.assign(ejeVal(undefined, ""), { show: false }), yAxis: ejeCat(ev.map((x) => cap1(x[0]))),
    tooltip: { formatter: (p) => tt(p.name, [{ v: num(p.value), n: "actividades" }]) },
    series: [{ id: "e", type: "bar", barMaxWidth: 16, data: ev.map(([k, c]) => ({ value: c, itemStyle: { color: COLOR_EVIDENCIA[k] } })),
      itemStyle: { borderRadius: [0, 8, 8, 0] }, label: etiquetaPunta((p) => num(p.value)) }]
  }), { replaceMerge: ["series"] });
  const org = contar(f, (r) => r.tipo_organizador).slice(0, 5);
  g("g-of-organizador").setOption(opc({
    grid: { left: 16, right: 44, top: 6, bottom: 4, containLabel: true },
    xAxis: Object.assign(ejeVal(undefined, ""), { show: false }), yAxis: ejeCat(org.map((x) => cap1(x[0]))),
    tooltip: { formatter: (p) => tt(p.name, [{ v: num(p.value), n: "actividades" }]) },
    series: [{ id: "o", type: "bar", barMaxWidth: 16, data: org.map((x) => x[1]), itemStyle: { color: C.verde, borderRadius: [0, 8, 8, 0] }, label: etiquetaPunta((p) => num(p.value)) }]
  }), { replaceMerge: ["series"] });
  $("of-conteo").textContent = `${num(Math.min(S.ofVer, f.length))} de ${num(f.length)}`;
  $("of-lista").innerHTML = f.slice(0, S.ofVer).map((r) => tarjetaOferta(r)).join("") || `<p class="vacio">Ninguna actividad con estos filtros.</p>`;
  $("of-mas").hidden = f.length <= S.ofVer;
}
$("of-mas").addEventListener("click", () => { S.ofVer += 12; renderExplorar(); });
$("of-buscar").addEventListener("input", (ev) => { S.ofBuscar = ev.target.value; S.ofVer = 12; renderExplorar(); });

// ---------------------------------------------------------------- Para quién
const PUBLICOS = ["Jóvenes", "Niños y adolescentes", "Todo público", "Otro o no indica"];
const grupoPublico = (r) => (PUBLICOS.includes(r.publico) ? r.publico : "Otro o no indica");
function renderPublico() {
  const tot = PUBLICOS.map((p) => REG.filter((r) => grupoPublico(r) === p).length);
  $("of-pub-tiles").innerHTML = PUBLICOS.slice(0, 3).map((p, i) => tile({ clase: i === 0 ? "oscuro" : "", v: num(tot[i]),
    l: `para ${p.toLowerCase()} (${pct((100 * tot[i]) / REG.length, 0)} del total)` })).join("");
  const temas = contar(REG, (r) => r.temas).map((t) => t[0]);
  const series = PUBLICOS.map((p, i) => ({
    id: "s" + i, name: p, type: "bar", stack: "t", barMaxWidth: 20,
    data: temas.map((t) => REG.filter((r) => r.temas.includes(t) && grupoPublico(r) === p).length),
    itemStyle: { color: COLOR_PUBLICO[p] || C.gris, borderColor: "#fff", borderWidth: 2, borderRadius: redondeo(i, PUBLICOS.length) },
    label: { show: true, position: "inside", color: i === 2 || i === 3 ? C.tinta : "#fff", fontSize: 11, fontWeight: 600, formatter: (q) => (q.value >= 3 ? q.value : "") }
  }));
  g("g-of-publico").setOption(opc({
    grid: { left: 16, right: 16, top: 36, bottom: 6, containLabel: true }, legend: leyenda(PUBLICOS),
    xAxis: ejeVal(undefined, ""), yAxis: ejeCat(temas.map(cap1)),
    tooltip: { trigger: "axis", axisPointer: { type: "shadow", shadowStyle: { color: "rgba(23,22,28,.04)" } },
      formatter: (ps) => tt(ps[0].name, ps.map((q) => ({ color: q.color, n: q.seriesName, v: num(q.value) }))) },
    series
  }), { replaceMerge: ["series"] });
  const dep = REG.filter((r) => r.temas.includes("deporte")), depJ = dep.filter((r) => r.publico === "Jóvenes").length;
  const porTema = temas.map((t) => { const x = REG.filter((r) => r.temas.includes(t)); return { t, n: x.length, j: x.filter((r) => r.publico === "Jóvenes").length }; })
    .filter((x) => x.n >= 8).sort((a, b) => b.j / b.n - a.j / a.n);
  $("of-pub-lectura").innerHTML = `Solo <b>${num(tot[0])}</b> de ${num(REG.length)} actividades se dirigen a jóvenes; la mayor parte es para niños y adolescentes o para todo público. En deporte, <b>${num(depJ)}</b> de ${num(dep.length)} ${depJ === 1 ? "es" : "son"} para jóvenes. El tema con mayor proporción de oferta juvenil es <b>${esc(porTema[0].t)}</b> (${num(porTema[0].j)} de ${num(porTema[0].n)}).`;
}
TABLAS.ofPublico = () => { const temas = contar(REG, (r) => r.temas).map((t) => t[0]); return [["Tema"].concat(PUBLICOS, ["Total"]), temas.map((t) => [cap1(t)].concat(PUBLICOS.map((p) => num(REG.filter((r) => r.temas.includes(t) && grupoPublico(r) === p).length)), [num(REG.filter((r) => r.temas.includes(t)).length)]))]; };

// ---------------------------------------------------------------- Convocatoria
function renderConvocatoria() {
  const dec_ = REG.filter((r) => r.evidencia === "participación declarada"), dem = REG.filter((r) => r.evidencia === "demanda observada");
  $("of-conv-tiles").innerHTML = [
    tile({ v: num(dec_.length), l: "actividades publicaron cuánta gente participó" }),
    tile({ clase: "acento", v: num(dem.length), l: "tuvieron más interesados que cupos" }),
    tile({ v: num(REG.filter((r) => r.evidencia === "oferta").length), l: "solo anunciaron la actividad, sin cifras" })
  ].join("");
  $("of-demanda").innerHTML = dem.map((r) => `<article class="demanda">
      <div class="demanda-cifra">${r.cifra_n != null ? num(r.cifra_n) : "—"}</div>
      <h4>${esc(r.nombre)}</h4><p>${esc(r.senal || "")}</p>
      <div class="of-tags"><span class="tag-p" style="--c:${COLOR_PUBLICO[r.publico] || C.gris}">${esc(r.publico)}</span><span class="tag-s">${esc(r.distritos.join(" · "))} · ${r.anio}</span></div>
      ${r.url ? `<a class="of-fuente" href="${esc(r.url)}" target="_blank" rel="noopener">Ver fuente ↗</a>` : ""}</article>`).join("");
  const orden = dec_.slice().sort((a, b) => (b.cifra_n || -1) - (a.cifra_n || -1));
  $("of-participacion").innerHTML = orden.map((r) => tarjetaOferta(r, true)).join("");
}

// ---------------------------------------------------------------- Visibilidad
function renderVisibilidad() {
  const V = OF.visibilidad.slice().map((d) => ({ ...d, total: Object.values(d.por_anio).reduce((a, b) => a + b, 0) })).sort((a, b) => b.total - a.total);
  const anios = OF.anios_vis, colores = ["#a9b1f2", "#6a77e0", "#252f86"];
  g("g-of-visibilidad").setOption(opc({
    grid: { left: 16, right: 50, top: 36, bottom: 6, containLabel: true }, legend: leyenda(anios.map((a, i) => (i === anios.length - 1 ? `${a} (en curso)` : a))),
    xAxis: ejeVal(undefined, ""), yAxis: ejeCat(V.map((d) => d.corto)),
    tooltip: { trigger: "axis", axisPointer: { type: "shadow", shadowStyle: { color: "rgba(23,22,28,.04)" } },
      formatter: (ps) => tt(V[ps[0].dataIndex].nombre, ps.map((q) => ({ color: q.color, n: q.seriesName, v: num(q.value) })).concat([{ n: "Total", v: num(V[ps[0].dataIndex].total) }])) },
    series: anios.map((a, i) => ({ id: "s" + i, name: i === anios.length - 1 ? `${a} (en curso)` : a, type: "bar", stack: "t", barMaxWidth: 22,
      data: V.map((d) => d.por_anio[a] || 0), itemStyle: { color: colores[i % 3], borderColor: "#fff", borderWidth: 2, borderRadius: redondeo(i, anios.length) },
      label: i === anios.length - 1 ? { show: true, position: "right", color: C.tinta, fontWeight: 600, fontSize: 12, formatter: (p) => num(V[p.dataIndex].total) } : { show: false } }))
  }), { replaceMerge: ["series"] });
  const a = V[0], z = V[V.length - 1];
  $("of-vis-lectura").innerHTML = `<b>${esc(a.nombre)}</b> publicó <b>${num(a.total)}</b> notas con términos de juventud en 2024–2026; <b>${esc(z.nombre)}</b>, <b>${num(z.total)}</b>. La cantidad de notas depende de cuánto comunica cada municipalidad, no solo de cuánto organiza.`;
}
TABLAS.ofVisibilidad = () => [["Distrito"].concat(OF.anios_vis, ["Total"]), OF.visibilidad.map((d) => [d.nombre].concat(OF.anios_vis.map((a) => num(d.por_anio[a] || 0)), [num(Object.values(d.por_anio).reduce((x, y) => x + y, 0))]))];

Object.assign(RENDER, { explorar: renderExplorar, publico: renderPublico, convocatoria: renderConvocatoria, visibilidad: renderVisibilidad });
