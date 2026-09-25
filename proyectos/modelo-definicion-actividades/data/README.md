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
| `cnv_madres_15_19_distritos_lima.csv` | Nacimientos de madres de 15–19 años por distrito de residencia × año × edad de la madre. **Sensible: contiene celdas < 10** |
| `cem_casos_edad_sexo_distritos_lima.csv` | Casos atendidos en los CEM por distrito de domicilio × año × grupo de edad × sexo. **Sensible** |
| `cem_casos_tipo_violencia_distritos_lima.csv` | Casos atendidos en los CEM por distrito × año × tipo de violencia. **Sensible** |
| `discapacidad_certificados_distritos_lima.csv` | Certificados de discapacidad emitidos por distrito × año × grupo de edad × sexo. **Sensible** |
| `conadis_inscritos_distritos_lima.csv` | Inscripciones en el registro del CONADIS por distrito × año × grupo de edad × sexo. **Sensible** |

Los archivos marcados como **sensibles** son conteos agregados, pero incluyen celdas pequeñas. **No deben
compartirse ni analizarse directamente.** Se usan solo las versiones procesadas, que ocultan esas celdas.

## `data/raw/enaho/` — microdatos de la ENAHO

Los genera `scripts/empleo_enaho.py descargar`: son los archivos `enaho_{año}_modulo05.dta` (Módulo 05,
Empleo e Ingresos, ENAHO anual 2022–2025) descargados del portal de microdatos del INEI. En total ocupan
cerca de 1,5 GB.

## `data/raw/` — otras fuentes (Capa 2)

| Carpeta | Contenido | Script |
|---|---|---|
| `data/raw/enaho/modulo03_{año}/` | ENAHO 2022–2025, Módulo 03 (educación e internet), con cuestionarios y diccionarios | `capa2_educacion_internet_enaho.py descargar` |
| `data/raw/enapres/{año}_cap800A/` | ENAPRES 2022–2025, capítulo 800A (cultura), CSV con cuestionarios y diccionarios | `capa2_cultura_enapres.py descargar` |
| `data/raw/enaho/modulo02_{año}/` | ENAHO 2022–2025, Módulo 02 (miembros del hogar): parentesco, estado civil y edades de todos los miembros | `integracion_enaho_segmentos.py descargar` |
| `data/raw/enapres/{año}_cap600/`, `2025_cap400/` | ENAPRES 2022–2025, capítulo de seguridad ciudadana (600; 400 en 2025), CSV con cuestionario y diccionario | `integracion_seguridad_enapres.py descargar` |
| `data/raw/enut/2024/` | ENUT 2024, módulos 200 (personas), 600 (diario de uso del tiempo) y 700–900 (satisfacción) | `capa2_uso_tiempo_enut.py descargar` |
| `data/raw/ipsos/` | PDF públicos de Ipsos (infografías 2017–2022 y el reporte global de 2024) | Descarga manual |
| `data/raw/senaju/` | Informe *Jóvenes en Agenda* (2025), revisado y descartado | Descarga manual |

Las cifras de Ipsos transcritas a mano están en `fuentes/capa2_estudios_ipsos.csv`, que sí se versiona.

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

### Registros sensibles (celdas < 10 ocultas)
En todos estos archivos, `casos` queda vacío y `oculto` = `True` cuando el conteo es menor de 10 o cuando
se oculta de forma complementaria. `registro` toma los valores `maternidad_adolescente`,
`violencia_atendida_cem`, `violencia_cem_por_tipo`, `discapacidad_certificados` y `discapacidad_conadis`.

- **`capa1_registros_distrito_anio.csv`:** casos por distrito y año (43 distritos) y agregado de Lima Este.
  `periodo_parcial` indica los años incompletos (por ejemplo, CNV 2026: enero–junio).
- **`capa1_registros_distrito_desagregado.csv`:** casos 2022–2025 por distrito × `variable` (edad, sexo o
  tipo de violencia) × `categoria`, con `pct_del_distrito`. El agregado de Lima Este tiene
  `ubigeo` = `LIMA_ESTE`.
- **`capa1_registros_resumen.csv`:** por distrito, `casos_2022_2025`, `promedio_anual`, `poblacion_2026`
  (mujeres de 15–19 para el CNV; jóvenes de 15–29 para los demás), `tasa`, `tasa_por` y
  `mediana_lima_metropolitana`.

### `capa1_empleo_enaho.csv` y `capa1_empleo_enaho_validacion.csv`
Lo genera `scripts/empleo_enaho.py calcular`. Es un **cálculo propio** con microdatos de la ENAHO: desempleo,
tasa de actividad (PEA) y empleo formal/informal (este último solo en 2022–2023) de jóvenes de 15–29 años,
para Lima Metropolitana y el total nacional, 2022–2025, por sexo. Incluye `valor`, `ee` (error estándar),
`cv`, `referencial`, `n_muestral` y `replica_validada`. El archivo de validación compara 2022–2023 con Dato
Joven.

