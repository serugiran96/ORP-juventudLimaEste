/* Observatorio · piezas comunes: datos, paleta, formato, gráficos, indicadores, controles y tablas. */
const D = JSON.parse(document.getElementById("datos").textContent);

// ---------------------------------------------------------------- Paleta (validada con el validador de dataviz)
// Sexo: verde/índigo · Situación: índigo, índigo claro, verde, rojo · Edad: rampa ordinal índigo
// Nivel alcanzado: dos familias (sin superior en rojos, con superior en índigos) · Contexto: gris.
const C = {
  rojo: "#e0402f", indigo: "#3b4cc0", indigo2: "#7f8ce6", indigo3: "#a9b1f2", verde: "#14a38b",
  gris: "#d7d3cd", gris2: "#b3aea7", tinta: "#17161c", tinta2: "#4a4852", tinta3: "#85828c", linea: "#ebe9e5",
  rojoOsc: "#b3261e", rojoClaro: "#f0998d", indigoClaro: "#9aa3ee", fondo2: "#f7f6f3"
};
const RAMPA = { "15-19": "#a9b1f2", "20-24": "#6a77e0", "25-29": "#252f86", "30+": "#b3aea7" };
const SEXO = { total: "Todos", mujer: "Mujeres", hombre: "Hombres" };
const COLOR_SEXO = { mujer: C.verde, hombre: C.indigo };
const EDAD = { "15-29": "15 a 29", "15-19": "15 a 19", "20-24": "20 a 24", "25-29": "25 a 29", "30+": "30 o más" };
const EDADES = ["15-19", "20-24", "25-29"];

// ---------------------------------------------------------------- Formato (coma decimal, espacio de miles)
const NB = " ", NNB = " ";
const dec = (v, d = 1) => Number(v).toFixed(d).replace(".", ",");
const pct = (v, d = 1) => (v == null ? "—" : dec(v, d) + NB + "%");
const num = (v) => (v == null ? "—" : Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, NNB));
const mil = (v) => num(Math.round(v / 1000)) + NB + "mil";
const est = (e, d = 1) => (!e || e.v == null ? "—" : pct(e.v, d) + (e.p === "r" ? "*" : ""));
const val = (e) => (e && e.v != null ? e.v : null);
const rango = (e) => (e && e.per ? "≈" + NB + num(e.per[0] / 1000) + "–" + mil(e.per[1]) : "");
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const $ = (id) => document.getElementById(id);

function grupoTxt(sexo, edad) {
  const quien = sexo === "mujer" ? "las mujeres" : sexo === "hombre" ? "los hombres" : "los jóvenes";
  return `${quien} de ${EDAD[edad]} años`;
}

// ---------------------------------------------------------------- Estado
const S = { tab: null };
const RENDER = {};
const HERO = {};
const CONTROLES = {};
Object.assign(S, { distrito: null, pobMet: "peso", sexo: "total", edad: "15-29",
  segVista: "sexo", cemVista: "distrito", renojVista: "tipo", volVista: "experiencia", extraDim: "Todas" });
Object.assign(CONTROLES, {
  pobMet: [["peso", "Peso en Lima Este"], ["sexo", "Mujeres y hombres"], ["edad", "Edades"], ["joven", "% jóvenes en el distrito"]],
  sexo: [["total", "Todos"], ["mujer", "Mujeres"], ["hombre", "Hombres"]],
  edad: [["15-29", "15 a 29"], ["15-19", "15 a 19"], ["20-24", "20 a 24"], ["25-29", "25 a 29"]],
  segVista: [["sexo", "Mujeres y hombres"], ["lugar", "Lima Este y Lima Metropolitana"], ["edad", "Por edad"]],
  cemVista: [["distrito", "Por distrito"], ["anio", "Por año"]],
  renojVista: [["tipo", "Tipo"], ["tema", "Tema"], ["distrito", "Distrito"], ["anio", "Año"]],
  volVista: [["experiencia", "Experiencia"], ["interes", "Interés"], ["ocupacion", "Ocupación"]],
  extraDim: [["Todas", "Todas"]].concat([...new Set(D.contexto.extra.map((d) => d.dimension))].map((d) => [d, d]))
});

