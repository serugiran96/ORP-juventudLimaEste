/* ==========================================================================
   Informe en formato web: interacción.
   Todo es opcional: sin JavaScript la página se lee completa.
   1. Barra de progreso de lectura
   2. Índice desplegable de la barra superior: marca el capítulo que se está leyendo
   3. Barras de los gráficos: crecen al aparecer en pantalla
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

  /* 2. Índice desplegable -------------------------------------------------- */
  var menu = document.getElementById("menu");
  var boton = document.querySelector(".barra__indice");
  var etiqueta = document.querySelector("[data-actual]");
  var enlaces = menu ? Array.prototype.slice.call(menu.querySelectorAll("a[href^='#']")) : [];
  var capitulos = enlaces
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);

  function abrirMenu(abrir) {
    if (!menu || !boton) return;
    menu.classList.toggle("abierto", abrir);
    boton.setAttribute("aria-expanded", abrir ? "true" : "false");
  }
  if (boton) {
    boton.addEventListener("click", function () {
      abrirMenu(boton.getAttribute("aria-expanded") !== "true");
    });
  }
  enlaces.forEach(function (a) { a.addEventListener("click", function () { abrirMenu(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && boton && boton.getAttribute("aria-expanded") === "true") {
      abrirMenu(false);
      boton.focus();
    }
  });
  document.addEventListener("click", function (e) {
    if (!menu || !menu.classList.contains("abierto")) return;
    if (!menu.contains(e.target) && !boton.contains(e.target)) abrirMenu(false);
  });

  function marcarActual(id) {
    enlaces.forEach(function (a) {
      if (a.getAttribute("href") === "#" + id) {
        a.setAttribute("aria-current", "true");
        if (etiqueta) etiqueta.textContent = a.textContent.replace(/^(\d)/, "$1. ");
      } else {
        a.removeAttribute("aria-current");
      }
    });
  }

  // El capítulo actual es el último cuyo inicio ya pasó bajo la barra superior.
  function capituloActual() {
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
})();
