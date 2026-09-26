# Paleta y ayudas para gráficos del observatorio.
#
# Código de color fijo en todo el observatorio (el color dice el ámbito del dato, nunca "mejor" o "peor"):
#   Lima Este = rojo · Lima Metropolitana = negro · Perú urbano / estudios exploratorios = gris con borde discontinuo.
# Precisión: marcador lleno = confiable; marcador hueco = referencial (CV 15-25 %); no publicable = no se dibuja.

ROJO <- "#c42b1f"
TINTA <- "#1c1b1a"
TINTA_2 <- "#56524c"
GRIS <- "#8a857d"
GRIS_CLARO <- "#cfcac2"
LINEA <- "#e6e2db"
FONDO <- "#faf8f5"
BLANCO <- "#ffffff"

COLOR_AMBITO <- c("Lima Este" = ROJO, "Lima Metropolitana" = TINTA, "Perú urbano" = GRIS, "Nacional" = GRIS)
COLOR_SEXO <- c("Mujeres" = TINTA, "Hombres" = GRIS)
COLOR_EVIDENCIA <- c("oferta" = GRIS_CLARO, "participación declarada" = TINTA_2, "demanda observada" = ROJO)

AMBITO <- c(lima_este = "Lima Este", lima_metropolitana = "Lima Metropolitana", nacional = "Nacional")
SEXO <- c(total = "Total", hombre = "Hombres", mujer = "Mujeres")

# Tema común de plotly: tipografía, coma decimal, sin barra de herramientas.
tema <- function(p, alto = 320, margen_izq = 10, leyenda = TRUE, ...) {
  p$height <- alto  # alto del contenedor del widget (si no, htmlwidgets reserva 400 px)
  p |>
    layout(
      height = alto, separators = ", ",
      font = list(family = "IBM Plex Sans, system-ui, sans-serif", size = 13, color = TINTA_2),
      paper_bgcolor = BLANCO, plot_bgcolor = BLANCO,
      margin = list(l = margen_izq, r = 16, t = if (leyenda) 36 else 10, b = 40),
      hoverlabel = list(bgcolor = BLANCO, bordercolor = LINEA, font = list(color = TINTA, size = 12)),
      xaxis = list(gridcolor = LINEA, zeroline = FALSE, linecolor = GRIS_CLARO, fixedrange = TRUE),
      yaxis = list(gridcolor = "rgba(0,0,0,0)", zeroline = FALSE, linecolor = GRIS_CLARO, fixedrange = TRUE,
                   automargin = TRUE),
      showlegend = leyenda,
      legend = list(orientation = "h", x = 0, y = 1, yanchor = "bottom", font = list(size = 12), traceorder = "normal"),
      ...
    ) |>
    config(displayModeBar = FALSE, locale = "es", responsive = TRUE)
}

# Texto del tooltip de una estimación de encuesta.
tooltip_est <- function(etiqueta, valor, ic_inf, ic_sup, precision, n = NA, extra = "") {
  paste0("<b>", etiqueta, "</b><br>", num(valor, 1), " %",
         ifelse(is.na(ic_inf), "", paste0(" (IC 95 %: ", num(ic_inf, 1), "–", num(ic_sup, 1), ")")),
         "<br>Precisión: ", precision, ifelse(is.na(n), "", paste0(" · n = ", num(n))), extra)
}

# Gráfico de puntos con intervalo de confianza: una fila por categoría, una serie por ámbito o sexo.
# df: categoria, serie, valor, ee, precision, (n_muestral). colores: vector con nombre por serie.
puntos_ic <- function(df, colores, alto = NULL, rango = NULL, orden = NULL, titulo_x = "% de jóvenes",
                      simbolos = NULL) {
  df <- df |> filter(precision != "no_publicable") |>
    mutate(ic_inf = pmax(valor - 1.96 * ee, 0), ic_sup = valor + 1.96 * ee,
           hueco = precision == "referencial",
           texto = tooltip_est(paste(serie, "·", categoria), valor, ic_inf, ic_sup, precision,
                               if ("n_muestral" %in% names(df)) n_muestral else NA))
  niveles <- if (is.null(orden)) df |> group_by(categoria) |> summarise(v = max(valor)) |> arrange(v) |> pull(categoria)
             else rev(orden)
  df$categoria <- factor(df$categoria, levels = niveles)
  series <- intersect(names(colores), unique(df$serie))
  desp <- setNames(seq(-0.18, 0.18, length.out = max(length(series), 1)), series)
  if (length(series) == 1) desp[] <- 0
  p <- plot_ly()
  for (s in series) {
    # el primer punto define el símbolo de la leyenda: se ordena para que sea una estimación confiable (lleno)
    d <- df |> filter(serie == s) |> mutate(y = as.numeric(categoria) + desp[[s]]) |> arrange(hueco)
    p <- p |>
      add_segments(data = d, x = ~ic_inf, xend = ~ic_sup, y = ~y, yend = ~y, line = list(color = colores[[s]], width = 2),
                   hoverinfo = "skip", showlegend = FALSE, opacity = 0.55) |>
      add_markers(data = d, x = ~valor, y = ~y, name = s, text = ~texto, hoverinfo = "text",
                  marker = list(size = 10, color = ifelse(d$hueco, BLANCO, colores[[s]]),
                                symbol = if (is.null(simbolos)) "circle" else simbolos[[s]],
                                line = list(color = colores[[s]], width = 2)))
  }
  alto <- alto %||% (96 + 34 * length(niveles))
  p |> tema(alto = alto) |>
    layout(xaxis = list(title = list(text = titulo_x, font = list(size = 12)), range = rango, ticksuffix = " %"),
           yaxis = list(tickvals = seq_along(niveles), ticktext = niveles, title = ""))
}

# Barras horizontales simples con etiqueta directa.
barras_h <- function(df, x, y, color = ROJO, texto = NULL, alto = NULL, sufijo = "", titulo_x = "", hover = NULL) {
  df <- df |> mutate(.y = factor({{ y }}, levels = df |> arrange({{ x }}) |> pull({{ y }})))
  alto <- alto %||% (60 + 30 * nrow(df))
  plot_ly(df, x = rlang::enquo(x), y = ~.y, type = "bar", orientation = "h",
          marker = list(color = color), text = texto, textposition = "outside", cliponaxis = FALSE,
          hovertext = hover, hoverinfo = if (is.null(hover)) "x+y" else "text") |>
    tema(alto = alto, leyenda = FALSE) |>
    layout(xaxis = list(title = list(text = titulo_x, font = list(size = 12)), ticksuffix = sufijo),
           yaxis = list(title = ""), bargap = 0.35)
}

`%||%` <- function(a, b) if (is.null(a)) b else a
