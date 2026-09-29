/* Capa 1 · Contexto */
// ================================================================ POBLACIÓN
const P = D.contexto.poblacion;
const DIST = P.distritos.slice().sort((a, b) => b.jovenes - a.jovenes);

function heroContexto() {
  $("hero-contexto").innerHTML = `<div class="v">${mil(P.total.jovenes)}</div>
    <div class="l">jóvenes de 15 a 29 años viven en Lima Este (proyección ${P.anio}).</div>`;
}

function poblacionTiles() {
  const T = P.total, may = DIST[0];
  const cadaN = Math.round(100 / T.pct_joven);
  const edadMax = EDADES.reduce((a, b) => (T.pct_edad[b] > T.pct_edad[a] ? b : a));
  $("pob-tiles").innerHTML = [
    tile({ clase: "oscuro", v: pct(may.pct_de_lima_este), l: `de los jóvenes de Lima Este vive en ${esc(may.nombre)}`,
      s: `${num(may.jovenes)} jóvenes` }),
    tile({ v: pct(T.pct_mujeres), l: "son mujeres", s: `${pct(T.pct_hombres)} son hombres`,
      extra: `<div class="barrita"><i style="width:${T.pct_mujeres}%;background:${C.verde}"></i><i style="width:${T.pct_hombres}%;background:${C.indigo}"></i></div>
        <div class="leyenda-mini"><span><i style="background:${C.verde}"></i>Mujeres</span><span><i style="background:${C.indigo}"></i>Hombres</span></div>` }),
    tile({ v: pct(T.pct_edad[edadMax]), l: `tiene entre ${EDAD[edadMax].replace(" a ", " y ")} años, el grupo más grande`,
      extra: `<div class="barrita">${EDADES.map((e) => `<i style="width:${T.pct_edad[e]}%;background:${RAMPA[e]}"></i>`).join("")}</div>
        <div class="leyenda-mini">${EDADES.map((e) => `<span><i style="background:${RAMPA[e]}"></i>${EDAD[e]}: ${pct(T.pct_edad[e])}</span>`).join("")}</div>` }),
    tile({ v: pct(T.pct_joven), l: "de toda la población de Lima Este tiene entre 15 y 29 años",
      s: `Alrededor de 1 de cada ${cadaN} habitantes` })
  ].join("");
  $("pob-encuestas").textContent = `ENUT: ${mil(P.encuestas.enut)}; ENAPRES: ${mil(P.encuestas.enapres)}; ENAHO: ${mil(P.encuestas.enaho)}`;
}

function graficoDistritos() {
  const ch = g("g-distritos");
  const sel = S.distrito;
  const op = (d) => (!sel || d.nombre === sel ? 1 : 0.32);
  let series, eje, top = S.pobMet === "joven" ? 30 : 8, lect;
  if (S.pobMet === "peso" || S.pobMet === "joven") {
    const campo = S.pobMet === "peso" ? "pct_de_lima_este" : "pct_joven";
    series = [{
      id: "s0", name: S.pobMet === "peso" ? "Peso en Lima Este" : "Jóvenes en el distrito", type: "bar", barMaxWidth: 22,
      data: DIST.map((d) => ({ value: d[campo], itemStyle: { color: d.nombre === sel ? C.rojo : C.indigo, borderRadius: [0, 11, 11, 0], opacity: sel && d.nombre !== sel ? 0.55 : 1 } })),
      label: etiquetaPunta(), emphasis: { itemStyle: { color: C.rojo } },
      markLine: S.pobMet === "joven" ? {
        symbol: "none", silent: true, lineStyle: { color: C.tinta, width: 1.5, type: "solid" },
        label: { formatter: `Lima Este: ${pct(P.total.pct_joven)}`, position: "start", distance: 6, color: C.tinta2, fontSize: 11 },
        data: [{ xAxis: P.total.pct_joven }]
      } : undefined
    }];
    eje = ejeVal(S.pobMet === "peso" ? 50 : 30);
    if (S.pobMet === "peso") {
      const suma = DIST[0].pct_de_lima_este + DIST[1].pct_de_lima_este;
      lect = `<b>${esc(DIST[0].nombre)}</b> concentra <b>${pct(DIST[0].pct_de_lima_este)}</b> de los jóvenes de Lima Este. Junto con ${esc(DIST[1].nombre)} (<b>${pct(DIST[1].pct_de_lima_este)}</b>) suman <b>${pct(suma)}</b>: casi ${Math.round(suma / 10)} de cada 10.`;
    } else {
      const o = DIST.slice().sort((a, b) => b.pct_joven - a.pct_joven);
      lect = `En <b>${esc(o[0].nombre)}</b>, <b>${pct(o[0].pct_joven)}</b> de los habitantes son jóvenes; en <b>${esc(o[o.length - 1].nombre)}</b>, <b>${pct(o[o.length - 1].pct_joven)}</b>. En todo Lima Este, <b>${pct(P.total.pct_joven)}</b>.`;
    }
  } else if (S.pobMet === "sexo") {
    top = 34;
    series = [["mujer", "Mujeres", "pct_mujeres"], ["hombre", "Hombres", "pct_hombres"]].map(([k, n, campo], i) => ({
      id: "s" + i, name: n, type: "bar", stack: "t", barMaxWidth: 26,
      data: DIST.map((d) => ({ value: d[campo], itemStyle: { opacity: op(d) } })),
      itemStyle: { color: COLOR_SEXO[k], borderColor: "#fff", borderWidth: 2, borderRadius: redondeo(i, 2) },
      label: etiquetaDentro(8),
      markLine: i === 0 ? { symbol: "none", silent: true, lineStyle: { color: "#fff", width: 2, type: "solid" }, label: { show: false }, data: [{ xAxis: 50 }] } : undefined
    }));
    eje = ejeVal(100);
    const menos = DIST.filter((d) => d.pct_mujeres < 50);
    lect = menos.length === 0
      ? "En los siete distritos hay más mujeres que hombres jóvenes."
      : `Hay más mujeres que hombres jóvenes en todos los distritos, salvo en <b>${menos.map((d) => `${esc(d.nombre)}</b> (${pct(d.pct_mujeres)} mujeres)`).join(", <b>")}.`;
  } else {
    top = 34;
    series = EDADES.map((e, i) => ({
      id: "s" + i, name: EDAD[e] + " años", type: "bar", stack: "t", barMaxWidth: 26,
      data: DIST.map((d) => ({ value: d.pct_edad[e], itemStyle: { opacity: op(d) } })),
      itemStyle: { color: RAMPA[e], borderColor: "#fff", borderWidth: 2, borderRadius: redondeo(i, 3) },
      label: etiquetaDentro(8, i === 0 ? C.tinta : "#fff")
    }));
    eje = ejeVal(100);
    const todos = DIST.every((d) => d.pct_edad["25-29"] >= Math.max(d.pct_edad["15-19"], d.pct_edad["20-24"]));
    lect = todos
      ? `En los siete distritos, el grupo más numeroso es el de <b>25 a 29 años</b> (${pct(P.total.pct_edad["25-29"])} en Lima Este).`
      : "La distribución por edades varía entre distritos.";
  }
  ch.setOption(opc({
    grid: { left: 16, right: 64, top, bottom: 8, containLabel: true },
    legend: S.pobMet === "sexo" || S.pobMet === "edad" ? leyenda(series.map((s) => s.name)) : { show: false },
    xAxis: eje, yAxis: ejeCat(DIST.map((d) => d.corto)),
    tooltip: {
      formatter: (p) => {
        const d = DIST[p.dataIndex];
        if (S.pobMet === "peso") return tt(d.nombre, [{ v: pct(d.pct_de_lima_este), n: `de los jóvenes de Lima Este · ${num(d.jovenes)} jóvenes` }]);
        if (S.pobMet === "joven") return tt(d.nombre, [{ v: pct(d.pct_joven), n: `de la población del distrito tiene 15–29 años<br>${num(d.jovenes)} de ${num(d.poblacion_total)} habitantes` }]);
        if (S.pobMet === "sexo") return tt(d.nombre, [{ color: C.verde, n: "Mujeres", v: `${pct(d.pct_mujeres)} · ${num(d.mujeres)}` }, { color: C.indigo, n: "Hombres", v: `${pct(d.pct_hombres)} · ${num(d.hombres)}` }]);
        return tt(d.nombre, EDADES.map((e) => ({ color: RAMPA[e], n: EDAD[e] + " años", v: `${pct(d.pct_edad[e])} · ${num(d.edad[e])}` })));
      }
    },
    series
  }), { replaceMerge: ["series"] });
  $("pob-lectura").innerHTML = lect;
}

