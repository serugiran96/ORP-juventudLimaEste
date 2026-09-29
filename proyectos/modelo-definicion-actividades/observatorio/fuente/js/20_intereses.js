/* Capa 2 · Intereses: su semana, horarios, cultura y ocio, vida digital y aspiraciones */
const I = D.intereses;
const horas = (e) => (!e || e.v == null ? "—" : dec(e.v) + NB + "h" + (e.p === "r" ? "*" : ""));
const LUGAR = { le: "Lima Este", lm: "Lima Metropolitana" };

Object.assign(S, { horQuien: "le|total|todos", culVista: "lugar", culItem: I.cultura.asistencia.le.total[0].t, digVista: "lugar",
  ipsos: I.aspiraciones[0].id });
Object.assign(CONTROLES, {
  horQuien: [["le|total|todos", "Lima Este"], ["lm|total|todos", "Lima Metropolitana"], ["lm|mujer|todos", "Mujeres (Lima Metropolitana)"],
    ["lm|hombre|todos", "Hombres (Lima Metropolitana)"], ["lm|mujer|no trabajó ni estudió en la semana", "Mujeres que no trabajan ni estudian (LM)"]],
  culVista: [["lugar", "Lima Este y Lima Metropolitana"], ["sexo", "Mujeres y hombres"], ["edad", "Por edad"]],
  digVista: [["lugar", "Lima Este y Lima Metropolitana"], ["sexo", "Mujeres y hombres"]],
  ipsos: I.aspiraciones.map((e) => [e.id, e.estudio.replace(/:.*$/, "").replace(/ del Perú urbano.*$/, "")])
});

HERO.intereses = () => {
  const r = I.cultura.resumen.le.alguno;
  $("hero-intereses").innerHTML = `<div class="v">${est(r)}</div>
    <div class="l">de los jóvenes de Lima Este fue al menos una vez en el año a una actividad cultural: cine, conciertos, ferias, bibliotecas…</div>`;
};

// Barras agrupadas horizontales: una fila por categoría, una serie por grupo. Solo la primera serie lleva etiqueta.
function barrasGrupos(id, filas, grupos, o) {
  const opt = o || {};
  const series = grupos.map(([nombre, color, datos], i) => ({
    id: "s" + i, name: nombre, type: "bar", barMaxWidth: opt.grosor || 12, barGap: "25%",
    data: datos.map((e) => ({ value: val(e) || 0, est: e, txt: opt.fmt ? opt.fmt(e) : est(e) })),
    itemStyle: { color, borderRadius: [0, 8, 8, 0] },
    label: i === 0 || opt.todas ? etiquetaPunta() : { show: false }
  }));
  g(id).setOption(opc({
    grid: { left: 16, right: 58, top: grupos.length > 1 ? 36 : 6, bottom: 6, containLabel: true },
    legend: grupos.length > 1 ? leyenda(grupos.map((x) => x[0])) : { show: false },
    xAxis: Object.assign(ejeVal(opt.max, opt.sufijo === undefined ? NB + "%" : opt.sufijo), { show: !opt.sinEje }),
    yAxis: ejeCat(filas),
    tooltip: { formatter: (p) => tt(filas[p.dataIndex], [{ v: p.data.txt, n: esc(p.seriesName) + (opt.fmt ? "" : "<br>" + detalleEst(p.data.est)) }]) },
    series
  }), { replaceMerge: ["series"] });
  if (opt.click && !graficos[id]._click) { g(id).on("click", (p) => opt.click(p.dataIndex)); graficos[id]._click = true; }
}

