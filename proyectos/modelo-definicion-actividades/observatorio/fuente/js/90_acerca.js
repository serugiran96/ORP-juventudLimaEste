/* Acerca del observatorio */
RENDER.acerca = () => {
  $("acerca-version").textContent = `Versión generada el ${D.meta.generado}${D.meta.commit ? ` (código ${D.meta.commit})` : ""}.`;
};
