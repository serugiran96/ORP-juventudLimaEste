/* Actividades: ranking del modelo multicriterio (pesos ajustables), potencial frente a solidez, fichas y transversales */
const ALT = MOD.alternativas;
const FICHA = CR.fichas;
const COLOR_NIVEL = { "Mayor potencial": C.rojo, "Potencial medio": C.indigo2, "Menor respaldo hoy": C.gris2 };

Object.assign(S, { escenario: "recomendado", pesos: Object.assign({}, MOD.pesos.recomendado), ficha: null });
Object.assign(CONTROLES, { escenario: Object.entries(MOD.escenarios).concat([["personalizado", "Personalizado"]]) });

function ordenados() {
  return ALT.map((a) => ({ a, p: puntajeCon(a, S.pesos) })).sort((x, y) => y.p - x.p || x.a.ficha.localeCompare(y.a.ficha));
}

HERO.actividades = () => {
  const d = ordenados().filter((x) => nivelDe(x.p) === "Mayor potencial");
  $("hero-actividades").innerHTML = `<div class="v">${d.length} de ${ALT.length}</div>
    <div class="l">alternativas con mayor potencial de convocatoria: ${d.map((x) => `<b>${esc(altCorta(x.a).toLowerCase())}</b>`).join(" y ")}.</div>`;
};

