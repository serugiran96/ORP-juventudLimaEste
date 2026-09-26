# Piezas de página del observatorio (HTML construido con htmltools).
#
# Patrón de lectura de cada visualización: GRÁFICO o INDICADOR → "¿Qué nos dice?" (2-3 líneas) → "Importante"
# (una limitación breve) → fuente y ámbito.

kpi <- function(valor, etiqueta, nota = NULL, acento = FALSE) {
  div(class = paste("kpi", if (acento) "kpi-acento"),
      div(class = "kpi-valor", valor), div(class = "kpi-etiqueta", etiqueta),
      if (!is.null(nota)) div(class = "kpi-nota", nota))
}
kpis <- function(...) div(class = "kpis", ...)

chip_ambito <- function(ambito) {
  clase <- switch(ambito, "Lima Este" = "amb-le", "Lima Metropolitana" = "amb-lm", "Perú urbano" = "amb-pu",
                  "Distrito" = "amb-di", "Registro publicado" = "amb-reg", "amb-pu")
  span(class = paste("amb", clase), ambito)
}

# Tarjeta de visualización con lectura guiada.
bloque <- function(titulo, visual, dice, importante = NULL, fuente = NULL, ambito = NULL, id = NULL) {
  div(class = "bloque", id = id,
      div(class = "bloque-cab", h3(titulo), if (!is.null(ambito)) div(class = "ambitos", lapply(ambito, chip_ambito))),
      div(class = "bloque-visual", visual),
      div(class = "lectura",
          div(class = "dice", span(class = "lbl", "¿Qué nos dice?"), HTML(dice)),
          if (!is.null(importante)) div(class = "importante", span(class = "lbl", "Importante"), HTML(importante))),
      if (!is.null(fuente)) div(class = "fuente", HTML(paste("Fuente:", fuente))))
}

# Pestañas internas de una página (las activa observatorio.js).
subtabs <- function(id, ...) {
  pestanas <- list(...)
  nombres <- names(pestanas)
  claves <- paste0(id, "-", seq_along(pestanas))
  tagList(
    div(class = "subtabs", role = "tablist",
        lapply(seq_along(pestanas), function(i)
          tags$button(class = paste("subtab", if (i == 1) "activo"), role = "tab",
                      `data-subtab` = claves[i], `aria-selected` = if (i == 1) "true" else "false", nombres[i]))),
    lapply(seq_along(pestanas), function(i)
      div(class = "subpanel", id = claves[i], hidden = if (i > 1) NA else NULL, pestanas[[i]]))
  )
}

aviso <- function(..., clase = "") div(class = paste("aviso", clase), ...)
encabezado <- function(titulo, bajada, capa = NULL) {
  div(class = "pag-cab", if (!is.null(capa)) div(class = "eyebrow", capa), h2(titulo), p(class = "bajada", bajada))
}

# Filtros de chips (una fila por campo). `campos` = list(campo = list(etiqueta = "…", valores = c(valor = "texto")))
# Los elementos filtrables llevan data-filtrable = objetivo y data-f-<campo> = "valor1|valor2".
filtro_chips <- function(objetivo, campos) {
  div(class = "filtros", `data-filtros` = objetivo,
      lapply(names(campos), function(campo) {
        cf <- campos[[campo]]
        div(class = "filtro", span(class = "lbl", cf$etiqueta),
            div(class = "chips", `data-campo` = campo,
                tags$button(class = "chip activo", `data-valor` = "", "Todos"),
                lapply(names(cf$valores), function(v) tags$button(class = "chip", `data-valor` = v, cf$valores[[v]]))))
      }),
      span(class = "contador", `data-contador` = objetivo))
}
f_attr <- function(x) paste(str_split(x, ";\\s*")[[1]], collapse = "|")

# Los textos de resultados/ marcan "(referencial)"; en el observatorio la marca es el asterisco.
marca_ref <- function(x) {
  x <- gsub("(\\d) \\(referencial\\)", "\\1*", x)
  gsub(" \\(referencial\\)", "*", x)
}

# Referencias cruzadas: evidencias (con su ficha técnica al pasar el cursor), hallazgos y fichas (enlaces).
ref_ev <- function(ids) {
  ids <- str_split(ids, ";\\s*")[[1]]
  lapply(ids[ids %in% rownames(EV)], function(i) {
    e <- EV[i, ]
    span(class = "ref", tabindex = "0",
         title = paste0(e$indicador, " · ", e$poblacion, " · ", e$ambito, " · ", e$periodo, " · ", e$fuente), i)
  })
}
ref_enlaces <- function(ids) {
  if (is.na(ids)) return(NULL)
  ids <- str_split(ids, ";\\s*")[[1]]
  lapply(ids, function(i) a(class = "ref", href = paste0("#", i), i))
}
