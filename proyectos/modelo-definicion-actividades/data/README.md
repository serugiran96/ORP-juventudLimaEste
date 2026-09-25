# Datos del proyecto

Los archivos de `data/raw/` y `data/processed/` **no se suben al repositorio**. Se regeneran con los
scripts de `scripts/` (ver "Cómo reproducir" en el `README.md` del proyecto). Este archivo documenta su
contenido.

## Nivel geográfico

Todas las tablas procesadas tienen la columna `nivel_geografico`, y sus valores **no se mezclan**:

| Valor | Significado | ¿Se puede atribuir a Lima Este? |
|---|---|---|
| `distrito` | Un distrito (UBIGEO). La columna `lima_este` marca los 7 del proyecto. | Sí, al distrito correspondiente |
| `lima_este_agregado` | Suma de los 7 distritos (solo para datos distritales) | Sí |
| `lima_metropolitana` | 43 distritos de la provincia de Lima (sin el Callao) | **No** |
| `nacional` | Perú | **No** |

## `data/raw/dato_joven/` — extracción de Dato Joven

Los genera `scripts/extraer_dato_joven.py`. Contienen solo resultados de consultas agregadas. En
`_metadatos.json` se registra, para cada archivo, el tablero de origen, la tabla, los filtros, la fecha
de extracción y la fecha de última actualización del tablero.

| Archivo | Contenido |
|---|---|
| `distritos_lima_metropolitana.csv` | UBIGEO y nombre de los 43 distritos |
| `poblacion_joven_distritos_lima.csv` | Población de 15–29 años por distrito, año (2019–2026), sexo y grupo de edad |
| `poblacion_total_distritos_lima.csv` | Población total por distrito, año y sexo |
| `poblacion_joven_nacional.csv`, `poblacion_total_nacional.csv` | Totales del país (fila UBIGEO `000000`) |
| `encuestas_regionales.csv` | 38 tableros de encuestas, tabla `datosRegionales`, regiones "LIMA METROPOLITANA" y "NACIONAL" |
| `encuestas_nacionales.csv` | Los mismos tableros, tabla `datosNacionales` (desagregaciones solo nacionales) |
| `consolidado_regionales.csv` | Tablero consolidado "Indicadores regionales" (34 tablas), las mismas dos regiones |
| `renoj_organizaciones_distritos_lima.csv` | Número de organizaciones del RENOJ por distrito × año de acreditación × tipo × temática |
| `voluntariado_distritos_lima.csv` | Número de personas voluntarias inscritas por distrito × una variable a la vez |

## `data/processed/` — datos de la Capa 1

Los genera `scripts/procesar_capa1.py`, salvo `capa1_resumen_lima_metropolitana.csv`, que lo genera el
notebook `notebooks/01_capa1_diagnostico.ipynb`.

### `capa1_poblacion_joven_distritos.csv`
Una fila por distrito × año × sexo × grupo de edad. Columnas: `nivel_geografico`, `ubigeo`, `distrito`,
`lima_este`, `anio`, `sexo` (hombre / mujer), `grupo_edad` (15 a 19, 20 a 24, 25 a 29), `poblacion`.

### `capa1_poblacion_resumen.csv`
Una fila por unidad geográfica × año (2019–2026): los 43 distritos, el agregado de Lima Este, Lima
Metropolitana y Perú. Columnas: `joven_15_29`, `joven_15_19`, `joven_20_24`, `joven_25_29`,
`joven_hombre`, `joven_mujer`, `poblacion_total`, `pct_joven` (% de jóvenes en la población total) y
`pct_mujer_joven` (% de mujeres entre los jóvenes).
**Advertencia:** las variaciones entre años no son interpretables (ver `fuentes/metodologia_capa1.md`, D5).

### `capa1_indicadores_encuestas.csv`
Una fila por indicador × nivel geográfico × desagregación × año.

| Columna | Descripción |
|---|---|
| `dimension` | Dimensión del mapa analítico (Educación, Empleo y situación laboral, etc.) |
| `tablero` | Tablero de Dato Joven (o tabla del consolidado, si `origen` = `consolidado`) |
| `indicador` | Nombre del indicador o categoría, tal como lo publica la fuente |
| `fuente` | ENAHO, EPEN, ENDES o ENAPRES (algunos combinan ENAHO y EPEN) |
| `poblacion` | Rango de edad (por ejemplo, `15-29`, `18-29`, `17-24`) |
| `nivel_geografico` | `lima_metropolitana` o `nacional` |
| `desagregacion` | `total`, `hombre`, `mujer`, `urbano` o `rural` |
| `anio` | Año |
| `valor` | Valor numérico (sin el símbolo %) |
| `unidad` | `%`, `años` o `soles` |
| `cv` | Coeficiente de variación (%) |
| `referencial` | `True` si CV > 15 %; la fuente pone esos valores entre paréntesis |
| `sin_dato` | `True` si la fuente publica "(¬)" |
| `origen` | `tablero_individual` o `consolidado` |
| `excluida_por_etiqueta_ambigua` | `True` si la fuente repite la misma etiqueta con valores distintos (no usar) |
| `en_periodo_prioritario` | `True` para 2022–2026 |

### `capa1_indicadores_encuestas_desagregacion_nacional.csv`
Mismas columnas, solo nivel nacional, con desagregaciones por etnia, lengua materna, pobreza, nivel
educativo y dominio geográfico.

### `capa1_resumen_lima_metropolitana.csv`
Resumen por indicador para Lima Metropolitana: valor inicial (2022 o primer año disponible), último valor,
cambio y si es distinguible del error de muestreo (prueba aproximada), valores por sexo y valor nacional.

### `capa1_renoj_organizaciones.csv` y `capa1_renoj_resumen_distritos.csv`
Organizaciones juveniles acreditadas por distrito, año de acreditación, tipo y temática. El resumen tiene,
por distrito: `organizaciones_acumuladas` (2019–2026), `acreditadas_2022_2026`, `joven_15_29` (2026) y
`organizaciones_por_10mil_jovenes`.

### `capa1_voluntariado_distritos.csv` y `capa1_voluntariado_resumen_distritos.csv`
Personas inscritas en el Programa de Voluntariado Juvenil por distrito × variable × valor, con
`pct_del_distrito`. El resumen tiene `personas_inscritas` e `inscritas_por_10mil_jovenes`.
**Solo como señal complementaria:** son personas que se inscribieron por decisión propia.

### `control_consolidado_vs_tableros.csv`
Valores que difieren entre el tablero consolidado y los tableros individuales. Vacío en la última
extracción: los 399 valores comunes coinciden.
