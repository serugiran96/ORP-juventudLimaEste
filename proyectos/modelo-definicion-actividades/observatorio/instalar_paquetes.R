# Instala los paquetes de R que necesita el observatorio (solo la primera vez).
# Uso, desde la carpeta observatorio/:  Rscript instalar_paquetes.R

paquetes <- c("dplyr", "tidyr", "readr", "stringr", "purrr", "htmltools",
              "plotly", "DT", "crosstalk", "jsonlite", "knitr", "rmarkdown")
faltan <- setdiff(paquetes, rownames(installed.packages()))
if (length(faltan) > 0) {
  install.packages(faltan, repos = "https://cloud.r-project.org")
} else {
  message("Todos los paquetes ya están instalados.")
}