function ficha() {
  const T = P.total;
  const d = S.distrito ? P.distritos.find((x) => x.nombre === S.distrito) : T;
  const escala = 35;
  const chips = [["", "Lima Este"]].concat(DIST.map((x) => [x.nombre, x.corto]));
  $("ficha-distrito").innerHTML = `
    <div class="chips">${chips.map(([v, t]) => `<button class="chip" type="button" data-distrito="${esc(v)}" aria-pressed="${(S.distrito || "") === v}">${esc(t)}</button>`).join("")}</div>
    <div><div class="ficha-nombre">${esc(d.nombre === "Lima Este" ? "Lima Este (7 distritos)" : d.nombre)}</div></div>
    <div class="ficha-grande"><b>${num(d.jovenes)}</b><span>jóvenes de 15 a 29 años${S.distrito ? ` · <strong>${pct(d.pct_de_lima_este)}</strong> de Lima Este` : ""}</span></div>
    <div class="fila-dato">
      <div class="t"><span>Jóvenes en la población ${S.distrito ? "del distrito" : "total"}</span><b>${pct(d.pct_joven)}</b></div>
      <div class="pista"><i style="width:${(100 * d.pct_joven) / escala}%"></i>${S.distrito ? `<em style="left:${(100 * T.pct_joven) / escala}%" title="Lima Este: ${pct(T.pct_joven)}"></em>` : ""}</div>
      ${S.distrito ? `<div class="t"><small>La línea negra marca el promedio de Lima Este (${pct(T.pct_joven)})</small></div>` : ""}
    </div>
    <div class="fila-dato">
      <div class="t"><span>Mujeres y hombres</span></div>
      <div class="partida">
        <div style="flex-grow:${d.pct_mujeres};background:${C.verde}" title="${num(d.mujeres)} mujeres">Mujeres ${pct(d.pct_mujeres)}</div>
        <div style="flex-grow:${d.pct_hombres};background:${C.indigo}" title="${num(d.hombres)} hombres">Hombres ${pct(d.pct_hombres)}</div>
      </div>
    </div>
    <div class="fila-dato">
      <div class="t"><span>Edades</span></div>
      <div class="edades">${EDADES.map((e) => `<div class="edad" title="${num(d.edad[e])} jóvenes"><span>${EDAD[e]}</span><div class="b"><i style="width:${(100 * d.pct_edad[e]) / 45}%;background:${RAMPA[e]}"></i></div><b>${pct(d.pct_edad[e])}</b></div>`).join("")}</div>
    </div>`;
}
$("ficha-distrito").addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-distrito]");
  if (b) elegirDistrito(b.dataset.distrito || null);
});
function elegirDistrito(nombre) {
  S.distrito = nombre && S.distrito !== nombre ? nombre : null;  // volver a elegir el mismo distrito lo deselecciona
  graficoDistritos();
  ficha();
}

TABLAS.distritos = () => [
  ["Distrito", "Jóvenes", "% de Lima Este", "% de la población", "% mujeres", "% hombres", "15 a 19", "20 a 24", "25 a 29"],
  DIST.concat([P.total]).map((d) => [d.nombre, num(d.jovenes), pct(d.pct_de_lima_este), pct(d.pct_joven), pct(d.pct_mujeres),
    pct(d.pct_hombres)].concat(EDADES.map((e) => pct(d.pct_edad[e]))))
];

function renderPoblacion() {
  poblacionTiles();
  graficoDistritos();
  ficha();
  if (!graficos["g-distritos"]._click) {
    g("g-distritos").on("click", (p) => elegirDistrito(DIST[p.dataIndex].nombre));
    graficos["g-distritos"]._click = true;
  }
}

// ================================================================ ESTUDIO Y TRABAJO
const E = D.contexto.estudio;
const SIT = [["solo_estudia", "Solo estudia", C.indigo, "#fff"], ["estudia_y_trabaja", "Estudia y trabaja", C.indigo2, C.tinta],
  ["solo_trabaja", "Solo trabaja", C.verde, "#fff"], ["ni_estudia_ni_trabaja", "No estudia ni trabaja", C.rojo, "#fff"]];
const NIV = [["sin_secundaria", "No terminó la secundaria", C.rojoOsc, "#fff"], ["secundaria", "Solo secundaria completa", C.rojoClaro, C.tinta],
  ["tecnica", "Superior técnica", C.indigoClaro, C.tinta], ["universitaria", "Superior universitaria", C.indigo, "#fff"]];
const FILAS_EDAD = ["15-19", "20-24", "25-29", "15-29"];
const etqFila = (e) => (e === "15-29" ? "Todos (15 a 29)" : EDAD[e]);

