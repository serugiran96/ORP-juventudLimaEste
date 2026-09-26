# Paquetes que usa el observatorio.
# Si falta alguno, ejecuta primero: source("instalar_paquetes.R")

suppressPackageStartupMessages({
  library(dplyr)      # transformar tablas: filter(), mutate(), summarise()...
  library(tidyr)      # reordenar tablas: pivot_longer(), separate_rows()...
  library(readr)      # leer archivos CSV
  library(stringr)    # trabajar con texto
  library(purrr)      # aplicar funciones a listas: map()
  library(htmltools)  # construir HTML desde R: div(), p(), span()...
  library(plotly)     # gráficos interactivos
  library(DT)         # tablas interactivas
  library(crosstalk)  # filtros que conectan gráficos y tablas sin servidor
  library(jsonlite)   # pasar datos de R al JavaScript de la página
})
