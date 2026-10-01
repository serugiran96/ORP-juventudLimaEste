/* Actividades: ranking de actividades y de servicios por público, fichas y transversales */
const FICHA = CR.fichas;
const listaTxt = (s) => (s ? String(s).split(";").map((x) => x.trim()).filter(Boolean) : []);

Object.assign(S, { pSexo: "total", pEdad: "todas", ficha: null });
Object.assign(CONTROLES, {
  pSexo: [["total", "Todos"], ["mujer", "Mujeres"], ["hombre", "Hombres"]],
  pEdad: [["todas", "15 a 29"], ["15-19", "15 a 19"], ["20-24", "20 a 24"], ["25-29", "25 a 29"]]
});

const pubsSel = () => filtrarPublicos(S.pSexo, S.pEdad);
const todosSel = () => S.pSexo === "total" && S.pEdad === "todas";
const quienSel = () => `${S.pSexo === "mujer" ? "las mujeres" : S.pSexo === "hombre" ? "los hombres" : "los jóvenes"} de ${S.pEdad === "todas" ? "15 a 29" : EDAD[S.pEdad]} años`;
function ordenGrupo(g, pubs) {
  return TIPOS.filter((t) => t.grupo === g && t.medido).map((t) => Object.assign({ t }, convDe(t, pubs)))
    .sort((a, b) => b.tot - a.tot || a.t.id.localeCompare(b.t.id));
}
const pctMujeres = (t, pubs) => { const c = convDe(t, pubs), m = convDe(t, pubs.filter((p) => p.sexo === "mujer")); return c.tot ? (100 * m.tot) / c.tot : null; };
const nombre = (t) => `<b>${esc(t.tipo.toLowerCase())}</b>`;
const mayus = (h) => h.replace(/^(<b>)?(.)/, (m, b, l) => (b || "") + l.toUpperCase());