// ---------------------------------------------------------------- Su semana
function renderTiempo() {
  const L = I.horarios.horas_libres.le.total, sat = I.tiempo.satisfaccion.le;
  $("int-tiempo-tiles").innerHTML = [
    tile({ clase: "oscuro", v: horas(L[0]), l: "libres un día de lunes a viernes", s: "Sin trabajo, estudio, tareas del hogar, cuidado ni traslados" }),
    tile({ v: horas(L[1]), l: "libres el sábado" }),
    tile({ v: horas(L[2]), l: "libres el domingo" }),
    tile({ v: est(sat[0]), l: "está muy satisfecho con la cantidad de su tiempo libre", title: tituloEst(sat[0]) })
  ].join("");
  const le = I.tiempo.participacion.le.total, lm = I.tiempo.participacion.lm.total;
  barrasGrupos("g-int-actividades", le.map((x) => x.t), [["Lima Este", C.rojo, le], ["Lima Metropolitana", C.gris, lm]], { max: 100 });
  const k = (t) => le.find((x) => x.t === t);
  $("int-act-lectura").innerHTML = `Casi todos usan el celular o la computadora (<b>${est(k("Usar celular o computadora"))}</b>) y hacen tareas del hogar (<b>${est(k("Tareas del hogar"))}</b>) en la semana. En su tiempo libre, <b>${est(k("Deporte o ejercicio"))}</b> hizo deporte, <b>${est(k("Aficiones, artes y juegos"))}</b> se dedicó a aficiones, artes o juegos y <b>${est(k("Ir a eventos culturales o deportivos"))}</b> fue a un evento cultural o deportivo.`;
  const hLE = I.tiempo.horas.le.total, hM = I.tiempo.horas.lm.mujer, hH = I.tiempo.horas.lm.hombre;
  barrasGrupos("g-int-horas", hLE.map((x) => x.t), [["Lima Este (todos)", C.rojo, hLE], ["Mujeres (Lima Metropolitana)", C.verde, hM], ["Hombres (Lima Metropolitana)", C.indigo, hH]],
    { fmt: horas, sufijo: NB + "h", todas: true });
  const tareas = (x) => x.find((y) => y.t === "Tareas del hogar"), cuidar = (x) => x.find((y) => y.t === "Cuidar a otras personas");
  $("int-horas-lectura").innerHTML = `En Lima Metropolitana, las mujeres jóvenes dedican <b>${horas(tareas(hM))}</b> a la semana a las tareas del hogar y <b>${horas(cuidar(hM))}</b> a cuidar a otras personas; los hombres, <b>${horas(tareas(hH))}</b> y <b>${horas(cuidar(hH))}</b>.`;
  const sLE = I.tiempo.satisfaccion.le, sLM = I.tiempo.satisfaccion.lm;
  barrasGrupos("g-int-satisfaccion", sLE.map((x) => x.t), [["Lima Este", C.rojo, sLE], ["Lima Metropolitana", C.gris, sLM]], { max: 100 });
  $("int-sat-lectura").innerHTML = `Menos de la mitad está muy satisfecho con su tiempo libre: <b>${est(sLE[0])}</b> con la cantidad y <b>${est(sLE[1])}</b> con la calidad.`;
}
TABLAS.intActividades = () => [["Actividad", "Lima Este", "Lima Metropolitana"], I.tiempo.participacion.le.total.map((x, i) => [x.t, est(x), est(I.tiempo.participacion.lm.total[i])])];
TABLAS.intHoras = () => [["Actividad", "Lima Este", "Mujeres (LM)", "Hombres (LM)"], I.tiempo.horas.le.total.map((x, i) => [x.t, horas(x), horas(I.tiempo.horas.lm.mujer[i]), horas(I.tiempo.horas.lm.hombre[i])])];
TABLAS.intSatisfaccion = () => [["Aspecto", "Lima Este", "Lima Metropolitana"], I.tiempo.satisfaccion.le.map((x, i) => [x.t, est(x), est(I.tiempo.satisfaccion.lm[i])])];

