/* Observatorio de Juventudes de Lima Este: navegación y filtros (sin servidor). */
(function () {
  var PAGINAS = ["inicio", "contexto", "intereses", "oferta", "cruce", "actividades"];

  // Tras mostrar contenido oculto, los gráficos y tablas deben recalcular su tamaño.
  function redimensionar(raiz) {
    window.dispatchEvent(new Event("resize"));
    if (window.Plotly) {
      (raiz || document).querySelectorAll(".js-plotly-plot").forEach(function (p) {
        try { Plotly.Plots.resize(p); } catch (e) {}
      });
    }
    if (window.jQuery && jQuery.fn.dataTable) {
      jQuery.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    }
  }

  // ---------- Router por hash: #pagina o #ancla-dentro-de-una-pagina
  function mostrar() {
    var h = decodeURIComponent((location.hash || "#inicio").slice(1));
    var pagina = PAGINAS.indexOf(h) >= 0 ? h : null;
    var destino = null;
    if (!pagina) {
      destino = document.getElementById(h);
      var contenedor = destino ? destino.closest(".obs-pagina") : null;
      pagina = contenedor ? contenedor.id : "inicio";
    }
    PAGINAS.forEach(function (p) {
      var s = document.getElementById(p);
      if (s) s.hidden = p !== pagina;
    });
    document.querySelectorAll(".obs-nav a").forEach(function (a) {
      a.classList.toggle("activo", a.getAttribute("href") === "#" + pagina);
    });
    if (destino) {
      var panel = destino.closest(".subpanel");
      if (panel && panel.hidden) activarSubtab(panel.id);
      var ficha = destino.closest(".ficha");
      if (ficha) mostrarFicha(ficha);
      if (destino.classList.contains("hallazgo")) mostrarElemento(destino);
      setTimeout(function () { destino.scrollIntoView({ block: "start" }); }, 30);
    } else {
      window.scrollTo(0, 0);
    }
    setTimeout(function () { redimensionar(document.getElementById(pagina)); }, 60);
  }

  // ---------- Pestañas internas
  function activarSubtab(clave) {
    var boton = document.querySelector('[data-subtab="' + clave + '"]');
    if (!boton) return;
    var grupo = boton.parentElement;
    grupo.querySelectorAll(".subtab").forEach(function (b) {
      var activo = b === boton;
      b.classList.toggle("activo", activo);
      b.setAttribute("aria-selected", activo ? "true" : "false");
      var panel = document.getElementById(b.getAttribute("data-subtab"));
      if (panel) panel.hidden = !activo;
    });
    redimensionar(document.getElementById(clave));
  }

  // ---------- Filtros de chips (fichas, patrones, hallazgos)
  // Cada grupo de filtros tiene data-filtros="nombre" y cada elemento filtrable data-f-<campo>.
  function aplicarFiltros(grupo) {
    var objetivo = grupo.getAttribute("data-filtros");
    var activos = {};
    grupo.querySelectorAll(".chips").forEach(function (c) {
      var campo = c.getAttribute("data-campo");
      var sel = c.querySelector(".chip.activo");
      var valor = sel ? sel.getAttribute("data-valor") : "";
      if (valor) activos[campo] = valor;
    });
    var visibles = 0, total = 0;
    document.querySelectorAll('[data-filtrable="' + objetivo + '"]').forEach(function (el) {
      total++;
      var ok = Object.keys(activos).every(function (campo) {
        var v = (el.getAttribute("data-f-" + campo) || "").split("|");
        return v.indexOf(activos[campo]) >= 0;
      });
      el.hidden = !ok;
      if (ok) visibles++;
    });
    var cont = document.querySelector('[data-contador="' + objetivo + '"]');
    if (cont) cont.textContent = visibles + " de " + total;
  }
  function mostrarElemento(el) {
    // Si un filtro oculta el elemento enlazado, se limpian los filtros de su grupo.
    if (!el.hidden) return;
    var objetivo = el.getAttribute("data-filtrable");
    var grupo = document.querySelector('[data-filtros="' + objetivo + '"]');
    if (!grupo) return;
    grupo.querySelectorAll(".chips").forEach(function (c) {
      c.querySelectorAll(".chip").forEach(function (b) { b.classList.toggle("activo", b.getAttribute("data-valor") === ""); });
    });
    aplicarFiltros(grupo);
  }

  // ---------- Actividades: una ficha visible a la vez; el índice marca la activa
  function mostrarFicha(ficha) {
    document.querySelectorAll(".fichas-cuerpo .ficha").forEach(function (f) { f.hidden = f !== ficha; });
    document.querySelectorAll(".fichas-indice .fi").forEach(function (a) {
      a.classList.toggle("activo", a.getAttribute("href") === "#" + ficha.id);
    });
  }

  // ---------- Oferta: contadores que siguen a los filtros de crosstalk
  function contadoresOferta() {
    var datos = document.getElementById("oferta-datos");
    if (!datos || !window.crosstalk) return;
    var filas = JSON.parse(datos.textContent);
    var filtro = new crosstalk.FilterHandle("oferta");
    function actualizar() {
      var claves = filtro.filteredKeys;
      var sel = claves ? filas.filter(function (f) { return claves.indexOf(f.id) >= 0; }) : filas;
      var cuenta = function (fn) { return sel.filter(fn).length; };
      var set = function (id, v) { var e = document.getElementById(id); if (e) e.textContent = v; };
      set("k-total", sel.length);
      set("k-juventud", cuenta(function (f) { return f.publico === "juventud"; }));
      set("k-participacion", cuenta(function (f) { return f.evidencia === "participación declarada"; }));
      set("k-demanda", cuenta(function (f) { return f.evidencia === "demanda observada"; }));
      set("k-gratuito", cuenta(function (f) { return f.costo === "gratuito"; }));
    }
    filtro.on("change", actualizar);
    actualizar();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".subtab").forEach(function (b) {
      b.addEventListener("click", function () { activarSubtab(b.getAttribute("data-subtab")); });
    });
    document.querySelectorAll("[data-filtros]").forEach(function (grupo) {
      grupo.querySelectorAll(".chip").forEach(function (b) {
        b.addEventListener("click", function () {
          b.parentElement.querySelectorAll(".chip").forEach(function (o) { o.classList.remove("activo"); });
          b.classList.add("activo");
          aplicarFiltros(grupo);
        });
      });
      aplicarFiltros(grupo);
    });
  });
  window.addEventListener("hashchange", mostrar);
  window.addEventListener("load", function () {
    mostrar();
    contadoresOferta();
  });
})();
