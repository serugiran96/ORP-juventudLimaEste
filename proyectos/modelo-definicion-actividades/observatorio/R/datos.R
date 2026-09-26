# Lectura y preparación de los datos del observatorio.
#
# El observatorio NO recalcula nada que ya haya hecho el pipeline de Python: lee los datasets finales de
# data/processed/, fuentes/ y resultados/ y solo los filtra, ordena o resume para graficarlos.
# Las cifras citadas en los textos salen de resultados/evidencias.csv (función ev()), igual que en el informe.

# ---------------------------------------------------------------------------------------------------------
# Rutas: Quarto ejecuta el código desde observatorio/, y los datos están en la carpeta del proyecto.
RAIZ <- normalizePath("..")
ruta <- function(...) file.path(RAIZ, ...)
leer <- function(...) read_csv(ruta(...), show_col_types = FALSE, progress = FALSE)

DISTRITOS <- c("Ate", "Chaclacayo", "El Agustino", "La Molina", "Lurigancho-Chosica",
               "San Juan de Lurigancho", "Santa Anita")

# ---------------------------------------------------------------------------------------------------------
# CAPA 1 — Contexto y necesidades
# Población 2026 por distrito, sexo y grupo de edad (solo nivel 2026: decisión D5).
poblacion <- leer("data/processed/capa1_poblacion_joven_distritos.csv") |>
  filter(lima_este, anio == 2026) |>
  mutate(sexo = recode(sexo, hombre = "Hombres", mujer = "Mujeres"),
         grupo_edad = str_replace(grupo_edad, " a ", "–"))
renoj <- leer("data/processed/capa1_renoj_resumen_distritos.csv")
voluntariado <- leer("data/processed/capa1_voluntariado_resumen_distritos.csv")
registros <- leer("data/processed/capa1_registros_resumen.csv")          # celdas < 10 ya ocultas
reg_anual <- leer("data/processed/capa1_registros_distrito_anio.csv")

# Estimaciones de Lima Este de la segunda integración (ENAHO, ENAPRES seguridad, ENUT)
segmentos_enaho <- leer("data/processed/integracion_enaho_segmentos.csv")
seguridad <- leer("data/processed/integracion_seguridad_enapres.csv")
tiempo <- leer("data/processed/integracion_tiempo_enut.csv")

# ---------------------------------------------------------------------------------------------------------
# CAPA 2 — Intereses, hábitos y barreras
enut <- leer("data/processed/capa2_uso_tiempo_enut.csv")
enapres <- leer("data/processed/capa2_cultura_enapres.csv")
enapres_edad <- leer("data/processed/integracion_cultura_edad_enapres.csv")
enaho_ed <- leer("data/processed/capa2_educacion_internet_enaho.csv")
ipsos <- leer("fuentes/capa2_estudios_ipsos.csv")

# ---------------------------------------------------------------------------------------------------------
# CAPA 3 — Oferta y convocatoria
oferta <- leer("fuentes/capa3_registro_oferta.csv")
notas_gobpe <- leer("data/raw/capa3/gobpe_listado.csv")

# ---------------------------------------------------------------------------------------------------------
# CRUCE — segunda integración (resultados/). Las fichas se leen de fichas_actividad.csv, que tiene los mismos
# textos que fichas_cadena.csv en columnas separadas.
evidencias <- leer("resultados/evidencias.csv")
hallazgos <- leer("resultados/hallazgos_integrados.csv")
patrones <- leer("resultados/patrones.csv")
segmentos <- leer("resultados/segmentos.csv")
fichas <- leer("resultados/fichas_actividad.csv")
componentes_f <- leer("resultados/fichas_componentes.csv")
convocatoria_f <- leer("resultados/fichas_convocatoria.csv")
cambios_v1 <- leer("resultados/cambios_primera_version.csv")
validacion <- leer("resultados/validacion_integracion.csv")

# ---------------------------------------------------------------------------------------------------------
# Formato (estilo peruano: coma decimal, espacio para los miles) y cifras citadas desde evidencias.csv
num <- function(x, d = 0) formatC(x, format = "f", digits = d, big.mark = " ", decimal.mark = ",")
pct <- function(x, d = 1) paste0(num(x, d), " %")
mil <- function(x) paste0(num(round(x / 1000)), " mil")

EV <- evidencias |> tibble::column_to_rownames("id")

# ev("E-110") -> "63,2 %"; con asterisco si la cifra es referencial. Mismas reglas que el informe:
# una cifra no publicable no se muestra.
ev <- function(id, marca = TRUE) {
  e <- EV[id, ]
  if (is.na(e$valor)) stop("Evidencia sin valor: ", id)
  if (identical(e$precision, "no_publicable")) stop("Evidencia no publicable: ", id)
  s <- switch(e$unidad,
              "%" = paste0(num(e$valor, if (e$precision == "sin error publicado") 0 else 1), " %"),
              "horas" = paste0(num(e$valor, 1), " horas"),
              "personas" = if (e$valor >= 10000) mil(e$valor) else num(e$valor),
              "por 1 000" = num(e$valor, 1), "por 10 000" = num(e$valor, 1),
              num(e$valor))
  # En el observatorio la marca de una cifra referencial es un asterisco (explicado en cada página).
  if (marca && identical(e$precision, "referencial")) s <- paste0(s, "*")
  s
}

# ev_personas("E-023") -> "≈ 119–140 mil según la población 2026 de Dato Joven; 136–177 mil según la encuesta"
ev_personas <- function(id) {
  e <- EV[id, ]
  partes <- c()
  if (!is.na(e$personas_dj_inf))
    partes <- c(partes, paste0(num(round(e$personas_dj_inf / 1000)), "–", mil(e$personas_dj_sup),
                               " según la población 2026 de Dato Joven"))
  if (!is.na(e$personas_encuesta)) {
    lo <- e$personas_encuesta - 1.96 * e$personas_encuesta_ee
    hi <- e$personas_encuesta + 1.96 * e$personas_encuesta_ee
    partes <- c(partes, paste0(num(round(lo / 1000)), "–", mil(hi), " según la encuesta"))
  }
  paste0("≈ ", paste(partes, collapse = "; "))
}

# Marca de precisión para gráficos: los valores no publicables se ocultan.
publicable <- function(df) df |> filter(precision != "no_publicable")