function estudioTiles() {
  const A = E.asistencia[S.sexo][S.edad], N = E.nivel[S.sexo][S.edad];
  const lm = (e) => (e && e.v != null ? `Lima Metropolitana: ${est(e)}` : "");
  const junto = (...p) => p.filter(Boolean).join(" · ");
  $("est-tiles").innerHTML = [
    tile({ v: est(A.estudia), l: `de ${grupoTxt(S.sexo, S.edad)} estudia (colegio, instituto o universidad)`, s: junto(rango(A.estudia), lm(A.lm_estudia)), title: tituloEst(A.estudia) }),
    tile({ v: est(A.universidad), l: "está en la universidad", s: junto(rango(A.universidad), lm(A.lm_universidad)), title: tituloEst(A.universidad) }),
    tile({ v: est(A.instituto), l: "está en un instituto (superior técnica)", s: junto(A.instituto && A.instituto.v == null ? "Muestra insuficiente en Lima Este" : rango(A.instituto), lm(A.lm_instituto)), title: tituloEst(A.instituto) }),
    tile({ clase: "oscuro", v: est(N.sin_superior), l: "nunca llegó a la educación superior",
      s: S.edad === "15-19" ? "A esta edad muchos todavía están en el colegio."
        : S.edad === "15-29" ? `Incluye a quienes aún están en el colegio. Entre los de 25 a 29 años: ${est(E.nivel[S.sexo]["25-29"].sin_superior)}`
        : junto(rango(N.sin_superior), lm(N.lm_sin_superior)),
      title: tituloEst(N.sin_superior) })
  ].join("");
}

function apiladoEdades(id, fuente, categorias, lectId, lectFn, ejeDerecho) {
  const ch = g(id);
  const series = categorias.map(([k, n, color, texto], i) => ({
    id: "s" + i, name: n, type: "bar", stack: "t", barMaxWidth: 28,
    data: FILAS_EDAD.map((e) => {
      const x = fuente[S.sexo][e][k];
      return { value: val(x) || 0, est: x, itemStyle: { opacity: e === S.edad ? 1 : 0.5 } };
    }),
    itemStyle: { color, borderColor: "#fff", borderWidth: 2, borderRadius: redondeo(i, categorias.length) },
    label: etiquetaDentro(7, texto)
  }));
  const yAxis = [ejeCat(FILAS_EDAD.map(etqFila), {
    axisLabel: { color: C.tinta2, fontSize: 13, margin: 12, formatter: (v, i) => (FILAS_EDAD[i] === S.edad ? `{b|${v}}` : v), rich: { b: { fontWeight: 700, color: C.tinta, fontSize: 13 } } }
  })];
  if (ejeDerecho) yAxis.push(Object.assign(ejeCat(FILAS_EDAD.map((e) => ejeDerecho(e))), { position: "right", axisLabel: { color: C.tinta, fontSize: 12.5, fontWeight: 600, margin: 12 } }));
  ch.setOption(opc({
    grid: { left: 16, right: ejeDerecho ? 12 : 16, top: 36, bottom: 6, containLabel: true },
    legend: leyenda(categorias.map((c) => c[1])),
    xAxis: ejeVal(100), yAxis,
    tooltip: { formatter: (p) => tt(`${SEXO[S.sexo]} · ${etqFila(FILAS_EDAD[p.dataIndex])}`, [{ v: est(p.data.est), n: esc(p.seriesName) + "<br>" + detalleEst(p.data.est) }]) },
    series
  }), { replaceMerge: ["series", "yAxis"] });
  $(lectId).innerHTML = lectFn();
}

function lecturaSituacion() {
  const x = E.situacion[S.sexo][S.edad];
  let t = `De ${grupoTxt(S.sexo, S.edad)}: <b>${est(x.solo_estudia)}</b> solo estudia, <b>${est(x.estudia_y_trabaja)}</b> estudia y trabaja, <b>${est(x.solo_trabaja)}</b> solo trabaja y <b>${est(x.ni_estudia_ni_trabaja)}</b> no estudia ni trabaja${x.ni_estudia_ni_trabaja && x.ni_estudia_ni_trabaja.per ? ` (${rango(x.ni_estudia_ni_trabaja)})` : ""}.`;
  if (S.edad === "15-29") {
    const a = E.situacion[S.sexo]["15-19"], b = E.situacion[S.sexo]["25-29"];
    t += ` Con la edad el estudio da paso al trabajo: a los 15–19, <b>${est(a.solo_estudia)}</b> solo estudia; a los 25–29, <b>${est(b.solo_trabaja)}</b> solo trabaja.`;
  }
  return t;
}
function lecturaNivel() {
  const n = E.nivel[S.sexo][S.edad];
  let t = `<b>${est(n.sin_superior)}</b> de ${grupoTxt(S.sexo, S.edad)} nunca llegó a la educación superior: <b>${est(n.sin_secundaria)}</b> no terminó la secundaria y <b>${est(n.secundaria)}</b> solo la completó.`;
  if (S.edad === "15-19") t += " A esta edad muchos todavía están en el colegio o recién la terminaron.";
  if (S.edad === "15-29") {
    const m = E.nivel[S.sexo]["25-29"];
    t += ` Entre ${grupoTxt(S.sexo, "25-29")}, que ya pasaron la edad típica de estudio, la cifra es <b>${est(m.sin_superior)}</b>.`;
  }
  if (n.superior_completa && n.superior_completa.v != null && S.edad !== "15-19") t += ` <b>${est(n.superior_completa)}</b> ya terminó una carrera técnica o universitaria.`;
  return t;
}

function graficoDonde() {
  const A = E.asistencia[S.sexo][S.edad];
  const no = A.estudia && A.estudia.v != null ? { v: Math.round((100 - A.estudia.v) * 10) / 10, p: "c" } : null;
  const partes = [["Universidad", A.universidad, C.indigo], ["Instituto", A.instituto, C.indigo2], ["Colegio", A.escolar, C.indigo3], ["No estudia", no, C.gris]];
  g("g-donde").setOption(opc({
    legend: { show: true, orient: "vertical", right: 0, top: "middle", icon: "roundRect", itemWidth: 12, itemHeight: 12, itemGap: 14, selectedMode: false,
      textStyle: { color: C.tinta2, fontSize: 13, rich: { v: { fontWeight: 600, color: C.tinta, fontSize: 13, padding: [0, 0, 0, 6] } } },
      formatter: (n) => { const x = partes.find((p) => p[0] === n); return `${n} {v|${est(x[1])}}`; } },
    title: { text: est(A.estudia), subtext: "estudia", left: "31%", top: "40%", textAlign: "center",
      textStyle: { fontFamily: "Onest", fontSize: 26, fontWeight: 600, color: C.tinta }, subtextStyle: { fontSize: 13, color: C.tinta2 } },
    tooltip: { formatter: (p) => tt(`${SEXO[S.sexo]} · ${EDAD[S.edad]} años`, [{ v: est(p.data.est), n: esc(p.name) + (p.name === "No estudia" ? "" : "<br>" + detalleEst(p.data.est)) }]) },
    series: [{ id: "donde", type: "pie", center: ["32%", "50%"], radius: ["58%", "84%"], padAngle: 2, avoidLabelOverlap: true,
      itemStyle: { borderRadius: 10 }, label: { show: false }, emphasis: { scale: true, scaleSize: 5 },
      data: partes.map(([n, e, color]) => ({ name: n, value: val(e) || 0, est: e, itemStyle: { color } })) }]
  }));
  const hay = [[A.universidad, "van a la universidad"], [A.instituto, "a un instituto"], [A.escolar, "al colegio"]].filter(([e]) => e && e.v != null);
  const trozos = hay.map(([e, t], i) => `<b>${Math.round(e.v)}</b> ${i === 0 ? t : t.replace("van ", "")}`);
  const frase = trozos.length > 1 ? trozos.slice(0, -1).join(", ") + " y " + trozos[trozos.length - 1] : trozos[0] || "";
  const faltan = 3 - hay.length;
  $("est-donde-lectura").innerHTML = `De cada 100 ${S.sexo === "mujer" ? "mujeres" : S.sexo === "hombre" ? "hombres" : "jóvenes"} de ${EDAD[S.edad]} años, ${frase}.${faltan ? " Los demás niveles tienen una muestra muy pequeña para publicarlos." : ""}${A.lm_universidad && A.lm_universidad.v != null ? ` En Lima Metropolitana: ${est(A.lm_universidad)} en la universidad y ${est(A.lm_instituto)} en un instituto.` : ""}`;
}