// ---------------------------------------------------------------- ECharts: base común
const graficos = {};
function g(id) {
  if (!graficos[id]) {
    graficos[id] = echarts.init($(id), null, { renderer: "svg" });
  }
  return graficos[id];
}
const BASE = {
  textStyle: { fontFamily: "Onest, system-ui, sans-serif", color: C.tinta2 },
  animationDuration: 900, animationEasing: "cubicOut", animationDurationUpdate: 700, animationEasingUpdate: "cubicInOut",
  tooltip: {
    trigger: "item", confine: true, backgroundColor: "#fff", borderColor: C.linea, borderWidth: 1, padding: [10, 12],
    textStyle: { color: C.tinta, fontSize: 12 },
    extraCssText: "border-radius:14px;box-shadow:0 12px 32px -10px rgba(23,22,28,.28);"
  }
};
const opc = (o) => Object.assign({}, BASE, o, { tooltip: Object.assign({}, BASE.tooltip, o.tooltip || {}) });
const ejeCat = (data, extra) => Object.assign({
  type: "category", data, inverse: true, axisLine: { show: false }, axisTick: { show: false },
  axisLabel: { color: C.tinta2, fontSize: 13, margin: 12 }
}, extra || {});
const ejeVal = (max, suf = NB + "%") => ({
  type: "value", max, min: 0, splitNumber: 4, interval: max === 100 ? 25 : undefined, splitLine: { lineStyle: { color: C.linea } },
  axisLabel: { color: C.tinta3, fontSize: 11, formatter: (v) => dec(v, 0) + suf }
});
const leyenda = (items) => ({
  show: true, top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, itemGap: 16,
  textStyle: { color: C.tinta2, fontSize: 12.5 }, data: items, selectedMode: false
});
const redondeo = (i, n) => (n === 1 ? [0, 11, 11, 0] : i === 0 ? [11, 0, 0, 11] : i === n - 1 ? [0, 11, 11, 0] : 0);
const etiquetaDentro = (min, color) => ({
  show: true, position: "inside", fontSize: 12, fontWeight: 600, color: color || "#fff",
  formatter: (p) => (p.value >= min ? dec(p.value, 0) + NB + "%" : "")
});
const etiquetaPunta = (fmt) => ({
  show: true, position: "right", distance: 8, color: C.tinta, fontSize: 12.5, fontWeight: 600,
  formatter: fmt || ((p) => (p.data && p.data.txt) || pct(p.value))
});

function tt(titulo, filas, nota) {
  let h = `<div class="tt"><div class="tt-t">${esc(titulo)}</div>`;
  filas.forEach((f) => {
    h += f.color
      ? `<div class="tt-f"><i style="background:${f.color}"></i>${esc(f.n)}<b>${f.v}</b></div>`
      : `<div class="tt-v">${f.v}</div>${f.n ? `<div class="tt-s">${f.n}</div>` : ""}`;
  });
  if (nota) h += `<div class="tt-s">${nota}</div>`;
  return h + "</div>";
}
function detalleEst(e) {
  if (!e) return "";
  if (e.v == null) return "Muestra insuficiente para publicar la cifra";
  let s = `IC 95 %: ${dec(e.lo)}–${dec(e.hi)} %`;
  if (e.per) s += `<br>${rango(e)} jóvenes`;
  if (e.p === "r") s += `<br>* Referencial (CV ${dec(e.cv)} %)`;
  return s;
}

// ---------------------------------------------------------------- Piezas de interfaz
function tile(o) {
  return `<div class="tile ${o.clase || ""}"${o.title ? ` title="${esc(o.title)}"` : ""}>
    <div class="v">${o.v}</div><div class="l">${o.l}</div>${o.s ? `<div class="s">${o.s}</div>` : ""}${o.extra || ""}</div>`;
}
const tituloEst = (e) => (e && e.v != null ? `IC 95 %: ${dec(e.lo)}–${dec(e.hi)} % · n = ${num(e.n)}` : "");

function montarControles() {
  document.querySelectorAll("[data-ctrl]").forEach((cont) => {
    const clave = cont.dataset.ctrl;
    cont.innerHTML = CONTROLES[clave].map(([v, t]) => `<button type="button" data-v="${esc(v)}">${esc(t)}</button>`).join("");
    cont.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b || S[clave] === b.dataset.v) return;
      S[clave] = b.dataset.v;
      pintarControles();
      render(S.tab);
    });
  });
  pintarControles();
}
function pintarControles() {
  document.querySelectorAll("[data-ctrl]").forEach((cont) => {
    cont.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === S[cont.dataset.ctrl])));
  });
}

// Tablas ("Ver datos"): cada gráfico tiene su tabla equivalente.
const TABLAS = {};
function tablaHTML([cab, filas]) {
  return `<table><thead><tr>${cab.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${filas
    .map((f) => `<tr>${f.map((c, i) => `<td class="${i ? "n" : ""}">${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}
function refrescarTablas() {
  document.querySelectorAll("[data-tabla-de]").forEach((t) => {
    if (!t.hidden && TABLAS[t.dataset.tablaDe]) t.innerHTML = tablaHTML(TABLAS[t.dataset.tablaDe]());
  });
}
document.addEventListener("click", (ev) => {
  const b = ev.target.closest(".ver-datos");
  if (!b) return;
  const t = document.querySelector(`[data-tabla-de="${b.dataset.tabla}"]`);
  t.hidden = !t.hidden;
  b.setAttribute("aria-expanded", String(!t.hidden));
  b.textContent = t.hidden ? "Ver datos" : "Ocultar datos";
  if (!t.hidden) t.innerHTML = tablaHTML(TABLAS[b.dataset.tabla]());
});

