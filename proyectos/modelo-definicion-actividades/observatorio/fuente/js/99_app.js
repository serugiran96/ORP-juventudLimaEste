/* Navegación entre capas y pestañas. Cada capa registra sus funciones en RENDER (por pestaña) y HERO (por capa). */
const CAPAS = {
  contexto: ["poblacion", "estudio", "seguridad", "organizaciones", "natalidad", "extra"],
  intereses: ["tiempo", "horarios", "cultura", "digital", "aspiraciones"],
  oferta: ["explorar", "publico", "convocatoria", "visibilidad"],
  cruce: ["criterios", "matriz", "segmentos", "hallazgos", "evidencias"],
  actividades: ["resultado", "fichas", "transversal"],
  acerca: ["acerca"]
};
const CAPA_DE = {};
Object.entries(CAPAS).forEach(([c, tabs]) => tabs.forEach((t) => { CAPA_DE[t] = c; }));

function render(tab) {
  if (RENDER[tab]) RENDER[tab]();
  refrescarTablas();
}
function mostrar() {
  let h = decodeURIComponent((location.hash || "#poblacion").slice(1));
  if (/^[AF]-\d\d$/.test(h)) { S.ficha = h; h = "fichas"; }   // enlace directo a un tipo de actividad o a una ficha
  const tab = CAPA_DE[h] ? h : "poblacion";
  const capa = CAPA_DE[tab];
  const cambioCapa = capa !== S.capa, cambio = tab !== S.tab;
  S.tab = tab;
  S.capa = capa;
  document.querySelectorAll("section.capa").forEach((c) => { c.hidden = c.dataset.capa !== capa; });
  document.querySelectorAll(".capas a").forEach((a) => a.classList.toggle("activa", a.dataset.capa === capa));
  document.querySelectorAll(`#capa-${capa} [data-panel]`).forEach((p) => { p.hidden = p.id !== tab; });
  document.querySelectorAll(`#capa-${capa} .pestanas a`).forEach((a) => a.classList.toggle("activa", a.dataset.tab === tab));
  if (HERO[capa]) HERO[capa]();
  render(tab);
  requestAnimationFrame(() => {
    document.querySelectorAll(`#${tab} .grafico`).forEach((el) => graficos[el.id] && graficos[el.id].resize());
    if (cambioCapa) {
      window.scrollTo(0, 0);
    } else if (cambio) {
      const p = document.querySelector(`#capa-${capa} .pestanas`);
      const y = p ? p.getBoundingClientRect().top + window.scrollY - 70 : 0;
      if (window.scrollY > y) window.scrollTo({ top: y, behavior: "smooth" });
    }
  });
}
let espera;
window.addEventListener("resize", () => { clearTimeout(espera); espera = setTimeout(() => Object.values(graficos).forEach((c) => c.resize()), 120); });
window.addEventListener("hashchange", mostrar);

$("pie-meta").textContent = `Generado el ${D.meta.generado}${D.meta.commit ? ` · versión ${D.meta.commit}` : ""} · Fuentes: Dato Joven (Observatorio Nacional de Juventud), ENAHO, ENAPRES y ENUT (INEI), RENOJ y Programa de Voluntariado (SENAJU), notas de prensa de municipalidades y entidades públicas, Ipsos.`;
montarControles();
// Las tipografías van incrustadas: se espera a que estén listas para que los gráficos midan bien sus textos.
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(mostrar);
