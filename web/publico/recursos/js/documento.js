/* ==========================================================================
   Documento en formato web: interacción.
   Todo es opcional: sin JavaScript la página se lee completa.
   1. Barra de progreso de lectura
   2. Índice desplegable: marca el capítulo que se está leyendo
   3. Barras del gráfico: crecen al aparecer en pantalla
   4. Bibliografía: cuenta de fuentes
   ========================================================================== */
(function () {
  "use strict";

  var movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. Progreso de lectura ------------------------------------------------ */
  var progreso = document.querySelector("[data-progreso]");
  var pendiente = false;
  function actualizarProgreso() {
    pendiente = false;
    var alto = document.documentElement.scrollHeight - window.innerHeight;
    var avance = alto > 0 ? Math.min(1, Math.max(0, window.scrollY / alto)) : 0;
    progreso.style.width = (avance * 100).toFixed(2) + "%";
  }
  if (progreso) {
    window.addEventListener("scroll", function () {
      if (!pendiente) { pendiente = true; requestAnimationFrame(actualizarProgreso); }
    }, { passive: true });
    window.addEventListener("resize", actualizarProgreso);
    actualizarProgreso();
  }

  /* 2. Índice ------------------------------------------------------------ */
  var indice = document.getElementById("indice");
  var boton = document.querySelector(".barra__indice");
  var etiqueta = document.querySelector("[data-actual]");
  var enlaces = indice ? Array.prototype.slice.call(indice.querySelectorAll("a[href^='#']")) : [];
  var capitulos = enlaces
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);

  function abrirIndice(abrir) {
    if (!indice || !boton) return;
    indice.classList.toggle("abierta", abrir);
    boton.setAttribute("aria-expanded", abrir ? "true" : "false");
  }
  if (boton) {
    boton.addEventListener("click", function () {
      abrirIndice(boton.getAttribute("aria-expanded") !== "true");
    });
  }
  enlaces.forEach(function (a) { a.addEventListener("click", function () { abrirIndice(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && boton && boton.getAttribute("aria-expanded") === "true") {
      abrirIndice(false);
      boton.focus();
    }
  });
  document.addEventListener("click", function (e) {
    if (!indice || !indice.classList.contains("abierta")) return;
    if (!indice.contains(e.target) && !boton.contains(e.target)) abrirIndice(false);
  });

  function marcarActual(id) {
    enlaces.forEach(function (a) {
      var esActual = a.getAttribute("href") === "#" + id;
      if (esActual) {
        a.setAttribute("aria-current", "true");
        if (etiqueta) etiqueta.textContent = a.textContent.replace(/^(\d)/, "$1. ");
      } else {
        a.removeAttribute("aria-current");
      }
    });
  }

  // El capítulo actual es el último cuyo inicio ya pasó bajo la barra superior.
  function capituloActual() {
    // Al final de la página, el último capítulo es el actual aunque su inicio no llegue arriba.
    var alFinal = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    if (alFinal) return capitulos[capitulos.length - 1];
    var limite = window.innerHeight * 0.3;
    var actual = null;
    capitulos.forEach(function (c) {
      if (c.getBoundingClientRect().top - limite <= 0) actual = c;
    });
    return actual;
  }
  var ultimo = null;
  function revisarCapitulo() {
    var c = capituloActual();
    var id = c ? c.id : null;
    if (id === ultimo) return;
    ultimo = id;
    if (id) { marcarActual(id); }
    else {
      enlaces.forEach(function (a) { a.removeAttribute("aria-current"); });
      if (etiqueta) etiqueta.textContent = "Índice";
    }
  }
  if (capitulos.length) {
    var esperando = false;
    window.addEventListener("scroll", function () {
      if (!esperando) { esperando = true; requestAnimationFrame(function () { esperando = false; revisarCapitulo(); }); }
    }, { passive: true });
    revisarCapitulo();
  }

  /* 3. Barras que crecen al aparecer ------------------------------------- */
  var graficos = document.querySelectorAll(".grafico");
  if (movimientoReducido || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(graficos, function (el) { el.classList.add("visible"); });
  } else {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add("visible");
          observador.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.35 });
    Array.prototype.forEach.call(graficos, function (el) { observador.observe(el); });
  }

  /* 4. Cuenta de fuentes en la bibliografía ------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-cuenta]"), function (span) {
    var lista = span.closest("details").querySelector("ul");
    if (lista) span.textContent = "(" + lista.children.length + ")";
  });
})();