const NINI = [["hogar", "Se dedica al hogar"], ["busca", "Busca trabajo"], ["quiere", "Quiere trabajar, pero no buscó"], ["estudiando", "Estudia fuera del sistema formal"]];
function graficoNini() {
  const n = E.nini[S.sexo];
  const total = E.situacion[S.sexo]["15-29"].ni_estudia_ni_trabaja;
  $("est-nini-cifra").innerHTML = `<b>${est(total)}</b><span>de ${grupoTxt(S.sexo, "15-29")} no estudia ni trabaja ${rango(total) ? `(${rango(total)})` : ""}</span>`;
  g("g-nini").setOption(opc({
    grid: { left: 16, right: 70, top: 4, bottom: 4, containLabel: true },
    xAxis: Object.assign(ejeVal(80), { show: false }), yAxis: ejeCat(NINI.map((x) => x[1])),
    tooltip: { formatter: (p) => tt(`${SEXO[S.sexo]} que no estudian ni trabajan`, [{ v: est(p.data.est), n: esc(p.name) + "<br>" + detalleEst(p.data.est) }]) },
    series: [{ id: "nini", type: "bar", barMaxWidth: 20, showBackground: true, backgroundStyle: { color: C.fondo2, borderRadius: 11 },
      data: NINI.map(([k]) => ({ value: val(n[k]) || 0, est: n[k], txt: est(n[k]) })),
      itemStyle: { color: C.rojo, borderRadius: 11 }, label: etiquetaPunta() }]
  }));
  const orden = NINI.filter(([k]) => n[k] && n[k].v != null).sort((a, b) => n[b[0]].v - n[a[0]].v);
  const VERBO = { hogar: "dedicarse al hogar", busca: "buscar trabajo", quiere: "querer trabajar sin haber buscado", estudiando: "estudiar fuera del sistema formal" };
  let t = `Lo más frecuente es <b>${VERBO[orden[0][0]]}</b> (<b>${est(n[orden[0][0]])}</b>).`;
  if (S.sexo === "mujer" && n.hogar_del_total) t += ` Las mujeres jóvenes dedicadas al hogar son <b>${est(n.hogar_del_total)}</b> de todas las mujeres de 15 a 29 años (${rango(n.hogar_del_total)}).`;
  if (S.sexo === "total") t += ` Entre las mujeres, el hogar pesa mucho más (${est(E.nini.mujer.hogar)}) que entre los hombres (${est(E.nini.hombre.hogar)}).`;
  if (S.edad !== "15-29") t += " <i>Este dato solo existe para todo el grupo de 15 a 29 años.</i>";
  $("est-nini-lectura").innerHTML = t;
}

function estudioTrabajo() {
  const x = E.empleo[S.sexo][S.edad], y = E.empleo[S.sexo]["15-29"];
  const solo = S.edad !== "15-29" ? " (dato para 15 a 29 años)" : "";
  $("est-trabajo").innerHTML = [
    tile({ v: est(x.desempleo), l: "de quienes trabajan o buscan trabajo está desempleado", s: "Tasa de desempleo · 2022–2025", title: tituloEst(x.desempleo) }),
    tile({ v: est(x.busca_trabajo), l: `de ${grupoTxt(S.sexo, S.edad)} busca trabajo`, s: rango(x.busca_trabajo), title: tituloEst(x.busca_trabajo) }),
    tile({ v: est(y.informal_ocupados), l: "de los jóvenes que trabajan tiene un empleo informal" + solo, s: "2022–2023 (el INEI no publicó la variable en 2024–2025)", title: tituloEst(y.informal_ocupados) }),
    tile({ v: est(y.independiente_ocupados), l: "de los que trabajan lo hace por cuenta propia o como empleador" + solo, s: "2022–2025", title: tituloEst(y.independiente_ocupados) })
  ].join("");
}

TABLAS.situacion = () => [["Edad"].concat(SIT.map((s) => s[1])), FILAS_EDAD.map((e) => [etqFila(e)].concat(SIT.map(([k]) => est(E.situacion[S.sexo][e][k]))))];
TABLAS.nivel = () => [["Edad"].concat(NIV.map((s) => s[1]), ["Sin educación superior", "Superior completa"]),
  FILAS_EDAD.map((e) => [etqFila(e)].concat(NIV.map(([k]) => est(E.nivel[S.sexo][e][k])), [est(E.nivel[S.sexo][e].sin_superior), est(E.nivel[S.sexo][e].superior_completa)]))];
TABLAS.donde = () => [["Grupo", "Estudia", "Universidad", "Instituto", "Colegio", "LM: estudia", "LM: universidad", "LM: instituto"],
  ["total", "mujer", "hombre"].flatMap((s) => FILAS_EDAD.map((e) => { const a = E.asistencia[s][e]; return [`${SEXO[s]} · ${etqFila(e)}`, est(a.estudia), est(a.universidad), est(a.instituto), est(a.escolar), est(a.lm_estudia), est(a.lm_universidad), est(a.lm_instituto)]; }))];
TABLAS.nini = () => [["Situación", "Todos", "Mujeres", "Hombres"], NINI.map(([k, n]) => [n, est(E.nini.total[k]), est(E.nini.mujer[k]), est(E.nini.hombre[k])])];

function renderEstudio() {
  estudioTiles();
  apiladoEdades("g-situacion", E.situacion, SIT, "est-sit-lectura", lecturaSituacion);
  graficoDonde();
  graficoNini();
  apiladoEdades("g-nivel", E.nivel, NIV, "est-nivel-lectura", lecturaNivel, (e) => `${est(E.nivel[S.sexo][e].sin_superior)} sin superior`);
  estudioTrabajo();
}

// ================================================================ SEGURIDAD
const G = D.contexto.seguridad;
const IND_SEG = [["noche_inseguro", "Se siente inseguro al caminar de noche"], ["evito_alguna", "Dejó de hacer alguna actividad"],
  ["evito_salir_noche", "Dejó de salir de noche"], ["evito_llegar_tarde", "Evitó llegar tarde a casa"]];