### `control_consolidado_vs_tableros.csv`
Valores que difieren entre el tablero consolidado y los tableros individuales. Vacío en la última
extracción: los 399 valores comunes coinciden.

## `data/processed/` — datos de la Capa 2

Estimaciones propias con microdatos del INEI. Todas tienen estas columnas comunes:

| Columna | Descripción |
|---|---|
| `periodo` | Año, o `2022-2025` si se agruparon las olas |
| `nivel_geografico` | `lima_este` (dominio no planificado), `lima_metropolitana` o `nacional` |
| `grupo_edad`, `sexo` | Grupo de edad (`15-29`, `15-19`, `20-24`, `25-29`, `30+`, `14+`) y sexo (`total`, `hombre`, `mujer`) |
| `familia`, `categoria` (o `item`) | Tipo de indicador y categoría |
| `valor`, `ee`, `cv` | Estimación (en %, salvo horas), error estándar y coeficiente de variación |
| `n_muestral` | Casos en la muestra del denominador |
| `precision` | `confiable` (CV ≤ 15), `referencial` (15–25) o `no_publicable` (CV > 25) |
| `valor_publicable` | `valor` si es publicable; vacío si no |

- **`capa2_uso_tiempo_enut.csv`** (ENUT 2024): `familia` = `participacion_semanal` (%), `horas_semanales_promedio`,
  `horas_semanales_entre_participantes` (horas), y la satisfacción con el tiempo libre (%).
- **`capa2_cultura_enapres.csv`** (ENAPRES 2022–2025): `familia` = `asistencia`, `patrimonio`, `bienes_culturales`
  (`categoria` = "Sí"), `forma_de_entrada` y `motivo_no_asistencia` (una fila por categoría); `item` es el servicio
  o bien cultural.
- **`capa2_educacion_internet_enaho.csv`** (ENAHO 2022–2025): `familia` = `internet`, `proposito_internet`
  (% de usuarios), `educacion`, `nivel_asistencia` y `motivo_no_asistencia`.
- **`capa2_educacion_internet_enaho_validacion.csv`**: comparación con Dato Joven.

## `data/raw/capa3/` — notas de prensa (Capa 3)

Material de revisión para codificar a mano el registro de oferta. No son datos para analizar directamente.

| Archivo | Contenido | Script |
|---|---|---|
| `gobpe_listado.csv` | Notas de las siete municipalidades en gob.pe (2024–2026) encontradas con algún término de búsqueda: distrito, UBIGEO, id, fecha, título, enlace y términos que la encontraron | `capa3_noticias_gobpe.py listar` |
| `noticias_gobpe.csv` | Las notas del listado que la búsqueda devolvió con un término sobre juventud, con su texto | `capa3_noticias_gobpe.py detalle` |
| `gobpe_sectores_listado.csv`, `noticias_gobpe_sectores.csv` | Notas del MTPE, IPD, Ministerio de Cultura, DEVIDA y Municipalidad de Lima que mencionan un distrito de Lima Este, con su texto | `capa3_noticias_gobpe.py sectores` y `detalle_sectores` |
| `noticias_munichosica.csv`, `noticias_serpar.csv`, `noticias_senaju.csv` | Notas de munichosica.pe, SERPAR y SENAJU (API de WordPress) | `capa3_noticias_wp.py` |
| `directorio_puntos_de_cultura.pdf` | Directorio del Ministerio de Cultura. Revisado y descartado: no indica el distrito | Descarga manual |

## `data/processed/` y `fuentes/` — Capa 3

- **`data/processed/capa3_notas_candidatas.csv`** (`capa3_triaje.py`): notas que mencionan a jóvenes, adolescentes o
  estudiantes y alguna actividad. Tiene fragmentos del texto con edades (`edades`), costos (`costo`), cifras
  (`cifras`) y posibles señales de demanda (`demanda`) para agilizar la lectura. No clasifica nada.
- **`fuentes/capa3_registro_oferta.csv`**: registro codificado a mano, una fila por actividad (se versiona en git).