// Texto con viñetas "• a • b" -> lista; barreras "[directa] …" -> lista con su pertinencia.
function vinetas(t) {
  if (!t) return "";
  const s = refTxt(t);
  if (!s.includes("•")) return `<p>${esc(s)}</p>`;
  return `<ul>${s.split("•").map((x) => x.trim()).filter(Boolean).map((x) => `<li>${esc(x)}</li>`).join("")}</ul>`;
}
function barreras(t) {
  if (!t) return "";
  const m = [...refTxt(t).matchAll(/\[(directa|indirecta|sin datos)\]\s*([^\[]+)/g)];
  if (!m.length) return `<p>${esc(refTxt(t))}</p>`;
  return `<ul class="barreras">${m.map((x) => `<li><span class="pb ${x[1].replace(" ", "-")}">${x[1]}</span>${esc(x[2].trim())}</li>`).join("")}</ul>`;
}

// ---------------------------------------------------------------- Resultado
function montarPesos() {
  $("pesos").innerHTML = CRIT.map((k) => `<label class="peso"><span><i style="background:${COLOR_CRIT[k.id]}"></i>${esc(k.nombre)}</span>
      <input type="range" min="0" max="3" step="1" value="${S.pesos[k.id]}" data-peso="${k.id}" aria-label="Peso de ${esc(k.nombre)}"><b>${S.pesos[k.id]}</b></label>`).join("");
}
function sincronizarPesos() {
  document.querySelectorAll("[data-peso]").forEach((el) => { el.value = S.pesos[el.dataset.peso]; el.nextElementSibling.textContent = S.pesos[el.dataset.peso]; });
}
$("pesos").addEventListener("input", (ev) => {
  const el = ev.target.closest("[data-peso]");
  if (!el) return;
  S.pesos[el.dataset.peso] = Number(el.value);
  el.nextElementSibling.textContent = el.value;
  S.escenario = "personalizado";
  pintarControles();
  renderResultado(true);
});
$("pesos-toggle").addEventListener("click", (ev) => {
  const p = $("pesos"); p.hidden = !p.hidden;
  ev.currentTarget.setAttribute("aria-expanded", String(!p.hidden));
  ev.currentTarget.textContent = p.hidden ? "Ajustar pesos" : "Ocultar pesos";
});

function renderResultado(desdePesos) {
  if (!desdePesos && S.escenario !== "personalizado") S.pesos = Object.assign({}, MOD.pesos[S.escenario]);
  if (!$("pesos").children.length) montarPesos();
  sincronizarPesos();
  const tot = CRIT.reduce((a, k) => a + S.pesos[k.id], 0) || 1;
  $("res-escenario").textContent = `Pesos: ${CRIT.map((k) => `${k.nombre} ${S.pesos[k.id]}`).join(" · ")}`;
  $("res-leyenda").innerHTML = CRIT.map((k) => `<span><i style="background:${COLOR_CRIT[k.id]}"></i>${esc(k.nombre)}</span>`).join("") +
    `<span class="corte">Cortes: 45 y 60 puntos</span>`;
  const cont = $("ranking");
  if (!cont.children.length) {
    cont.innerHTML = ALT.map((a) => `<div class="rk" data-ficha="${a.ficha}">
        <span class="rk-n"></span>
        <a class="rk-nombre" href="#${a.ficha}"><b>${esc(altCorta(a))}</b><small>${esc(a.linea)}</small></a>
        <div class="rk-barra">${CRIT.map((k) => `<i data-c="${k.id}" style="background:${COLOR_CRIT[k.id]}"></i>`).join("")}</div>
        <span class="rk-p"></span><span class="nivel"></span>
        <span class="rk-rango" title="Puesto en las cuatro combinaciones de pesos predefinidas">[${a.puesto_min === a.puesto_max ? a.puesto_min : `${a.puesto_min}–${a.puesto_max}`}]</span></div>`).join("");
  }
  const antes = {};
  cont.querySelectorAll(".rk").forEach((el) => { antes[el.dataset.ficha] = el.getBoundingClientRect().top; });
  const orden = ordenados();
  orden.forEach(({ a, p }, i) => {
    const el = cont.querySelector(`[data-ficha="${a.ficha}"]`);
    el.querySelector(".rk-n").textContent = i + 1;
    CRIT.forEach((k) => {
      const seg = el.querySelector(`[data-c="${k.id}"]`);
      const aporte = (100 * S.pesos[k.id] * a.puntajes[k.id]) / (3 * tot);
      seg.style.width = aporte + "%";
      seg.title = `${k.nombre}: ${a.puntajes[k.id]} de 3 (${a.datos[k.id]}) × peso ${S.pesos[k.id]} = ${dec(aporte)} puntos`;
    });
    el.querySelector(".rk-p").textContent = dec(p, 0);
    const nv = nivelDe(p), chip = el.querySelector(".nivel");
    chip.textContent = nv;
    chip.className = "nivel " + CLASE_NIVEL[nv];
    cont.appendChild(el);
  });
  // Animación FLIP: cada fila se desliza desde su posición anterior.
  cont.querySelectorAll(".rk").forEach((el) => {
    const dy = (antes[el.dataset.ficha] || 0) - el.getBoundingClientRect().top;
    if (antes[el.dataset.ficha] !== undefined && Math.abs(dy) > 1) {
      el.style.transition = "none"; el.style.transform = `translateY(${dy}px)`;
      requestAnimationFrame(() => { el.style.transition = "transform .55s cubic-bezier(.2,.7,.2,1)"; el.style.transform = ""; });
    }
  });
  const mayor = orden.filter((x) => nivelDe(x.p) === "Mayor potencial"), medio = orden.filter((x) => nivelDe(x.p) === "Potencial medio");
  const estables = ALT.filter((a) => a.puesto_max <= 2).map((a) => `<b>${esc(altCorta(a).toLowerCase())}</b>`);
  $("res-lectura").innerHTML = `${mayor.length ? `Con estos pesos, <b>${mayor.length}</b> alternativa${mayor.length > 1 ? "s tienen" : " tiene"} mayor potencial: ${mayor.map((x) => `<b>${esc(altCorta(x.a).toLowerCase())}</b>`).join(", ")}. ` : "Con estos pesos, ninguna alternativa llega a 60 puntos. "}${medio.length ? `Le siguen, con potencial medio, ${medio.map((x) => esc(altCorta(x.a).toLowerCase())).join(", ")}. ` : ""}${estables.length ? `En las cuatro combinaciones de pesos predefinidas, ${estables.join(" y ")} ${estables.length > 1 ? "quedan" : "queda"} entre los dos primeros puestos.` : ""}`;
  renderCuadrante(orden);
  refrescarTablas();
  if (HERO.actividades) HERO.actividades();
}
function renderCuadrante(orden) {
  // Rejilla: columnas = nivel de potencial; filas = solidez de la evidencia (alta: 85 % o más).
  const cols = [["Menor respaldo hoy", "Menos de 45 puntos"], ["Potencial medio", "45 a 60 puntos"], ["Mayor potencial", "60 puntos o más"]];
  const filas = [["alta", "Evidencia sólida", (x) => x.a.solidez >= 85], ["menor", "Evidencia menos sólida", (x) => x.a.solidez < 85]];
  const lema = { "alta|Mayor potencial": "Priorizar para un piloto", "alta|Potencial medio": "Buenas candidatas", "alta|Menor respaldo hoy": "Poco respaldo, bien medido",
    "menor|Mayor potencial": "Reforzar la evidencia", "menor|Potencial medio": "Validar primero", "menor|Menor respaldo hoy": "Explorar solo con consulta" };
  let h = `<div class="cu-grid"><span></span>${cols.map(([n, r]) => `<span class="cu-col"><b>${n}</b><small>${r}</small></span>`).join("")}`;
  filas.forEach(([k, nombre, f]) => {
    h += `<span class="cu-fila">${nombre}</span>`;
    cols.forEach(([n]) => {
      const xs = orden.filter((x) => f(x) && nivelDe(x.p) === n);
      h += `<div class="cu-celda ${CLASE_NIVEL[n]}${k === "alta" && n === "Mayor potencial" ? " destacada" : ""}"><span class="cu-lema">${lema[`${k}|${n}`]}</span>
        ${xs.map((x) => `<a class="cu-alt" href="#${x.a.ficha}"><b>${dec(x.p, 0)}</b>${esc(altCorta(x.a))}</a>`).join("") || `<span class="cu-vacia">—</span>`}</div>`;
    });
  });
  $("act-cuadrante").innerHTML = h + "</div>";
  const piloto = orden.filter((x) => x.p >= 60 && x.a.solidez >= 85), validar = orden.filter((x) => x.p >= 45 && x.a.solidez < 85);
  $("res-cuadrante").innerHTML = `${piloto.length ? `Con más respaldo y evidencia sólida: ${piloto.map((x) => `<b>${esc(altCorta(x.a).toLowerCase())}</b>`).join(" y ")}. Son las candidatas naturales a un primer piloto. ` : ""}${validar.length ? `Con potencial al menos medio pero evidencia menos sólida: ${validar.map((x) => esc(altCorta(x.a).toLowerCase())).join(", ")}; conviene reforzar la evidencia antes.` : ""}`;
}
TABLAS.ranking = () => [["Puesto", "Alternativa"].concat(CRIT.map((k) => k.nombre), ["Puntaje", "Nivel", "Rango de puestos", "Solidez"]),
  ordenados().map(({ a, p }, i) => [String(i + 1), altCorta(a)].concat(CRIT.map((k) => `${a.puntajes[k.id]} (${a.datos[k.id]})`), [dec(p, 0), nivelDe(p), `${a.puesto_min}–${a.puesto_max}`, `${a.solidez} %`]))];

// ---------------------------------------------------------------- Fichas
function renderFichas() {
  const orden = ordenados();
  if (!S.ficha || !FICHA[S.ficha]) S.ficha = orden[0].a.ficha;
  const grupos = MOD.niveles.map(([, n]) => [n, orden.filter((x) => nivelDe(x.p) === n)]);
  $("fichas-indice").innerHTML = grupos.map(([n, xs]) => xs.length ? `<div class="fi-grupo"><span class="nivel ${CLASE_NIVEL[n]}">${n}</span>${xs.map(({ a, p }) =>
    `<a class="fi${a.ficha === S.ficha ? " activo" : ""}" href="#${a.ficha}"><span class="fi-id">${a.ficha}</span><span class="fi-nom">${esc(altCorta(a))}</span><span class="fi-p">${dec(p, 0)}</span></a>`).join("")}</div>` : "").join("") +
    `<div class="fi-grupo"><span class="nivel n0">No se puntúan</span>${["F-13", "F-15"].map((id) => `<a class="fi${id === S.ficha ? " activo" : ""}" href="#${id}"><span class="fi-id">${id}</span><span class="fi-nom">${esc(FICHA[id].actividad.replace(/:.*$/, ""))}</span></a>`).join("")}</div>`;
  const f = FICHA[S.ficha], a = ALT.find((x) => x.ficha === S.ficha);
  const x = a ? orden.find((o) => o.a.ficha === a.ficha) : null;
  const criterios = a ? `<div class="fd-crit">${CRIT.map((k) => `<div class="fd-c"><span class="fd-cn"><i style="background:${COLOR_CRIT[k.id]}"></i>${esc(k.nombre)}</span>
      <span class="fd-dots" style="color:${COLOR_CRIT[k.id]}">${puntos(a.puntajes[k.id])}</span><span class="fd-dato">${esc(a.datos[k.id])}</span></div>`).join("")}</div>` : "";
  const regs = f.registros.length ? `<table class="tabla-mini"><thead><tr><th>Código</th><th>Actividad registrada</th><th>Cifra</th></tr></thead><tbody>${f.registros.map((r) =>
    `<tr><td><span class="cod">${esc(r.codigo)}</span></td><td>${esc(r.nombre)}<small>${esc(r.distrito)} · ${esc(r.publico)}</small></td><td>${r.cifra != null ? `${num(r.cifra)} ${esc(r.cifra_tipo || "")}` : esc(r.nota || "")}</td></tr>`).join("")}</tbody></table>` : "<p>No se encontraron actividades comparables con datos para jóvenes (sin evidencia, que no es evidencia negativa).</p>";
  const comp = (estados) => f.componentes.filter((c) => estados.includes(c.estado));
  const compHTML = [["Con respaldo", ["respaldado en dos o más dimensiones", "respaldado en una dimensión"]],
    ["Por validar", ["solo señales débiles", "hipótesis de diseño", "sin evidencia"]],
    ["Ya existe, transversal o descartado", ["complementario (ya existe)", "condición transversal", "descartado"]]]
    .map(([t, es]) => `<div class="fd-comp"><span>${t}</span>${comp(es).map((c) => `<p class="${c.estado === "descartado" ? "tachado" : ""}"><b>${esc(c.componente)}</b><small>${esc(c.estado)}. ${esc(refTxt(c.nota || ""))}</small></p>`).join("") || "<p><small>—</small></p>"}</div>`).join("");
  $("ficha-detalle").innerHTML = `
    <div class="fd-cab">
      <div class="fd-tags"><span class="m-id">${f.id}</span><span class="tag-s">${esc(f.linea)}</span><span class="tag-s">${esc(f.tipo_ficha)}</span>
        ${x ? `<span class="nivel ${CLASE_NIVEL[nivelDe(x.p)]}">${nivelDe(x.p)} · ${dec(x.p, 0)} puntos</span><span class="tag-s">Puesto ${a.puesto_min === a.puesto_max ? a.puesto_min : `${a.puesto_min} a ${a.puesto_max}`} según los pesos</span>` : `<span class="nivel n0">No se puntúa</span>`}</div>
      <h3>${esc(f.actividad)}</h3>
    </div>
    ${criterios}
    <div class="fd-secciones">
      <section><h4>Para quién</h4><p>${esc(refTxt(f.poblacion))}</p>${f.alcance ? `<p class="meta">${esc(refTxt(f.alcance))}</p>` : ""}</section>
      <section><h4>Qué sabemos</h4><p>${esc(refTxt(f.necesidad))}</p>${vinetas(f.afirmaciones)}</section>
      <section><h4>Práctica o interés</h4><p>${esc(refTxt((f.interes || "").replace(/^\[[^\]]+\]\s*/, "").replace(/\s*Salto inferencial:.*$/, "")))}</p>${f.salto_inferencial ? `<p class="salto"><b>Salto que falta probar:</b> ${esc(f.salto_inferencial)}</p>` : ""}</section>
      <section><h4>Cómo convocar</h4>${barreras(f.barreras)}<p class="meta">Además, las <a href="#criterios">condiciones comunes</a>: gratis, horario de domingo por la tarde o sábado por la noche, lugar seguro y difusión con tiempo.</p></section>
      <section class="fd-ancha"><h4>Convocatoria observada en actividades parecidas</h4>${f.convocatoria_detalle_codigo ? `<p class="meta">${esc(f.convocatoria_detalle_codigo)}</p>` : ""}${regs}<p class="meta"><b>Oferta existente:</b> ${esc(f.oferta || "—")}</p></section>
      <section class="fd-validar fd-ancha"><h4>Qué falta validar con los jóvenes</h4>
        <div class="rejilla-3"><div><b>No sabemos</b>${vinetas(f.vacios)}</div><div><b>Hipótesis a probar</b>${f.hipotesis && f.hipotesis !== "No aplica." ? vinetas(f.hipotesis) : "<p>No aplica.</p>"}</div>
        <div><b>Qué medir en un piloto</b><p>${esc(f.validacion_piloto || "—")}</p><b>Dónde empezar</b><p>${esc(f.donde || "—")}</p></div></div></section>
      <section class="fd-ancha"><h4>Componentes</h4><div class="rejilla-3">${compHTML}</div></section>
    </div>
    <p class="fd-ev">Evidencias: ${lista(f.evidencias).map((e) => `<span class="m-id">${e}</span>`).join(" ")}</p>`;
}
const lista = (s) => (s ? String(s).split(";").map((x) => x.trim()).filter(Boolean) : []);

// ---------------------------------------------------------------- Transversales
function renderTransversal() {
  $("transversales").innerHTML = ["F-13", "F-15"].map((id) => {
    const f = FICHA[id];
    return `<article class="card"><div class="fd-tags"><span class="m-id">${id}</span><span class="tag-s">${esc(f.tipo_ficha)}</span></div>
      <h3 class="tr-t">${esc(f.actividad)}</h3>
      <p><b>Por qué:</b> ${esc(refTxt(f.necesidad))}</p><p><b>A quién:</b> ${esc(refTxt(f.poblacion))}</p>
      <div><b>Barreras</b>${barreras(f.barreras)}</div>
      <p><b>Qué hacer:</b> ${esc(f.validacion_piloto || "")}</p>
      <div><b>No sabemos</b>${vinetas(f.vacios)}</div>
      <a class="of-fuente" href="#${id}">Ver ficha completa →</a></article>`;
  }).join("");
}

Object.assign(RENDER, { resultado: () => renderResultado(false), fichas: renderFichas, transversal: renderTransversal });