function seguridadTiles() {
  const n = G.noche_inseguro.le;
  $("seg-tiles").innerHTML = [
    tile({ clase: "oscuro", v: est(n.total), l: "de los jóvenes de Lima Este se siente inseguro al caminar solo de noche por su barrio", s: `Mujeres ${est(n.mujer)} · Hombres ${est(n.hombre)}`, title: tituloEst(n.total) }),
    tile({ v: est(G.evito_alguna.le.total), l: "dejó de hacer alguna actividad por temor a la delincuencia", s: rango(G.evito_alguna.le.total), title: tituloEst(G.evito_alguna.le.total) }),
    tile({ v: est(G.evito_salir_noche.le.total), l: "dejó de salir de noche", s: rango(G.evito_salir_noche.le.total), title: tituloEst(G.evito_salir_noche.le.total) }),
    tile({ v: est(G.noche_inseguro.lm.total), l: "se siente inseguro de noche en Lima Metropolitana, como referencia", title: tituloEst(G.noche_inseguro.lm.total) })
  ].join("");
}

function distintos(a, b) { return a && b && a.v != null && b.v != null && (a.lo > b.hi || b.lo > a.hi); }

function graficoSeguridad() {
  let grupos;
  if (S.segVista === "sexo") grupos = [["Mujeres", C.verde, (k) => G[k].le.mujer], ["Hombres", C.indigo, (k) => G[k].le.hombre]];
  else if (S.segVista === "lugar") grupos = [["Lima Este", C.rojo, (k) => G[k].le.total], ["Lima Metropolitana", C.gris2, (k) => G[k].lm.total]];
  else grupos = EDADES.concat(["30+"]).map((e) => [e === "30+" ? "Adultos (30 o más)" : EDAD[e] + " años", RAMPA[e], (k) => G[k].le[e]]);
  const series = grupos.map(([n, color, f], i) => ({
    id: "s" + i, name: n, type: "bar", barMaxWidth: 16, barGap: "30%",
    data: IND_SEG.map(([k]) => ({ value: val(f(k)) || 0, est: f(k), txt: est(f(k)) })),
    itemStyle: { color, borderRadius: [0, 8, 8, 0] }, label: etiquetaPunta()
  }));
  g("g-seguridad").setOption(opc({
    grid: { left: 16, right: 58, top: 36, bottom: 6, containLabel: true },
    legend: leyenda(grupos.map((x) => x[0])), xAxis: ejeVal(100), yAxis: ejeCat(IND_SEG.map((x) => x[1])),
    tooltip: { formatter: (p) => tt(IND_SEG[p.dataIndex][1], [{ v: est(p.data.est), n: esc(p.seriesName) + "<br>" + detalleEst(p.data.est) }]) },
    series
  }), { replaceMerge: ["series"] });
  const N = G.noche_inseguro;
  let t;
  if (S.segVista === "sexo") {
    t = distintos(N.le.mujer, N.le.hombre)
      ? `Las mujeres se sienten más inseguras de noche que los hombres: <b>${est(N.le.mujer)}</b> frente a <b>${est(N.le.hombre)}</b>.`
      : `Mujeres: <b>${est(N.le.mujer)}</b>; hombres: <b>${est(N.le.hombre)}</b>.`;
    const s = G.evito_salir_noche.le;
    if (distintos(s.mujer, s.hombre)) t += ` También dejan de salir de noche más a menudo (${est(s.mujer)} frente a ${est(s.hombre)}).`;
  }
  else if (S.segVista === "lugar") t = distintos(N.le.total, N.lm.total)
    ? `La inseguridad de noche en Lima Este (<b>${est(N.le.total)}</b>) es distinta a la de Lima Metropolitana (<b>${est(N.lm.total)}</b>).`
    : `Lima Este (<b>${est(N.le.total)}</b>) y Lima Metropolitana (<b>${est(N.lm.total)}</b>) están en niveles parecidos: la diferencia está dentro del margen de error.`;
  else {
    const v = EDADES.map((e) => val(N.le[e]));
    const sube = v[0] < v[1] && v[1] < v[2] && distintos(N.le["15-19"], N.le["25-29"]);
    t = sube ? `La inseguridad de noche aumenta con la edad: de <b>${est(N.le["15-19"])}</b> a los 15–19 a <b>${est(N.le["25-29"])}</b> a los 25–29 (adultos: ${est(N.le["30+"])}).`
      : `Inseguridad de noche: ${EDADES.map((e) => `${EDAD[e]}, <b>${est(N.le[e])}</b>`).join("; ")}.`;
    const ev = G.evito_alguna.le;
    if (distintos(ev["15-19"], ev["30+"])) t += ` Los de 15–19 dejan de hacer actividades más que los adultos (${est(ev["15-19"])} frente a ${est(ev["30+"])}).`;
  }
  $("seg-lectura").innerHTML = t;
}

function graficoCem() {
  const cem = G.cem, ch = g("g-cem");
  if (S.cemVista === "distrito") {
    const d = cem.distritos.slice().sort((a, b) => b.tasa - a.tasa);
    ch.setOption(opc({
      grid: { left: 16, right: 58, top: 30, bottom: 6, containLabel: true },
      xAxis: ejeVal(undefined, ""), yAxis: ejeCat(d.map((x) => x.corto)),
      tooltip: { formatter: (p) => tt(d[p.dataIndex].nombre, [{ v: dec(p.value), n: `casos por cada 10 000 jóvenes al año<br>${num(d[p.dataIndex].casos)} casos en 2022–2025` }]) },
      series: [{ id: "cem", type: "bar", barMaxWidth: 20, data: d.map((x) => ({ value: x.tasa, txt: dec(x.tasa) })),
        itemStyle: { color: C.indigo, borderRadius: [0, 11, 11, 0] }, label: etiquetaPunta(),
        markLine: { symbol: "none", silent: true, lineStyle: { color: C.tinta, width: 1.5, type: "solid" },
          label: { formatter: `Mediana de Lima Metropolitana: ${dec(cem.mediana_lm)}`, position: "start", distance: 6, color: C.tinta2, fontSize: 11 }, data: [{ xAxis: cem.mediana_lm }] } }]
    }), { replaceMerge: ["series", "xAxis", "yAxis"] });
    $("cem-lectura").innerHTML = `Por cada 10 000 jóvenes, los CEM atienden cada año unos <b>${dec(cem.tasa_le)}</b> casos en Lima Este (mediana de Lima Metropolitana: ${dec(cem.mediana_lm)}). La tasa más alta está en <b>${esc(d[0].nombre)}</b> (${dec(d[0].tasa)}) y la más baja en <b>${esc(d[d.length - 1].nombre)}</b> (${dec(d[d.length - 1].tasa)}).`;
  } else {
    const s = cem.serie;
    ch.setOption(opc({
      grid: { left: 4, right: 30, top: 16, bottom: 6, containLabel: true },
      xAxis: { type: "category", data: s.map((x) => x.anio), boundaryGap: false, axisLine: { lineStyle: { color: C.linea } }, axisTick: { show: false }, axisLabel: { color: C.tinta2 } },
      yAxis: { type: "value", min: 0, splitLine: { lineStyle: { color: C.linea } }, axisLabel: { color: C.tinta3, fontSize: 11, formatter: (v) => num(v) } },
      tooltip: { trigger: "axis", axisPointer: { type: "line", lineStyle: { color: C.tinta3 } }, formatter: (p) => tt(p[0].name, [{ v: num(p[0].value), n: "casos atendidos (15–29 años)" }]) },
      series: [{ id: "cem", type: "line", data: s.map((x) => x.casos), symbol: "circle", symbolSize: 9, lineStyle: { width: 2.5, color: C.indigo },
        itemStyle: { color: C.indigo, borderColor: "#fff", borderWidth: 2 }, areaStyle: { color: "rgba(59,76,192,.08)" },
        label: { show: true, position: "top", color: C.tinta2, fontSize: 11, formatter: (p) => (p.dataIndex === 0 || p.dataIndex === s.length - 1 ? num(p.value) : "") } }]
    }), { replaceMerge: ["series", "xAxis", "yAxis"] });
    const a = s[0], b = s[s.length - 1];
    $("cem-lectura").innerHTML = `En <b>${b.anio}</b> los CEM atendieron <b>${num(b.casos)}</b> casos de jóvenes de Lima Este; en ${a.anio}, ${num(a.casos)}. El mínimo fue en 2020 (${num((s.find((x) => x.anio === 2020) || {}).casos)}), año de la pandemia.`;
  }
}