| Columna | Descripción |
|---|---|
| `id` | Identificador `C3-###` (se reasigna al reconstruir el registro; no usar como clave estable entre versiones) |
| `distrito`, `ubigeo` | Distrito(s) donde se realiza; varios separados por `;` |
| `ambito` | A quién está abierta: `distrital` (vecinos o colegios del distrito), `metropolitano` (cualquier persona de Lima) o `nacional` (todo el país, aunque la sede esté en Lima Este) |
| `organizador`, `tipo_organizador` | Quién la organiza, y tipo: municipalidad distrital, Municipalidad de Lima / SERPAR, gobierno nacional, alianza público-privada, sociedad civil, privado |
| `nombre` | Nombre de la actividad, programa, evento o espacio |
| `tipo_oferta` | Taller o curso, programa, evento, feria, concurso o competencia, servicio, espacio o infraestructura, convocatoria de voluntariado, beca o premio |
| `tematica` | Uno o más temas separados por `;` (lista cerrada, ver `metodologia_capa3.md`) |
| `publico_declarado`, `edad_min`, `edad_max` | Público y edades tal como los indica la fuente (vacío si no los indica) |
| `incluye_15_29` | `juventud` (dirigida a jóvenes o con rango dentro de 15–29), `adolescentes` (mezcla niños con adolescentes o "jóvenes"; incluye parte del rango 15–29), `todo público`, `no` (fuera del rango) o `no indica` |
| `costo`, `costo_detalle` | `gratuito`, `pagado`, `mixto` o `no indica`, y el monto si se publica |
| `modalidad` | `presencial`, `virtual`, `mixta` o `no indica` |
| `fecha_referencia`, `anio`, `periodo` | Fecha de inicio o de la nota principal, año, y duración o frecuencia |
| `lugar` | Sede(s) |
| `evidencia` | `oferta`, `participación declarada` o `demanda observada` (ver `metodologia_capa3.md`) |
| `cifra_tipo`, `cifra_n`, `cifra_texto`, `cifra_poblacion` | Tipo de cifra (inscritos, asistentes, vacantes, aforo, población beneficiaria estimada...), su valor (límite inferior si dice "más de"), el texto original y a quién se refiere |
| `senal_demanda` | Qué indica demanda y **a qué oferta concreta se refiere** (solo si `evidencia` = `demanda observada`); no es evidencia de interés general |
| `fuente_url`, `fuente_tipo`, `verificacion`, `fecha_consulta` | Enlace(s) separados por ` \| `, tipo de fuente, si se leyó el texto completo o solo el resumen del buscador, y fecha de consulta |
| `notas` | Aclaraciones |

## `data/processed/` — estimaciones de la integración (segunda versión)

Las usan `scripts/integracion_evidencias.py` y `scripts/integracion_construir.py`. Todas las estimaciones de Lima
Este son de dominio no planificado, con `valor`, `ee`, `cv`, `n_muestral` y `precision` (confiable ≤ 15 %,
referencial 15–25 %, no publicable > 25 %). Cuando existen, `personas_encuesta` y `personas_encuesta_ee` son el
total de personas que estima la propia encuesta (promedio anual si se agrupan años).

| Archivo | Script | Contenido |
|---|---|---|
| `integracion_enaho_segmentos.csv` | `integracion_enaho_segmentos.py` | Situación de estudio y trabajo, búsqueda de empleo, informalidad, trabajo independiente, población compatible con la preparación preuniversitaria (con motivos), composición de quienes no estudian ni trabajan, caracterización de las mujeres dedicadas al hogar (`hogar_*` frente a `resto_*`) y desplazamiento para estudiar. Columna `universo`: denominador de cada porcentaje; `equivalente_dato_joven`: sí / no / no aplica. |
| `integracion_enaho_validacion.csv` | ídem | Réplica de las cuatro categorías de "Actividades que realizan los jóvenes" frente a Dato Joven (Lima Metropolitana, 2022–2025, total y por sexo). |
| `integracion_bases_enaho.csv`, `integracion_bases_enapres.csv`, `integracion_bases_enut.csv` | scripts de integración | Población joven expandida por cada encuesta (Lima Este y Lima Metropolitana), con su error estándar. |
| `integracion_seguridad_enapres.csv` | `integracion_seguridad_enapres.py` | Inseguridad nocturna (2022–2025) y actividades evitadas por temor a la delincuencia (2022–2024), por año (Lima Metropolitana) y agrupado. Solo proporciones. |
| `integracion_seguridad_enapres_validacion.csv` | ídem | Réplica frente a Dato Joven. |
| `integracion_tiempo_enut.csv` | `integracion_tiempo_enut.py` | Disponibilidad (≥ 2 horas seguidas sin obligaciones) por bloque horario, horas no comprometidas por día, horas de trabajo doméstico y cuidado y participación semanal en algunas prácticas. `grupo` distingue a las mujeres que no trabajaron ni estudiaron en la semana del diario. |
| `integracion_cultura_edad_enapres.csv` | `integracion_cultura_edad_enapres.py` | Participación cultural por grupo de edad (Lima Este y Lima Metropolitana, 2022–2025), mismas familias que la Capa 2. |
| `integracion_cultura_totales_enapres.csv` | ídem | Personas de 15–29 que realizan cada práctica cultural según la encuesta. |

Las tablas de resultados (`resultados/evidencias.csv`, `fichas_*.csv`, etc.) se describen en
`fuentes/metodologia_integracion.md`. Las fichas citan actividades del registro de la Capa 3 por su `id`: si el
registro se reconstruye, hay que revisar esas referencias (`fichas_convocatoria.csv` guarda también el nombre de
cada actividad para poder comprobarlo).
