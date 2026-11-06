/* ==========================================================================
   Documento en formato web: interacción.
   Todo es opcional: sin JavaScript la página se lee completa.
   1. Barra de progreso de lectura
   2. Índice: marca el capítulo que se está leyendo y se abre como panel en móvil
   3. Pestañas (demandas del Comité Tahuantinsuyo)
   4. Barras de los gráficos: crecen al aparecer en pantalla
   5. Bibliografía: cuenta de fuentes
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

  /* 3. Pestañas ----------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-pestanas]"), function (grupo, g) {
    var paneles = Array.prototype.slice.call(grupo.querySelectorAll(".pestana"));
    if (!paneles.length) return;
    var lista = document.createElement("div");
    lista.className = "pestanas__lista";
    lista.setAttribute("role", "tablist");
    lista.setAttribute("aria-label", "Demandas por tema");

    var botones = paneles.map(function (panel, i) {
      var tema = panel.querySelector(".pestana__tema");
      var b = document.createElement("button");
      b.type = "button";
      b.className = "pestanas__boton";
      b.id = "pestana-" + g + "-" + i;
      b.textContent = tema ? tema.textContent : String(i + 1);
      b.setAttribute("role", "tab");
      b.setAttribute("aria-controls", "panel-" + g + "-" + i);
      panel.id = "panel-" + g + "-" + i;
      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("aria-labelledby", b.id);
      panel.tabIndex = 0;
      lista.appendChild(b);
      return b;
    });

    function elegir(i, enfocar) {
      botones.forEach(function (b, j) {
        var activo = i === j;
        b.setAttribute("aria-selected", activo ? "true" : "false");
        b.tabIndex = activo ? 0 : -1;
        paneles[j].hidden = !activo;
      });
      if (enfocar) botones[i].focus();
    }
    botones.forEach(function (b, i) {
      b.addEventListener("click", function () { elegir(i, false); });
      b.addEventListener("keydown", function (e) {
        var n = botones.length, destino = null;
        if (e.key === "ArrowRight") destino = (i + 1) % n;
        else if (e.key === "ArrowLeft") destino = (i - 1 + n) % n;
        else if (e.key === "Home") destino = 0;
        else if (e.key === "End") destino = n - 1;
        if (destino !== null) { e.preventDefault(); elegir(destino, true); }
      });
    });

    grupo.insertBefore(lista, grupo.firstChild);
    grupo.classList.add("activas");
    elegir(0, false);
  });

  /* 4. Barras que crecen al aparecer ------------------------------------- */
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

  /* 5. Cuenta de fuentes en la bibliografía ------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-cuenta]"), function (span) {
    var lista = span.closest("details").querySelector("ul");
    if (lista) span.textContent = "(" + lista.children.length + ")";
  });
})();