TABLAS.seguridad = () => [["Indicador", "Lima Este", "Mujeres", "Hombres", "15 a 19", "20 a 24", "25 a 29", "30 o más", "Lima Metropolitana", "Periodo"],
  IND_SEG.map(([k, n]) => [n, est(G[k].le.total), est(G[k].le.mujer), est(G[k].le.hombre)].concat(EDADES.concat(["30+"]).map((e) => est(G[k].le[e])), [est(G[k].lm.total), G[k].periodo]))];
TABLAS.cem = () => [["Distrito", "Casos por 10 000 jóvenes al año", "Casos 2022–2025"], G.cem.distritos.map((d) => [d.nombre, dec(d.tasa), num(d.casos)]).concat([["Mediana de Lima Metropolitana", dec(G.cem.mediana_lm), ""]], G.cem.serie.map((x) => [`Lima Este, ${x.anio}`, "", num(x.casos)]))];

function renderSeguridad() { seguridadTiles(); graficoSeguridad(); graficoCem(); }

// ================================================================ ORGANIZACIONES
const O = D.contexto.organizaciones;
const CORTOS_TIPO = {
  "Organizaciones de estudiantes (escolar, universitario, tecnológico, artístico o pedagógico)": "De estudiantes",
  "Organizaciones de voluntariado": "De voluntariado", "Organizaciones de redes comunitarias o colectivos": "Redes comunitarias o colectivos",
  "Organización artística y/o cultural": "Artística o cultural", "Asociación civil sin fines de lucro en vías de formalización.": "Asociación civil en formalización",
  "Organizaciones territoriales": "Territoriales", "Acciones solidarias y altruistas": "Acciones solidarias",
  "Ciencia, tecnología y TICS": "Ciencia y tecnología", "Medioambiente y recursos naturales": "Medio ambiente",
  "Desarrollo social y/o económico": "Desarrollo social o económico", "Democracia y Derechos Humanos": "Democracia y derechos humanos"
};
const corto = (s) => CORTOS_TIPO[s] || (s.length > 34 ? s.slice(0, 33) + "…" : s);

function barrasSimples(id, items, opciones) {
  const o = opciones || {};
  g(id).setOption(opc({
    grid: { left: 16, right: o.derecha || 58, top: o.markLine ? 30 : 6, bottom: 4, containLabel: true },
    xAxis: Object.assign(ejeVal(o.max), { show: false }), yAxis: ejeCat(items.map((x) => x.n)),
    tooltip: { formatter: (p) => tt(items[p.dataIndex].n, [{ v: items[p.dataIndex].txt, n: items[p.dataIndex].nota || "" }]) },
    series: [{ id: "b", type: "bar", barMaxWidth: 18, showBackground: true, backgroundStyle: { color: C.fondo2, borderRadius: 10 },
      data: items.map((x) => ({ value: x.v, txt: x.txt, itemStyle: { color: x.color || o.color || C.indigo } })),
      itemStyle: { borderRadius: 10 }, label: etiquetaPunta(), markLine: o.markLine }]
  }), { replaceMerge: ["series"] });
}

function organizacionesEnaho() {
  const le = O.enaho.le, lm = O.enaho.lm;
  const edadMax = EDADES.reduce((a, b) => ((val(lm[b]) || 0) > (val(lm[a]) || 0) ? b : a));
  $("org-enaho-tiles").innerHTML = [
    tile({ clase: "acento", v: est(le.total), l: "de los jóvenes de Lima Este pertenece a alguna organización", title: tituloEst(le.total) }),
    tile({ v: est(lm.total), l: "en Lima Metropolitana", title: tituloEst(lm.total) }),
    tile({ v: `${est(lm.mujer)} · ${est(lm.hombre)}`, l: "mujeres y hombres (Lima Metropolitana)" }),
    tile({ v: est(lm[edadMax]), l: `a los ${EDAD[edadMax]} años, la edad en que más participan (Lima Metropolitana)` })
  ].join("");
  const tipos = lm.tipos.filter((t) => t.v != null).sort((a, b) => b.v - a.v);
  barrasSimples("g-org-tipos", tipos.map((t) => ({ n: t.nombre, v: t.v, txt: est(t), nota: detalleEst(t) })), { max: 40 });
  const papel = lm.papel.filter((t) => t.v != null).sort((a, b) => b.v - a.v);
  barrasSimples("g-org-papel", papel.map((t) => ({ n: t.nombre, v: t.v, txt: est(t), nota: detalleEst(t) })), { max: 100, color: C.verde });
}
TABLAS.orgEnaho = () => {
  const f = [["Pertenece a alguna organización", est(O.enaho.le.total), est(O.enaho.lm.total)],
    ["Mujeres", est(O.enaho.le.mujer), est(O.enaho.lm.mujer)], ["Hombres", est(O.enaho.le.hombre), est(O.enaho.lm.hombre)]]
    .concat(EDADES.map((e) => [EDAD[e] + " años", est(O.enaho.le[e]), est(O.enaho.lm[e])]))
    .concat(O.enaho.lm.tipos.map((t, i) => ["Tipo: " + t.nombre, est(O.enaho.le.tipos[i]), est(t)]))
    .concat(O.enaho.lm.papel.map((t, i) => ["Papel: " + t.nombre, est(O.enaho.le.papel[i]), est(t)]));
  return [["Indicador", "Lima Este", "Lima Metropolitana"], f];
};