HERO.actividades = () => {
  const a = ordenGrupo("actividad", PUB)[0], s = ordenGrupo("servicio", PUB)[0];
  $("hero-actividades").innerHTML = `<div class="v">${milC(a.tot)}</div>
    <div class="l">jóvenes podría convocar ${nombre(a.t)}, la actividad con más alcance. Entre los servicios, ${nombre(s.t)} (${milC(s.tot)}).</div>`;
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

// ---------------------------------------------------------------- Resultado: dos rankings (actividades y servicios)
function renderRanking(cont, g) {
  const pubs = pubsSel(), orden = ordenGrupo(g, pubs), max = orden[0].tot || 1, todos = todosSel();
  if (!cont.children.length) {
    cont.innerHTML = orden.map(({ t }) => `<div class="rk" data-id="${t.id}">
      <span class="rk-n"></span>
      <a class="rk-nombre" href="#${t.id}"><b>${esc(t.tipo)}</b><small></small></a>
      <div class="rk-barra"><i class="rk-ya" style="background:${COLOR_YA}"></i><i class="rk-fr" style="background:${COLOR_FR}"></i></div>
      <span class="rk-p"></span><span class="rk-rango"></span></div>`).join("");
  }
  const antes = {};
  cont.querySelectorAll(".rk").forEach((el) => { antes[el.dataset.id] = el.getBoundingClientRect().top; });
  orden.forEach(({ t, ya, fr, tot }, i) => {
    const el = cont.querySelector(`[data-id="${t.id}"]`);
    el.querySelector(".rk-n").textContent = i + 1;
    const p = principalDe(t, pubs), m = pctMujeres(t, pubs);
    el.querySelector("small").innerHTML = tot ? `Más convoca a ${esc(pubCorto(p).toLowerCase())}${S.pSexo === "total" && m != null ? ` · ${pct(m, 0)} mujeres` : ""}${t.fren_medidos ? "" : " · frenados sin medir"}` : "Sin dato para este público";
    const sy = el.querySelector(".rk-ya"), sf = el.querySelector(".rk-fr");
    sy.style.width = (100 * ya) / max + "%"; sf.style.width = (100 * fr) / max + "%";
    sy.title = `Ya la hacen y tienen tiempo: ${num(ya)}`;
    sf.title = t.fren_medidos ? `Frenados por dinero, información u oferta, con tiempo: ${num(fr)}` : "Frenados: ninguna encuesta los mide";
    el.querySelector(".rk-p").textContent = milC(tot);
    const r = el.querySelector(".rk-rango");
    r.textContent = todos ? `[${t.plo === t.phi ? t.plo : `${t.plo}–${t.phi}`}]` : "";
    r.title = "Puestos posibles con el margen de error de las encuestas";
    cont.appendChild(el);
  });
  cont.querySelectorAll(".rk").forEach((el) => {
    const dy = (antes[el.dataset.id] || 0) - el.getBoundingClientRect().top;
    if (antes[el.dataset.id] !== undefined && Math.abs(dy) > 1) {
      el.style.transition = "none"; el.style.transform = `translateY(${dy}px)`;
      requestAnimationFrame(() => { el.style.transition = "transform .55s cubic-bezier(.2,.7,.2,1)"; el.style.transform = ""; });
    }
  });
  return orden;
}

function renderResultado() {
  const ley = `<span><i style="background:${COLOR_YA}"></i>Ya la hacen</span><span><i style="background:${COLOR_FR}"></i>Frenados por dinero, información o falta de oferta</span>`;
  $("res-leyenda").innerHTML = ley; $("serv-leyenda").innerHTML = ley;
  $("res-quien").textContent = `Jóvenes convocables: ${quienSel()}`;
  const pubs = pubsSel();
  // Actividades
  const oa = renderRanking($("rk-act"), "actividad");
  const [a, b, c] = oa;
  let txt = `Para ${quienSel()}, las actividades con más jóvenes convocables son ${nombre(a.t)} (${milC(a.tot)}), ${nombre(b.t)} (${milC(b.tot)}) y ${nombre(c.t)} (${milC(c.tot)}).`;
  if (a.fr / a.tot >= 0.3) txt += ` En ${nombre(a.t)}, ${pct((100 * a.fr) / a.tot, 0)} son jóvenes frenados por dinero, información o falta de oferta: se suman si es gratis, cerca y se difunde bien.`;
  if (S.pSexo === "total") {
    const top = oa.slice(0, 9);
    const hom = top.filter((x) => pctMujeres(x.t, pubs) < 35).map((x) => nombre(x.t));
    const muj = top.filter((x) => pctMujeres(x.t, pubs) >= 57).map((x) => nombre(x.t));
    if (hom.length) txt += ` ${mayus(yLista(hom))} ${hom.length > 1 ? "convocan" : "convoca"} sobre todo a hombres`;
    if (muj.length) txt += hom.length ? `; ${yLista(muj)}, a más mujeres` : ` ${mayus(yLista(muj))} ${muj.length > 1 ? "convocan" : "convoca"} a más mujeres`;
    if (hom.length || muj.length) txt += ".";
  }
  $("res-lectura").innerHTML = txt;
  // Servicios
  const os = renderRanking($("rk-serv"), "servicio");
  const c4 = os.filter((x) => x.t.conv.codigo === "C4").map((x) => nombre(x.t));
  $("serv-lectura").innerHTML = `Para ${quienSel()}, el servicio con más jóvenes convocables es ${nombre(os[0].t)} (${milC(os[0].tot)}).${S.pEdad === "25-29" ? " La preparación para la educación superior no tiene dato para 25 a 29 años: la encuesta pregunta por qué no estudian solo hasta los 24." : ""} ${c4.length ? `${mayus(yLista(c4))} ya ${c4.length > 1 ? "tuvieron" : "tuvo"} más interesados que cupos en Lima Este.` : ""}`;
  // Sin datos
  $("sin-datos").innerHTML = TIPOS.filter((t) => !t.medido).map((t) => `<a class="chip-sd" href="#${t.id}"><span class="m-id">${t.id}</span>${esc(t.tipo)}<small>${t.grupo === "servicio" ? "servicio" : "actividad"}</small></a>`).join("");
  refrescarTablas();
  if (HERO.actividades) HERO.actividades();
}
const tablaRanking = (g) => () => {
  const todos = todosSel();
  return [["Puesto", "Tipo", "Ya la hacen", "Frenados", "Jóvenes convocables"].concat(todos ? ["Rango con margen de error", "Puestos posibles"] : []).concat(["Público que más convoca"]),
    ordenGrupo(g, pubsSel()).map(({ t, ya, fr, tot }, i) => [String(i + 1), t.tipo, num(ya), t.fren_medidos ? num(fr) : "sin medir", num(tot)]
      .concat(todos ? [`${num(t.lo)}–${num(t.hi)}`, `${t.plo}–${t.phi}`] : []).concat([tot ? pubCorto(principalDe(t, pubsSel())) : "—"]))];
};
TABLAS.rkAct = tablaRanking("actividad");
TABLAS.rkServ = tablaRanking("servicio");

// ---------------------------------------------------------------- Fichas
function renderFichas() {
  const oa = ordenGrupo("actividad", PUB), os = ordenGrupo("servicio", PUB);
  if (!S.ficha || (!TIPOS.find((t) => t.id === S.ficha) && !FICHA[S.ficha])) S.ficha = oa[0].t.id;
  if (/^F-/.test(S.ficha) && !["F-13", "F-15"].includes(S.ficha)) { const t = TIPOS.find((x) => x.ficha === S.ficha); if (t) S.ficha = t.id; }
  const it = (id, nom, v) => `<a class="fi${id === S.ficha ? " activo" : ""}" href="#${id}"><span class="fi-id">${id}</span><span class="fi-nom">${esc(nom)}</span><span class="fi-p">${v}</span></a>`;
  const grupo = (titulo, clase, items) => `<div class="fi-grupo"><span class="nivel ${clase}">${titulo}</span>${items}</div>`;
  $("fichas-indice").innerHTML =
    grupo("Actividades · miles", "n2", oa.map((x) => it(x.t.id, x.t.tipo, Math.round(x.tot / 1000))).join("")) +
    grupo("Servicios · miles", "n2", os.map((x) => it(x.t.id, x.t.tipo, Math.round(x.tot / 1000))).join("")) +
    grupo("Sin datos para ordenar", "n0", TIPOS.filter((t) => !t.medido).map((t) => it(t.id, t.tipo, "")).join("")) +
    grupo("Protocolo y consulta", "n0", ["F-13", "F-15"].map((id) => it(id, FICHA[id].actividad.replace(/:.*$/, ""), "")).join(""));
  const t = TIPOS.find((x) => x.id === S.ficha);
  $("ficha-detalle").innerHTML = t ? detalleTipo(t) : detalleFicha(FICHA[S.ficha], null);
}

function detalleTipo(t) {
  const n = ordenGrupo(t.grupo, PUB).length, serv = t.grupo === "servicio";
  const tags = `<span class="m-id">${t.id}</span><span class="tag-s">${serv ? "Servicio" : "Actividad"}</span><span class="tag-s">${esc(t.linea)}</span>` +
    (t.medido ? `<span class="nivel n2">Puesto ${t.puesto} de ${n} ${serv ? "servicios" : "actividades"}</span>` : `<span class="nivel n0">No se ordena</span>`);
  const cab = `<div class="fd-cab"><div class="fd-tags">${tags}</div><h3>${esc(t.tipo)}</h3><p class="fd-formato"><b>Formato propuesto:</b> ${esc(t.formato)}</p></div>`;
  const validar = `<section class="fd-validar fd-ancha"><h4>Qué falta validar con los jóvenes</h4>
      <div class="rejilla-3"><div><b>Participación</b><p>Ninguna encuesta preguntó si participarían en este formato. Validar con consulta directa: qué formato, horario y lugar.</p></div>
      <div><b>Permanencia</b><p>Que la gente vuelva: en un piloto, medir cuántos asisten a 3 o más sesiones y cuántos siguen a los 3 meses.</p></div>
      <div><b>Convocatoria</b><p>Inscritos frente a cupos, por edad y sexo, y lista de espera.</p></div></div></section>`;
  const basicos = ["solo anuncios de oferta", "sin registros para jóvenes", "sin registros comparables"];
  const detConv = (t.conv.detalle || "").replace(/\.\s*$/, "");
  const senal = `<section class="fd-ancha fd-senal"><h4>Señales en Lima Este</h4><p><b>Registro de oferta:</b> ${CONV_TXT[t.conv.codigo] || ""} (${esc(t.conv.codigo)})${detConv && !basicos.includes(detConv) ? `: ${esc(refTxt(detConv))}` : ""}. La mayoría de las actividades que convocan no está registrada: si no hay registro, no resta.</p>${t.nec && t.nec !== "sin evidencia" ? `<p><b>Necesidad medida:</b> ${esc(t.nec)}.</p>` : ""}</section>`;
  const conFicha = (v) => (t.ficha ? detalleFicha(FICHA[t.ficha], v) : `<div class="fd-secciones"><section class="fd-ancha"><h4>Ficha de diseño</h4><p>Todavía no tiene una ficha de diseño detallada (para quién, barreras, componentes). Se puede preparar si queda entre las prioridades.</p></section>${v}</div>`);
  if (!t.medido) {
    return `${cab}<div class="fd-secciones"><section class="fd-ancha"><h4>Por qué no se ordena</h4><p>Ninguna encuesta del INEI pregunta cuántos jóvenes de Lima Este hacen o harían ${serv ? "este servicio" : "esta actividad"}, ni por qué no lo hacen. No se compara con las demás: se decide con la consulta directa a jóvenes.</p></section>${senal}</div>${conFicha(validar)}`;
  }
  // Embudo de Lima Este
  const pobT = PUB.reduce((s, p) => s + p.pob, 0);
  const dem = PUB.reduce((s, p) => s + (p.pob * ((t.seg[p.k][0] || 0) + (t.seg[p.k][1] || 0))) / 100, 0);
  const grande = `<div class="fd-grande"><b>${milC(t.total)}</b><span>jóvenes convocables en Lima Este: entre ${milC(t.lo)} y ${milC(t.hi)} con el margen de error de las encuestas (${pct(t.pct)} de los jóvenes).</span></div>`;
  const emb = `<div class="emb-mini">
      <div><b>${num(pobT)}</b><span>jóvenes de 15 a 29 años</span></div><i>×</i>
      <div><b>${pct((100 * dem) / pobT)}</b><span>la hace o la haría</span></div><i>×</i>
      <div><b>${pct((100 * t.total) / dem)}</b><span>tiene tiempo libre en su mejor horario</span></div><i>=</i>
      <div class="emb-fin"><b>${milC(t.total)}</b><span>convocables</span></div></div>`;
  // Qué dicen los datos
  const ref = (p) => (p === "referencial" ? "*" : "");
  const datoYa = t.prac.v != null ? `<b>${pct(t.prac.v)}${ref(t.prac.p)}</b> ${esc(t.prac.fuente)}.${t.factor < 1 ? " Es una práctica parecida, no la misma actividad: cuenta la mitad." : ""}` : "No medido: ninguna encuesta pregunta quién lo hace hoy.";
  const datoFr = t.fren_medidos && t.fren.v != null ? `<b>${pct(t.fren.v)}</b> ${esc(t.fren.fuente)}.${t.factor < 1 ? " También cuenta la mitad." : ""}` : "No medido: ninguna encuesta pregunta por qué no la hacen. El número es un piso.";
  const datos = `<section class="fd-ancha"><h4>Qué dicen los datos</h4><div class="fd-datos">
      <div><span class="fd-k"><i style="background:${COLOR_YA}"></i>Ya la hacen</span><p>${datoYa}</p></div>
      <div><span class="fd-k"><i style="background:${COLOR_FR}"></i>Frenados</span><p>${datoFr}</p></div></div></section>`;
  // Por público
  const maxP = Math.max(...PUB.map((p) => t.seg[p.k][2] + t.seg[p.k][3]));
  const porPub = `<section class="fd-ancha"><h4>Por público</h4><div class="fd-pub">${PUB.map((p) => {
    const s = t.seg[p.k], tot = s[2] + s[3];
    if (sinDato(s)) return `<div class="fp-fila"><span>${pubCorto(p)}</span><div class="rk-barra fp-barra"></div><b>—</b><small>sin dato para esta edad</small></div>`;
    return `<div class="fp-fila"><span>${pubCorto(p)}</span><div class="rk-barra fp-barra"><i style="width:${(100 * s[2]) / maxP}%;background:${COLOR_YA}"></i><i style="width:${(100 * s[3]) / maxP}%;background:${COLOR_FR}"></i></div><b>${milC(tot)}</b><small>${pct((s[0] || 0) + (s[1] || 0), 0)} la hace o la haría</small></div>`;
  }).join("")}</div></section>`;
  // Cómo convocar (con datos del público que más convoca)
  const p = principalDe(t, PUB), m = pctMujeres(t, PUB), K = CR.condiciones;
  const como = [`<li><b>Cuándo:</b> el ${bloqueTxt(p.mejor)}. ${pct(p.libre, 0)} de ${pubLargo(p)}, el público que más convoca, tiene ese horario libre.</li>`];
  if (t.fren.dinero && t.fren.v) {
    const d = Math.round((10 * t.fren.dinero) / t.fren.v);
    como.push(`<li><b>Gratis:</b> ${d >= 10 ? `todos los frenados que cuenta el modelo no ${serv ? "estudian" : "van"}` : `${d} de cada 10 frenados no ${serv ? "estudia" : "va"}`} por falta de dinero.</li>`);
  }
  if (t.fren.info && t.fren.v && Math.round((10 * t.fren.info) / t.fren.v) >= 1) {
    como.push(`<li><b>Difusión:</b> ${Math.round((10 * t.fren.info) / t.fren.v)} de cada 10 frenados no va porque no se entera a tiempo. Difundir con anticipación y por redes.</li>`);
  }
  como.push(`<li><b>Si es de noche:</b> ${pct(p.inseguro, 0)} de ${pubLargo(p)} se siente ${p.sexo === "mujer" ? "insegura" : "inseguro"} al caminar de noche por su barrio. Mejor de día, o con un lugar seguro y retorno acompañado.</li>`);
  if (p.sexo === "mujer" && p.edad !== "15-19" && p.sit.hogar) como.push(`<li><b>Cuidado infantil:</b> ${pct(p.sit.hogar, 0)} de ${pubLargo(p)} se dedica al hogar, y ${pct(K.cuidado.hogar_ninos, 0)} de las jóvenes dedicadas al hogar vive con niños de 0 a 5 años.</li>`);
  if (m != null && (m < 35 || m > 65)) como.push(`<li><b>Quiénes llegan:</b> ${m < 35 ? `${pct(100 - m, 0)} de su público son hombres` : `${pct(m, 0)} de su público son mujeres`}.</li>`);
  const comoHTML = `<section><h4>Cómo convocar</h4><ul class="fd-como">${como.join("")}</ul></section>`;
  // Dónde vive su público
  const dist = {};
  PUB.forEach((q) => { const c = t.seg[q.k][2] + t.seg[q.k][3]; Object.entries(q.dist).forEach(([d, v]) => { dist[d] = (dist[d] || 0) + (c * v) / 100; }); });
  const ds = Object.entries(dist).sort((x, y) => y[1] - x[1]), maxD = ds[0][1];
  const dondeHTML = `<section><h4>Dónde vive su público</h4><div class="fd-dist">${ds.map(([d, v]) => `<div class="fp-fila fd-d"><span>${esc(d)}</span><div class="fd-barra"><i style="width:${(100 * v) / maxD}%;background:${C.indigo2}"></i></div><b>${milC(v)}</b></div>`).join("")}</div>
    <p class="meta">Según dónde vive cada público. Las encuestas no permiten saber si en un distrito se practica más que en otro.</p></section>`;
  return `${cab}${grande}${emb}<div class="fd-secciones">${datos}${porPub}${comoHTML}${dondeHTML}${senal}</div>${conFicha(validar)}`;
}

function detalleFicha(f, validar) {
  const regs = f.registros.length ? `<table class="tabla-mini"><thead><tr><th>Código</th><th>Actividad registrada</th><th>Cifra</th></tr></thead><tbody>${f.registros.map((r) =>
    `<tr><td><span class="cod">${esc(r.codigo)}</span></td><td>${esc(r.nombre)}<small>${esc(r.distrito)} · ${esc(r.publico)}</small></td><td>${r.cifra != null ? `${num(r.cifra)} ${esc(r.cifra_tipo || "")}` : esc(r.nota || "")}</td></tr>`).join("")}</tbody></table>` : "<p>No se encontraron actividades comparables con datos para jóvenes (sin evidencia, que no es evidencia negativa).</p>";
  const comp = (estados) => f.componentes.filter((c) => estados.includes(c.estado));
  const compHTML = [["Con respaldo", ["respaldado en dos o más dimensiones", "respaldado en una dimensión"]],
    ["Por validar", ["solo señales débiles", "hipótesis de diseño", "sin evidencia"]],
    ["Ya existe, transversal o descartado", ["complementario (ya existe)", "condición transversal", "descartado"]]]
    .map(([t, es]) => `<div class="fd-comp"><span>${t}</span>${comp(es).map((c) => `<p class="${c.estado === "descartado" ? "tachado" : ""}"><b>${esc(c.componente)}</b><small>${esc(c.estado)}. ${esc(refTxt(c.nota || ""))}</small></p>`).join("") || "<p><small>—</small></p>"}</div>`).join("");
  const encabezado = validar === null ? `<div class="fd-cab"><div class="fd-tags"><span class="m-id">${f.id}</span><span class="tag-s">${esc(f.linea)}</span><span class="tag-s">${esc(f.tipo_ficha)}</span><span class="nivel n0">No se puntúa</span></div><h3>${esc(f.actividad)}</h3></div>` : `<h4 class="fd-ficha-t">Ficha de diseño ${f.id}: ${esc(f.actividad)}</h4>`;
  return `${encabezado}<div class="fd-secciones">
      <section><h4>Para quién</h4><p>${esc(refTxt(f.poblacion))}</p>${f.alcance ? `<p class="meta">${esc(refTxt(f.alcance))}</p>` : ""}</section>
      <section><h4>Qué sabemos</h4><p>${esc(refTxt(f.necesidad))}</p>${vinetas(f.afirmaciones)}</section>
      <section><h4>Práctica o interés</h4><p>${esc(refTxt((f.interes || "").replace(/^\[[^\]]+\]\s*/, "").replace(/\s*Salto inferencial:.*$/, "")))}</p>${f.salto_inferencial ? `<p class="salto"><b>Salto que falta probar:</b> ${esc(f.salto_inferencial)}</p>` : ""}</section>
      <section><h4>Cómo convocar</h4>${barreras(f.barreras)}<p class="meta">Además, las <a href="#criterios">condiciones comunes</a>: gratis, horario de domingo por la tarde o sábado por la noche, lugar seguro y difusión con tiempo.</p></section>
      <section class="fd-ancha"><h4>Convocatoria observada en actividades parecidas</h4>${f.convocatoria_detalle_codigo ? `<p class="meta">${esc(f.convocatoria_detalle_codigo)}</p>` : ""}${regs}<p class="meta"><b>Oferta existente:</b> ${esc(f.oferta || "—")}</p></section>
      ${validar || ""}
      <section class="fd-validar fd-ancha"><h4>Hipótesis y piloto de la ficha</h4>
        <div class="rejilla-3"><div><b>No sabemos</b>${vinetas(f.vacios)}</div><div><b>Hipótesis a probar</b>${f.hipotesis && f.hipotesis !== "No aplica." ? vinetas(f.hipotesis) : "<p>No aplica.</p>"}</div>
        <div><b>Qué medir en un piloto</b><p>${esc(f.validacion_piloto || "—")}</p><b>Dónde empezar</b><p>${esc(f.donde || "—")}</p></div></div></section>
      <section class="fd-ancha"><h4>Componentes</h4><div class="rejilla-3">${compHTML}</div></section>
    </div>
    <p class="fd-ev">Evidencias: ${listaTxt(f.evidencias).map((e) => `<span class="m-id">${e}</span>`).join(" ")}</p>`;
}

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


Object.assign(RENDER, { resultado: renderResultado, fichas: renderFichas, transversal: renderTransversal });