// ---------------------------------------------------------------- Horarios
const DIAS = ["Lunes a viernes", "Sábado", "Domingo"];
const FRANJAS = [["09:00-13:00", "Mañana", "9 a 13 h"], ["14:00-18:00", "Tarde", "14 a 18 h"], ["18:00-22:00", "Noche", "18 a 22 h"]];
function valoresHorario() {
  const [geo, sexo, grupo] = S.horQuien.split("|");
  return I.horarios[geo][`${sexo}|${grupo}`] || [];
}
function renderHorarios() {
  const vals = valoresHorario(), B = I.horarios.bloques;
  const celda = (dia, franja) => { const i = B.findIndex((b) => b.dia === dia && b.franja === franja); return i < 0 ? undefined : vals[i]; };
  let h = `<div class="hor-grid"><span></span>${FRANJAS.map(([, n, r]) => `<span class="hor-cab">${n}<small>${r}</small></span>`).join("")}`;
  DIAS.forEach((dia) => {
    h += `<span class="hor-dia">${dia}</span>`;
    FRANJAS.forEach(([f, n]) => {
      const e = celda(dia, f);
      if (e === undefined) { h += `<span class="hor-celda hor-na">No se midió</span>`; return; }
      const v = val(e);
      const a = v == null ? 0 : Math.min(1, 0.1 + (0.85 * v) / 60);
      h += `<span class="hor-celda${a > 0.5 ? " oscura" : ""}${n === "Noche" ? " noche" : ""}" style="--a:${a.toFixed(2)}" title="${esc(dia)}, ${esc(n.toLowerCase())}: ${esc(tituloEst(e) || "muestra insuficiente")}"><b>${est(e)}</b></span>`;
    });
  });
  $("int-horario").innerHTML = h + "</div>";
  const nombreQuien = CONTROLES.horQuien.find((x) => x[0] === S.horQuien)[1];
  $("hor-etiqueta").textContent = nombreQuien;
  const disp = B.map((b, i) => ({ b, e: vals[i] })).filter((x) => x.e && x.e.v != null).sort((a, b) => b.e.v - a.e.v);
  const nom = (b) => `${b.dia === "Lunes a viernes" ? "un día de semana" : "el " + b.dia.toLowerCase()} ${FRANJAS.find((f) => f[0] === b.franja)[1] === "Mañana" ? "por la mañana" : FRANJAS.find((f) => f[0] === b.franja)[1] === "Tarde" ? "por la tarde" : "por la noche"}`;
  $("int-hor-lectura").innerHTML = disp.length
    ? `Los mejores momentos son <b>${nom(disp[0].b)}</b> (${est(disp[0].e)}) y <b>${nom(disp[1].b)}</b> (${est(disp[1].e)}). El peor, <b>${nom(disp[disp.length - 1].b)}</b> (${est(disp[disp.length - 1].e)}).`
    : "Muestra insuficiente para este grupo.";
  $("hor-inseguridad").textContent = est(D.contexto.seguridad.noche_inseguro.le.total);
}
TABLAS.intHorario = () => [["Día y franja"].concat(CONTROLES.horQuien.map((x) => x[1])), I.horarios.bloques.map((b, i) => [`${b.dia}, ${b.franja}`].concat(CONTROLES.horQuien.map(([k]) => {
  const [geo, sexo, grupo] = k.split("|"); const v = I.horarios[geo][`${sexo}|${grupo}`]; return v ? est(v[i]) : "—";
})))];