function organizacionesRenoj() {
  const R = O.renoj;
  $("org-renoj-cifra").innerHTML = `<b>${num(R.total)}</b><span>organizaciones juveniles acreditadas en Lima Este entre ${R.anios[0]} y ${R.anios[1]}</span>`;
  const ch = g("g-renoj");
  let lect;
  if (S.renojVista === "anio") {
    const a = R.por_anio;
    ch.setOption(opc({
      grid: { left: 4, right: 12, top: 24, bottom: 6, containLabel: true },
      xAxis: { type: "category", data: a.map((x) => (x.anio === R.anios[1] ? `${x.anio}*` : String(x.anio))), axisLine: { lineStyle: { color: C.linea } }, axisTick: { show: false }, axisLabel: { color: C.tinta2 } },
      yAxis: { type: "value", splitLine: { lineStyle: { color: C.linea } }, axisLabel: { color: C.tinta3, fontSize: 11 } },
      tooltip: { formatter: (p) => tt(p.name.replace("*", " (año en curso)"), [{ v: num(p.value), n: "organizaciones acreditadas" }]) },
      series: [{ id: "b", type: "bar", barMaxWidth: 26, data: a.map((x) => x.n), itemStyle: { color: C.indigo, borderRadius: [10, 10, 0, 0] },
        label: { show: true, position: "top", color: C.tinta, fontWeight: 600, fontSize: 12 } }]
    }), { replaceMerge: ["series", "xAxis", "yAxis"] });
    lect = `Cada año se acreditan entre ${Math.min(...a.slice(1, -1).map((x) => x.n))} y ${Math.max(...a.map((x) => x.n))} organizaciones de Lima Este. * ${R.anios[1]}: año en curso.`;
  } else {
    let items, o = {};
    if (S.renojVista === "tipo") {
      items = R.tipo.map((x) => ({ n: corto(x.nombre), v: x.n, txt: num(x.n), nota: esc(x.nombre) }));
      lect = `Las más comunes son las <b>${corto(R.tipo[0].nombre).toLowerCase()}</b> y las <b>${corto(R.tipo[1].nombre).toLowerCase()}</b> (${num(R.tipo[0].n)} y ${num(R.tipo[1].n)}): juntas son ${pct((100 * (R.tipo[0].n + R.tipo[1].n)) / R.total, 0)} del total.`;
    } else if (S.renojVista === "tema") {
      items = R.tema.map((x) => ({ n: corto(x.nombre), v: x.n, txt: num(x.n), nota: esc(x.nombre) }));
      lect = `Por tema principal, destacan <b>${corto(R.tema[0].nombre).toLowerCase()}</b> (${num(R.tema[0].n)}), <b>${R.tema[1].nombre.toLowerCase()}</b> (${num(R.tema[1].n)}) e <b>${R.tema[2].nombre.toLowerCase()}</b> (${num(R.tema[2].n)}).`;
    } else {
      const d = R.distritos.slice().sort((a, b) => b.por_10mil - a.por_10mil);
      items = d.map((x) => ({ n: x.corto, v: x.por_10mil, txt: dec(x.por_10mil), nota: `por cada 10 000 jóvenes · ${num(x.n)} organizaciones` }));
      o = { markLine: { symbol: "none", silent: true, lineStyle: { color: C.tinta, width: 1.5, type: "solid" },
        label: { formatter: `Mediana de Lima Metropolitana: ${dec(R.mediana_lm)}`, position: "start", distance: 6, color: C.tinta2, fontSize: 11 }, data: [{ xAxis: R.mediana_lm }] } };
      lect = `Por cada 10 000 jóvenes, <b>${esc(d[0].nombre)}</b> tiene <b>${dec(d[0].por_10mil)}</b> organizaciones acreditadas; la mayoría de distritos está por debajo de la mediana de Lima Metropolitana (${dec(R.mediana_lm)}). SJL tiene más organizaciones (${num(R.distritos.find((x) => x.corto === "SJL").n)}), pero pocas para su tamaño.`;
    }
    barrasSimples("g-renoj", items, o);
  }
  $("renoj-lectura").innerHTML = lect;
}
TABLAS.renoj = () => {
  const R = O.renoj;
  return [["Grupo", "Categoría", "Organizaciones", "Por 10 000 jóvenes"],
    R.tipo.map((x) => ["Tipo", x.nombre, num(x.n), ""]).concat(R.tema.map((x) => ["Tema", x.nombre, num(x.n), ""]),
      R.distritos.map((x) => ["Distrito", x.nombre, num(x.n), dec(x.por_10mil)]), R.por_anio.map((x) => ["Año", String(x.anio), num(x.n), ""]))];
};

function organizacionesVoluntariado() {
  const V = O.voluntariado;
  $("org-vol-tiles").innerHTML = [
    tile({ v: num(V.inscritos), l: "jóvenes de Lima Este inscritos" }),
    tile({ v: pct(V.pct_mujeres), l: "son mujeres" }),
    tile({ clase: "acento", v: pct(V.participa_org_juvenil), l: "ya participa en una organización juvenil" }),
    tile({ v: pct(V.experiencia), l: "tiene alguna experiencia de voluntariado" })
  ].join("");
  const cap = (s) => s.charAt(0) + s.slice(1).toLowerCase();
  const lista = S.volVista === "experiencia" ? V.temas_experiencia : S.volVista === "interes" ? V.temas_interes : V.ocupacion.map((x) => ({ nombre: cap(x.nombre), pct: x.pct }));
  const nota = { experiencia: "de los inscritos tiene experiencia en este tema", interes: "de los inscritos dice tener interés en este tema", ocupacion: "de los inscritos" }[S.volVista];
  barrasSimples("g-voluntariado", lista.map((x) => ({ n: x.nombre, v: x.pct, txt: pct(x.pct), nota })), { max: 100, color: S.volVista === "ocupacion" ? C.indigo2 : C.verde });
}
TABLAS.voluntariado = () => {
  const V = O.voluntariado;
  return [["Grupo", "Categoría", "% de inscritos"], V.temas_experiencia.map((x) => ["Experiencia", x.nombre, pct(x.pct)])
    .concat(V.temas_interes.map((x) => ["Interés", x.nombre, pct(x.pct)]), V.ocupacion.map((x) => ["Ocupación", x.nombre, pct(x.pct)]), V.modalidad.map((x) => ["Modalidad", x.nombre, pct(x.pct)]))];
};

function renderOrganizaciones() { organizacionesEnaho(); organizacionesRenoj(); organizacionesVoluntariado(); }

