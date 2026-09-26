# Piezas de la página de Actividades: cada ficha se lee como un recorrido de ocho pasos.
#
# Para quién → Qué sabemos → Tamaño o alcance → Práctica o interés → Convocatoria → Barreras → Qué no sabemos →
# Qué habría que validar. Todo el contenido sale de resultados/fichas_*.csv; aquí solo se ordena y se dibuja.
# El estado de cada paso (dato, señal débil, sin evidencia, no aplica) se asigna con reglas fijas a partir de los
# códigos de la integración (fuentes/metodologia_integracion.md, sección 4). No es un puntaje: no se suma.

PASOS <- c("Para quién", "Qué sabemos", "Tamaño o alcance", "Práctica o interés relacionado",
           "Evidencia de convocatoria", "Barreras", "Qué no sabemos", "Qué habría que validar")

ALCANCE_TXT <- c("amplia" = "Toda la juventud", "segmento identificable" = "Segmento identificable",
                 "desconocido" = "No estimable", "no aplica" = "No aplica")
ALCANCE_CLASE <- c("amplia" = "amplia", "segmento identificable" = "segmento", "desconocido" = "desconocido",
                   "no aplica" = "no-aplica")

# ---------------------------------------------------------------------------------------------------------
# Texto: viñetas "• a • b", barreras "[directa] …" y la marca de las cifras referenciales.
vinetas <- function(x) {
  if (is.na(x) || !str_detect(x, "•")) return(p(marca_ref(x)))
  items <- str_trim(str_split(x, "•")[[1]])
  tags$ul(lapply(items[items != ""], function(i) tags$li(marca_ref(i))))
}
barreras_lista <- function(x) {
  partes <- str_match_all(x, "\\[(directa|indirecta|sin datos)\\]\\s*([^\\[]+)")[[1]]
  if (nrow(partes) == 0) return(p(marca_ref(x)))
  tags$ul(class = "barreras", lapply(seq_len(nrow(partes)), function(i)
    tags$li(span(class = paste("pert-b", str_replace(partes[i, 2], " ", "-")), partes[i, 2]), " ",
            marca_ref(str_trim(partes[i, 3])))))
}
cuenta_barreras <- function(x) {
  t <- str_match_all(x, "\\[(directa|indirecta|sin datos)\\]")[[1]][, 2]
  n <- table(factor(t, levels = c("directa", "indirecta", "sin datos")))
  paste(c(if (n[1]) paste(n[1], if (n[1] == 1) "directa" else "directas"),
          if (n[2]) paste(n[2], if (n[2] == 1) "indirecta" else "indirectas"),
          if (n[3]) "sin datos"), collapse = " · ")
}
n_items <- function(x) if (is.na(x) || !str_detect(x, "•")) 0 else sum(str_trim(str_split(x, "•")[[1]]) != "")

# ---------------------------------------------------------------------------------------------------------
# Estado de cada paso para el recorrido visual (reglas de la sección 4 de la metodología).
#   def = definición de la ficha · dato = dato observado · debil = señal débil o indirecta
#   vacio = sin evidencia (o vacío de información) · na = no aplica · validar = pendiente de validar con jóvenes
estado_pasos <- function(f) {
  nec <- switch(f$necesidad_tipo, "sin evidencia" = "vacio", "objetivo institucional" = "debil", "dato")
  if (str_detect(f$necesidad_tipo, ";")) nec <- "dato"
  tam <- switch(f$alcance_tipo, "desconocido" = "vacio", "no aplica" = "na", "dato")
  int <- switch(f$interes_codigo, "P0" = "vacio", "I1" = "debil", "no aplica" = "na", "dato")
  conv <- switch(f$convocatoria_codigo, "C0" = "vacio", "C1" = "vacio", "C2" = "debil", "no aplica" = "na", "dato")
  tb <- str_match_all(f$barreras, "\\[(directa|indirecta|sin datos)\\]")[[1]][, 2]
  bar <- if ("directa" %in% tb) "dato" else if ("indirecta" %in% tb) "debil" else "vacio"
  c("def", nec, tam, int, conv, bar, "vacio", "validar")
}