// ---------------------------------------------------------------- Cultura y ocio
function renderCultura() {
  const R = I.cultura.resumen.le, pat = I.cultura.patrimonio.le;
  $("int-cultura-tiles").innerHTML = [
    tile({ clase: "oscuro", v: est(R.alguno), l: "fue a alguna actividad cultural en el año", title: tituloEst(R.alguno) }),
    tile({ v: est(R.en_vivo), l: "vio un espectáculo o exposición en vivo (teatro, danza, circo, música o arte)", title: tituloEst(R.en_vivo) }),
    tile({ v: est(pat[0]), l: "visitó un museo", title: tituloEst(pat[0]) }),
    tile({ v: est(pat[1]), l: "visitó un monumento histórico", title: tituloEst(pat[1]) })
  ].join("");
  const A = I.cultura.asistencia, items = A.le.total.map((x) => x.t);
  let grupos;
  if (S.culVista === "lugar") grupos = [["Lima Este", C.rojo, A.le.total], ["Lima Metropolitana", C.gris, A.lm.total]];
  else if (S.culVista === "sexo") grupos = [["Mujeres", C.verde, A.le.mujer], ["Hombres", C.indigo, A.le.hombre]];
  else grupos = EDADES.map((e) => [EDAD[e] + " años", RAMPA[e], A.le[e]]);
  barrasGrupos("g-int-cultura", items, grupos, { max: 80, click: (i) => { S.culItem = items[i]; renderCulturaItem(); } });
  const le = A.le.total;
  let t = `El cine es lo más frecuente (<b>${est(le[0])}</b>). Le siguen los conciertos (<b>${est(le[1])}</b>), las ferias artesanales (<b>${est(le[2])}</b>), los festivales locales (<b>${est(le[3])}</b>) y las ferias del libro (<b>${est(le[4])}</b>).`;
  if (S.culVista === "edad") t = `Los conciertos son sobre todo de 20 a 29 años (${est(A.le["20-24"][1])} y ${est(A.le["25-29"][1])}) y poco de 15 a 19 (${est(A.le["15-19"][1])}). Al cine va ${est(A.le["15-19"][0])} de los de 15–19 y ${est(A.le["25-29"][0])} de los de 25–29.`;
  if (S.culVista === "sexo") {
    // Solo se nombran las diferencias cuyos intervalos de confianza no se superponen.
    const claras = items.map((n, i) => ({ n, m: A.le.mujer[i], h: A.le.hombre[i] })).filter((x) => distintos(x.m, x.h));
    t = claras.length
      ? `Diferencias claras entre mujeres y hombres: ${claras.map((x) => `<b>${esc(x.n.toLowerCase())}</b> (${est(x.m)} frente a ${est(x.h)})`).join("; ")}. En las demás actividades, la diferencia está dentro del margen de error.`
      : "No hay diferencias claras entre mujeres y hombres: todas están dentro del margen de error.";
  }
  $("int-cul-lectura").innerHTML = t;
  renderCulturaItem();
}
function renderCulturaItem() {
  $("cul-items").innerHTML = I.cultura.asistencia.le.total.map((x) => `<button class="chip" type="button" data-cul="${esc(x.t)}" aria-pressed="${x.t === S.culItem}">${esc(x.t)}</button>`).join("");
  $("cul-item-titulo").textContent = `${S.culItem}: por qué no fueron y cómo entraron`;
  const mot = I.cultura.motivos[S.culItem], ent = I.cultura.entrada[S.culItem];
  barrasGrupos("g-int-motivos", mot.map((x) => x.t), [["Lima Este", C.indigo, mot]], { max: 70, sinEje: true });
  barrasGrupos("g-int-entrada", ent.map((x) => x.t), [["Lima Este", C.verde, ent]], { max: 100, sinEje: true });
  const top = mot.filter((x) => x.v != null).sort((a, b) => b.v - a.v)[0];
  const dinero = mot.find((x) => x.t === "Falta de dinero"), gratis = ent.find((x) => x.t === "Gratis");
  const entTop = ent.filter((x) => x.v != null).sort((a, b) => b.v - a.v)[0];
  const frEnt = gratis && gratis.v != null ? `Entre quienes fueron, <b>${est(gratis)}</b> entró gratis.`
    : entTop ? `Entre quienes fueron, lo más común es que <b>${entTop.t.toLowerCase()}</b> (${est(entTop)}).` : "";
  $("int-mot-lectura").innerHTML = `Entre quienes no fueron, el motivo más citado es <b>${top ? top.t.toLowerCase() : "—"}</b> (${est(top)})${dinero && dinero.v != null ? `; la falta de dinero pesa ${est(dinero)}` : ""}. ${frEnt}`;
}
$("cul-items").addEventListener("click", (ev) => { const b = ev.target.closest("[data-cul]"); if (b) { S.culItem = b.dataset.cul; renderCulturaItem(); } });
TABLAS.intCultura = () => [["Actividad", "Lima Este", "Lima Metropolitana", "Mujeres", "Hombres", "15 a 19", "20 a 24", "25 a 29"],
  I.cultura.asistencia.le.total.map((x, i) => { const A = I.cultura.asistencia; return [x.t, est(x), est(A.lm.total[i]), est(A.le.mujer[i]), est(A.le.hombre[i]), est(A.le["15-19"][i]), est(A.le["20-24"][i]), est(A.le["25-29"][i])]; })];