// ================================================================ NATALIDAD
const N = D.contexto.natalidad;
function renderNatalidad() {
  const s = N.serie, a = s[0], b = s[s.length - 1];
  const cambio = (100 * (b.casos - a.casos)) / a.casos;
  const parcial = N.parcial[0];
  $("nat-tiles").innerHTML = [
    tile({ clase: "oscuro", v: num(b.casos), l: `nacimientos de madres de 15 a 19 años en ${b.anio}` }),
    tile({ v: (cambio < 0 ? "−" : "+") + dec(Math.abs(cambio), 0) + NB + "%", l: `frente a ${a.anio} (${num(a.casos)} nacimientos)` }),
    tile({ v: dec(N.tasa_le), l: "nacimientos por cada 1 000 mujeres de 15 a 19 años, cada año (2022–2025)", s: `Mediana de Lima Metropolitana: ${dec(N.mediana_lm)}` }),
    parcial ? tile({ v: num(parcial.casos), l: `nacimientos en ${parcial.periodo} de ${parcial.anio}`, s: "Datos parciales del año en curso" }) : ""
  ].join("");
  g("g-nat-serie").setOption(opc({
    grid: { left: 4, right: 30, top: 24, bottom: 6, containLabel: true },
    xAxis: { type: "category", data: s.map((x) => x.anio), boundaryGap: false, axisLine: { lineStyle: { color: C.linea } }, axisTick: { show: false }, axisLabel: { color: C.tinta2 } },
    yAxis: { type: "value", min: 0, splitLine: { lineStyle: { color: C.linea } }, axisLabel: { color: C.tinta3, fontSize: 11, formatter: (v) => num(v) } },
    tooltip: { trigger: "axis", axisPointer: { type: "line", lineStyle: { color: C.tinta3 } }, formatter: (p) => tt(p[0].name, [{ v: num(p[0].value), n: "nacimientos de madres de 15 a 19 años" }]) },
    series: [{ id: "nat", type: "line", data: s.map((x) => x.casos), symbol: "circle", symbolSize: 10, lineStyle: { width: 3, color: C.rojo },
      itemStyle: { color: C.rojo, borderColor: "#fff", borderWidth: 2 }, areaStyle: { color: { type: "linear", x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: "rgba(224,64,47,.18)" }, { offset: 1, color: "rgba(224,64,47,0)" }] } },
      label: { show: true, position: "top", distance: 10, color: C.tinta, fontWeight: 600, fontSize: 12, formatter: (p) => (p.dataIndex === 0 || p.dataIndex === s.length - 1 ? num(p.value) : "") } }]
  }));
  $("nat-serie-lectura").innerHTML = `Los nacimientos de madres adolescentes bajaron de <b>${num(a.casos)}</b> en ${a.anio} a <b>${num(b.casos)}</b> en ${b.anio}: <b>${dec(Math.abs(cambio), 0)} %</b> menos, cada año un poco menos.`;
  const d = N.distritos.slice().sort((x, y) => y.tasa - x.tasa);
  barrasSimples("g-nat-distritos", d.map((x) => ({ n: x.corto, v: x.tasa, txt: dec(x.tasa), nota: `por cada 1 000 mujeres de 15 a 19 años<br>${num(x.casos)} nacimientos en 2022–2025`, color: x.tasa > N.mediana_lm ? C.rojo : C.indigo3 })), {
    markLine: { symbol: "none", silent: true, lineStyle: { color: C.tinta, width: 1.5, type: "solid" },
      label: { formatter: `Mediana de Lima Metropolitana: ${dec(N.mediana_lm)}`, position: "start", distance: 6, color: C.tinta2, fontSize: 11 }, data: [{ xAxis: N.mediana_lm }] } });
  const sobre = d.filter((x) => x.tasa > N.mediana_lm);
  $("nat-dist-lectura").innerHTML = `En rojo, los distritos por encima de la mediana de Lima Metropolitana (${dec(N.mediana_lm)}): <b>${sobre.map((x) => esc(x.nombre)).join("</b>, <b>")}</b>. La tasa más alta es la de <b>${esc(d[0].nombre)}</b> (${dec(d[0].tasa)}); la más baja, la de ${esc(d[d.length - 1].nombre)} (${dec(d[d.length - 1].tasa)}).`;
}
TABLAS.natSerie = () => [["Año", "Nacimientos"], N.serie.map((x) => [String(x.anio), num(x.casos)]).concat(N.parcial.map((x) => [`${x.anio} (${x.periodo})`, num(x.casos)]))];
TABLAS.natDist = () => [["Distrito", "Tasa por 1 000", "Nacimientos 2022–2025", "Promedio anual"], N.distritos.map((x) => [x.nombre, dec(x.tasa), num(x.casos), num(x.promedio)]).concat([["Lima Este", dec(N.tasa_le), "", ""], ["Mediana de Lima Metropolitana", dec(N.mediana_lm), "", ""]])];

// ================================================================ DATOS EXTRA
function valorExtra(x, v) {
  if (v == null) return "—";
  if (x.unidad === "soles") return "S/" + NB + num(v);
  if (x.unidad === "años") return dec(v) + NB + "años";
  return pct(v);
}
function renderExtra() {
  const lista = D.contexto.extra.filter((x) => S.extraDim === "Todas" || x.dimension === S.extraDim);
  $("extra-grid").innerHTML = lista.map((x) => {
    const comp = [["Mujeres", x.mujeres, C.verde], ["Hombres", x.hombres, C.indigo], ["Perú", x.peru, C.gris2]].filter((c) => c[1] != null);
    const max = x.unidad === "%" ? 100 : Math.max(x.valor || 0, ...comp.map((c) => c[1])) * 1.1;
    const unidad = x.unidad === "%" ? "puntos" : x.unidad;
    const tend = x.cambio == null || x.cambio === 0 ? "" : `<span class="tend ${x.cambio > 0 ? "sube" : "baja"}">${dec(Math.abs(x.cambio))} ${unidad} desde ${x.anios.slice(0, 4)} · ${x.distinguible === "sí" ? "cambio claro" : "dentro del margen de error"}</span>`;
    const contexto = x.tablero && x.tablero.toLowerCase() !== x.indicador.toLowerCase() && !x.tablero.startsWith("fact") ? `<div class="ex-ctx">${esc(x.tablero)}</div>` : "";
    return `<article class="ex"><div class="ex-dim">${esc(x.dimension)}</div>${contexto}<h4>${esc(x.indicador)}</h4>
      <div class="v">${valorExtra(x, x.valor)}${x.referencial ? "*" : ""}<small>${esc(x.poblacion)} años · ${esc(x.anios.slice(-4))}</small></div>
      <div class="ex-comp">${comp.map(([n, v, c]) => `<div><span>${n}</span><span class="b"><i style="width:${Math.min(100, (100 * v) / max)}%;background:${c}"></i></span><b>${valorExtra(x, v)}</b></div>`).join("")}</div>
      ${tend}</article>`;
  }).join("") || `<p class="vacio">No hay indicadores en este tema.</p>`;
}


HERO.contexto = heroContexto;
Object.assign(RENDER, { poblacion: renderPoblacion, estudio: renderEstudio, seguridad: renderSeguridad,
  organizaciones: renderOrganizaciones, natalidad: renderNatalidad, extra: renderExtra });