# Qué dice cada casilla del recorrido (una etiqueta corta).
resumen_pasos <- function(f, segs) {
  tam <- if (nrow(segs) > 0 && f$alcance_tipo %in% c("amplia", "segmento identificable"))
    paste0("≈ ", num(min(segs$personas_base_dato_joven_inf) / 1000), "–", num(max(segs$personas_base_dato_joven_sup) / 1000), " mil")
  else ALCANCE_TXT[[f$alcance_tipo]]
  c(str_replace(f$tipo_ficha, "población que requiere consulta directa", "consulta directa"),
    paste("necesidad:", f$necesidad_tipo), tam, f$interes_codigo, f$convocatoria_codigo, cuenta_barreras(f$barreras),
    paste(n_items(f$vacios), if (n_items(f$vacios) == 1) "vacío" else "vacíos"), participacion(f)$corto)
}

# ---------------------------------------------------------------------------------------------------------
# Participación concreta: siempre por validar con jóvenes (ninguna fuente llega a I2), salvo que la ficha no
# convoque. El matiz sale del código de convocatoria.
participacion <- function(f) {
  if (f$tipo_ficha == "protocolo transversal")
    return(list(corto = "no convoca", tag = "Protocolo: no convoca",
                texto = "No es una actividad de convocatoria: se aplica en toda actividad con adolescentes. Lo que se verifica es su aplicación, no la participación."))
  if (f$tipo_ficha == "población que requiere consulta directa")
    return(list(corto = "consultar", tag = "Requiere consulta directa",
                texto = "No sabemos qué actividad le sería útil: hay que consultar a este grupo antes de diseñar cualquier actividad. No se propone una actividad."))
  matiz <- switch(f$convocatoria_codigo,
    "C4" = "Hay demanda observada en una oferta parecida, pero vale solo para esa oferta concreta.",
    "C3" = "Hay participación declarada en ofertas comparables, sin cupos publicados.",
    "C2" = "Solo hay señales débiles de convocatoria (sin cifra o poco comparables).",
    "C1" = "Solo hay oferta, sin datos de participación.",
    "C0" = "No hay datos de convocatoria comparables (no es evidencia negativa).")
  list(corto = "por validar", tag = "Participación por validar con jóvenes",
       texto = paste("Ninguna fuente preguntó a los jóvenes de Lima Este si participarían en esta actividad (I2).", matiz))
}

recorrido <- function(f, segs) {
  est <- estado_pasos(f)
  res <- resumen_pasos(f, segs)
  tags$ol(class = "recorrido", `aria-label` = "Recorrido de la ficha",
          lapply(seq_along(PASOS), function(i)
            tags$li(class = paste("rc", paste0("rc-", est[i])),
                    a(href = paste0("#", f$id, "-p", i), span(class = "rc-n", i), span(class = "rc-t", PASOS[i]),
                      span(class = "rc-v", res[i])))))
}

# ---------------------------------------------------------------------------------------------------------
# Tamaño: las dos bases de población en una escala común (0–500 mil) para todas las fichas.
ESCALA_MAX <- 500000
svg_tamano <- function(segs) {
  if (nrow(segs) == 0) return(NULL)
  ancho <- 560; x0 <- 10; x1 <- 540; fila <- 58
  alto <- 26 + fila * nrow(segs)
  sx <- function(v) x0 + (x1 - x0) * v / ESCALA_MAX
  marcas <- seq(0, ESCALA_MAX, 100000)
  # Rango en texto junto al intervalo: a la derecha, o a la izquierda si no cabe.
  etiqueta <- function(inf, sup, y) {
    txt <- paste0(num(inf / 1000), "–", num(sup / 1000), " mil")
    if (sx(sup) + 90 > ancho) tags$text(x = sx(inf) - 6, y = y, class = "t-val", `text-anchor` = "end", txt)
    else tags$text(x = sx(sup) + 6, y = y, class = "t-val", txt)
  }
  filas <- lapply(seq_len(nrow(segs)), function(i) {
    s <- segs[i, ]; y <- 14 + fila * (i - 1)
    pe <- EV[s$evidencia, "personas_encuesta"]; ee <- 1.96 * EV[s$evidencia, "personas_encuesta_ee"]
    tagList(
      tags$text(x = x0, y = y, class = "t-seg", paste0(s$id, " · ", num(s$porcentaje, 1), " % ",
                                                      str_replace(s$poblacion_de_referencia, "-", "–"))),
      tags$line(x1 = sx(s$personas_base_dato_joven_inf), x2 = sx(s$personas_base_dato_joven_sup), y1 = y + 14, y2 = y + 14,
                class = "l-dj"),
      etiqueta(s$personas_base_dato_joven_inf, s$personas_base_dato_joven_sup, y + 18),
      if (!is.na(pe)) tagList(
        tags$line(x1 = sx(pe - ee), x2 = sx(pe + ee), y1 = y + 30, y2 = y + 30, class = "l-enc"),
        tags$rect(x = sx(pe) - 4, y = y + 26, width = 8, height = 8, class = "m-enc"),
        etiqueta(pe - ee, pe + ee, y + 34))
    )
  })
  ejes <- lapply(marcas, function(m) tagList(
    tags$line(x1 = sx(m), x2 = sx(m), y1 = 4, y2 = alto - 16, class = "g-lin"),
    tags$text(x = sx(m), y = alto - 2, class = "t-eje", `text-anchor` = if (m == 0) "start" else if (m == ESCALA_MAX) "end" else "middle",
              if (m == 0) "0" else paste0(num(m / 1000), " mil"))))
  tags$svg(class = "svg-tam", viewBox = paste(0, 0, ancho, alto), role = "img",
           `aria-label` = "Tamaño del segmento con las dos bases de población", ejes, filas)
}