// ---------------------------------------------------------------- Vida digital
function renderDigital() {
  const d = I.digital.le.total, prop = (t) => d.propositos.find((x) => x.t === t);
  $("int-digital-tiles").innerHTML = [
    tile({ clase: "oscuro", v: est(d.usa), l: "usó internet el mes anterior", title: tituloEst(d.usa) }),
    tile({ v: est(d.diario), l: "de ellos lo usa todos los días", title: tituloEst(d.diario) }),
    tile({ v: est(prop("Estudiar o capacitarse")), l: "lo usa para estudiar o capacitarse", title: tituloEst(prop("Estudiar o capacitarse")) }),
    tile({ v: est(prop("Vender")), l: "lo usa para vender productos o servicios", title: tituloEst(prop("Vender")) })
  ].join("");
  const P = I.digital;
  const grupos = S.digVista === "lugar"
    ? [["Lima Este", C.rojo, P.le.total.propositos], ["Lima Metropolitana", C.gris, P.lm.total.propositos]]
    : [["Mujeres", C.verde, P.le.mujer.propositos], ["Hombres", C.indigo, P.le.hombre.propositos]];
  barrasGrupos("g-int-propositos", d.propositos.map((x) => x.t), grupos, { max: 100 });
  $("int-dig-lectura").innerHTML = S.digVista === "lugar"
    ? `Internet es sobre todo para comunicarse (<b>${est(prop("Comunicarse (chat, redes)"))}</b>) y entretenerse (<b>${est(prop("Entretenimiento"))}</b>). Solo <b>${est(prop("Estudiar o capacitarse"))}</b> lo usa para estudiar o capacitarse.`
    : `Mujeres: ${est(P.le.mujer.propositos.find((x) => x.t === "Estudiar o capacitarse"))} lo usa para estudiar; hombres: ${est(P.le.hombre.propositos.find((x) => x.t === "Estudiar o capacitarse"))}.`;
  const b = P.bienes.le;
  barrasGrupos("g-int-bienes", b.map((x) => x.t), [["Lima Este", C.rojo, b], ["Lima Metropolitana", C.gris, P.bienes.lm]], { max: 100 });
  const k = (t) => b.find((x) => x.t === t);
  $("int-bien-lectura").innerHTML = `Música (<b>${est(k("Música por internet"))}</b>) y películas o videos (<b>${est(k("Películas o videos por internet"))}</b>) por internet son casi universales. <b>${est(k("Videojuegos en el celular"))}</b> juega videojuegos en el celular y <b>${est(k("Videojuegos en línea"))}</b> en línea.`;
}
TABLAS.intPropositos = () => [["Uso", "Lima Este", "Lima Metropolitana", "Mujeres", "Hombres"], I.digital.le.total.propositos.map((x, i) => [x.t, est(x), est(I.digital.lm.total.propositos[i]), est(I.digital.le.mujer.propositos[i]), est(I.digital.le.hombre.propositos[i])])];
TABLAS.intBienes = () => [["Producto", "Lima Este", "Lima Metropolitana"], I.digital.bienes.le.map((x, i) => [x.t, est(x), est(I.digital.bienes.lm[i])])];

// ---------------------------------------------------------------- Aspiraciones (Ipsos, exploratorio)
function renderAspiraciones() {
  const e = I.aspiraciones.find((x) => x.id === S.ipsos);
  $("ipsos-ficha").innerHTML = `<i class="punto"></i><span><b>${esc(e.estudio)}</b>. Trabajo de campo: ${esc(e.campo || "—")}. Población: ${esc(e.poblacion || "—")} (${esc(e.cobertura || "—")}). Muestra: ${esc(e.muestra || "—")}. ${esc(e.metodo || "")}</span>`;
  $("ipsos-temas").innerHTML = e.temas.map((t) => {
    const max = 100;  // escala absoluta: los porcentajes se comparan entre tarjetas
    return `<article class="ex"><div class="ex-dim">${esc(e.id)}</div><h4>${esc(t.tema)}</h4>
      <div class="ex-comp">${t.items.map((x) => `<div title="${esc(x.nota || "")}"><span class="ex-larga">${esc(x.n)}</span><span class="b"><i style="width:${(100 * (x.v || 0)) / max}%;background:${C.indigo2}"></i></span><b>${x.v == null ? "—" : dec(x.v, 0) + NB + "%"}</b></div>`).join("")}</div>
      ${t.items[0] && t.items[0].base && t.items[0].base !== "Total" ? `<small class="meta">Base: ${esc(t.items[0].base)}</small>` : ""}</article>`;
  }).join("");
}

Object.assign(RENDER, { tiempo: renderTiempo, horarios: renderHorarios, cultura: renderCultura, digital: renderDigital, aspiraciones: renderAspiraciones });