# ---------------------------------------------------------------------------------------------------------
# Registros de convocatoria citados por la ficha.
COMP <- c("sí" = "●", "parcial" = "◐", "no" = "○")
tabla_convocatoria <- function(regs) {
  if (nrow(regs) == 0) return(NULL)
  div(class = "desplazable", tags$table(class = "tabla-simple conv-reg",
    tags$thead(tags$tr(tags$th("Código"), tags$th("Registro"), tags$th("Cifra declarada"),
                       tags$th(title = "Segmento · territorio · formato · costo (● sí, ◐ parcial, ○ no)", "Comparable (S·T·F·C)"))),
    tags$tbody(lapply(seq_len(nrow(regs)), function(i) {
      r <- regs[i, ]
      tags$tr(tags$td(span(class = paste("cod", if (r$codigo == "no comparable") "cod-na"), r$codigo)),
              tags$td(tags$b(r$actividad_c3), " ", r$nombre, tags$br(),
                      tags$small(class = "meta", paste0(r$distrito, " · público: ", r$publico, " · ", r$evidencia_c3))),
              tags$td(if (!is.na(r$cifra_declarada)) paste(num(r$cifra_declarada), r$cifra_tipo)
                      else tags$small(class = "meta", r$nota)),
              tags$td(class = "mono", title = paste0("segmento: ", r$comparable_segmento, "; territorio: ", r$comparable_territorio,
                                                    "; formato: ", r$comparable_formato, "; costo: ", r$comparable_costo),
                      paste(COMP[c(r$comparable_segmento, r$comparable_territorio, r$comparable_formato, r$comparable_costo)],
                            collapse = " ")))
    }))))
}

# Componentes agrupados por lo que la evidencia permite decir de ellos.
GRUPO_COMP <- c("respaldado en dos o más dimensiones" = "Con respaldo en la evidencia",
                "respaldado en una dimensión" = "Con respaldo en la evidencia",
                "solo señales débiles" = "Por validar", "hipótesis de diseño" = "Por validar",
                "sin evidencia" = "Por validar",
                "complementario (ya existe)" = "Ya existe, transversal o descartado",
                "condición transversal" = "Ya existe, transversal o descartado",
                "descartado" = "Ya existe, transversal o descartado")
bloque_componentes <- function(comps) {
  if (nrow(comps) == 0) return(NULL)
  grupos <- unique(GRUPO_COMP)
  div(class = "comps", lapply(grupos, function(g) {
    cc <- comps[GRUPO_COMP[comps$estado] == g, ]
    div(class = "comp-col", span(g),
        if (nrow(cc) == 0) div(class = "comp", tags$small("—")) else
          lapply(seq_len(nrow(cc)), function(i)
            div(class = paste("comp", if (cc$estado[i] == "descartado") "comp-descartado"),
                cc$componente[i], tags$small(paste0(cc$estado[i], ". ", marca_ref(cc$nota[i]))))))
  }))
}

# ---------------------------------------------------------------------------------------------------------
paso <- function(f, i, ..., codigo = NULL, clase = NULL, nota = NULL) {
  tags$li(class = paste("paso", clase), id = paste0(f$id, "-p", i),
          div(class = "paso-tit", tags$b(PASOS[i]), if (!is.null(codigo)) div(codigo),
              if (!is.null(nota)) tags$small(class = "meta", nota)),
          div(class = "paso-cont", ...))
}
cod <- function(x, na = FALSE) span(class = paste("cod", if (na) "cod-na"), x)

ficha_html <- function(f, visible = FALSE) {
  ids_seg <- if (is.na(f$segmentos)) character(0) else str_split(f$segmentos, ";\\s*")[[1]]
  segs <- segmentos |> filter(id %in% ids_seg)
  regs <- convocatoria_f |> filter(ficha == f$id)
  comps <- componentes_f |> filter(ficha == f$id)
  part <- participacion(f)
  int <- str_match(f$interes, "^\\[[^\\]]+\\]\\s*(.*?)(\\s*Salto inferencial:\\s*(.*))?$")
  conv_txt <- if (f$convocatoria_codigo == "C0") str_remove(f$convocatoria, "\\s*Registros no comparables:.*$")
              else if (f$convocatoria_codigo == "no aplica") "No aplica: esta ficha no es una actividad de convocatoria."
              else paste0(f$convocatoria_detalle_codigo, ".")
  convoca <- f$tipo_ficha %in% c("actividad de convocatoria abierta", "intervención segmentada")

  div(class = "ficha", id = f$id, hidden = if (!visible) NA,
      div(class = "ficha-cab",
          div(class = "ficha-tags", span(class = "id", f$id), span(class = "tag", f$linea),
              span(class = "tag tag-tipo", f$tipo_ficha), span(class = "tag tag-aviso", part$tag)),
          h3(f$actividad),
          recorrido(f, segs)),
      tags$ol(class = "pasos",
        paso(f, 1, codigo = cod(f$tipo_ficha),
             p(marca_ref(f$poblacion)),
             if (length(ids_seg)) div(class = "meta", "Segmentos: ", lapply(ids_seg, function(s)
               span(class = "ref", title = segmentos$segmento[segmentos$id == s], s)))),
        paso(f, 2, codigo = cod(f$necesidad_tipo, na = f$necesidad_tipo == "sin evidencia"), clase = "sabemos",
             p(tags$b("Contexto o necesidad: "), marca_ref(f$necesidad)),
             div(tags$b("Lo que se puede afirmar con datos observados:"), vinetas(f$afirmaciones))),
        paso(f, 3, codigo = span(class = paste("pert", paste0("pert-", ALCANCE_CLASE[[f$alcance_tipo]])), ALCANCE_TXT[[f$alcance_tipo]]),
             nota = if (convoca || f$alcance_tipo == "segmento identificable") "El tamaño no indica prioridad.",
             p(marca_ref(f$alcance)),
             if (nrow(segs)) div(class = "tam", svg_tamano(segs),
                                 div(class = "tam-ley", span(class = "k-dj", "población 2026 de Dato Joven"),
                                     span(class = "k-enc", "total de la encuesta (IC 95 %)"),
                                     span("escala común a todas las fichas; las bases no se combinan")))),
        paso(f, 4, codigo = cod(f$interes_codigo, na = f$interes_codigo %in% c("P0", "no aplica")),
             p(marca_ref(int[1, 2])),
             if (!is.na(int[1, 4])) div(class = "salto", tags$b("Salto inferencial abierto"), marca_ref(int[1, 4])),
             if (convoca) p(class = "meta", "Interés declarado en participar en esta actividad (I2): ninguna fuente lo mide.")),
        paso(f, 5, codigo = cod(f$convocatoria_codigo, na = f$convocatoria_codigo %in% c("C0", "no aplica")),
             p(marca_ref(conv_txt)), tabla_convocatoria(regs),
             p(tags$b("Oferta existente en el territorio: "), f$oferta)),
        paso(f, 6, barreras_lista(f$barreras)),
        paso(f, 7, vinetas(f$vacios)),
        paso(f, 8, clase = "validar",
             p(tags$b(paste0(part$tag, ". ")), part$texto),
             if (!identical(f$hipotesis, "No aplica.")) div(tags$b("Hipótesis a probar:"), vinetas(f$hipotesis)),
             p(tags$b(if (convoca) "Qué medir en un piloto: " else "Cómo se verifica: "), f$validacion_piloto),
             p(tags$b("Dónde: "), f$donde),
             bloque_componentes(comps))),
      tags$details(class = "mas traza",
        tags$summary("Trazabilidad: evidencias, registros y cambios respecto de la primera versión"),
        div(class = "refs", style = "padding:8px 0;border:0", ref_ev(f$evidencias)),
        if (!is.na(f$actividades_c3)) p(class = "meta", tags$b("Actividades del registro de oferta: "), f$actividades_c3),
        p(class = "meta", tags$b("Primera versión: "), f$origen_v1, " · ", f$resultado_auditoria,
          if (!is.na(f$cambio_v1)) paste0(". ", f$cambio_v1))))
}
