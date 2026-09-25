# Exploración técnica de Dato Joven

Fuente principal de la Capa 1: https://observatorio-juventud.minedu.gob.pe/dato-joven/

- **Fecha de la exploración:** 23/09/2026.
- **Objetivo:** determinar qué datos contiene Dato Joven y cómo obtenerlos de forma reproducible para los siete distritos del proyecto.
- **Alcance:** solo exploración. No se desarrolló el scraper definitivo ni se descargaron datos de forma masiva.

## Resumen

1. **Todos los datos de Dato Joven están en tableros de Power BI publicados en la web**: 54 tableros en total. El portal no ofrece CSV ni una API oficial documentada.
2. **La descarga directa en Excel existe, pero sirve poco.** 42 páginas de indicadores tienen un botón "Fuente de datos", pero solo hay 6 archivos distintos y la mayoría de los enlaces apuntan a un archivo que no corresponde al indicador. Los archivos útiles tienen datos agregados por departamento.
3. **Los tableros de Power BI se pueden consultar directamente con peticiones HTTP**, sin iniciar sesión y sin navegador. Es el método recomendado. **No hace falta Selenium.**
4. **Nivel geográfico:**
   - Los **indicadores de encuestas** (ENAHO, EPEN, ENDES, ENAPRES) llegan como máximo a **Lima Metropolitana**, que aparece separada de Lima Región y del Callao. **No bajan a distrito.**
   - La **población joven** y varios **registros administrativos** sí tienen **distrito (UBIGEO)**. Se verificó que devuelven datos para los siete distritos de Lima Este.
5. **Edad:** todas las fuentes llegan como máximo a **29 años**. No hay datos para quienes tienen 30 años. Se aplicará la aproximación de 15 a 29 años prevista en el `README.md`.

El **mapa analítico de la Capa 1** está en la [sección 8](#8-mapa-analítico-de-la-capa-1). Ordena por dimensión todo lo que Dato Joven permite responder.

## Cómo se hizo la exploración

- Se descargó el HTML de las páginas del portal: la portada de Dato Joven, 5 módulos, 9 páginas de categorías de indicadores y 49 páginas de indicadores. Se hizo una petición por segundo.
- Para los 54 tableros de Power BI se pidió solo la **estructura** (tablas, columnas, fecha de actualización), no los datos.
- Se hicieron alrededor de 150 **consultas pequeñas** para listar valores distintos (años, regiones, categorías, rangos de edad) y totales agregados de los siete distritos.
- Se descargaron **6 archivos Excel y 1 PDF de muestra** para ver su estructura. Se guardaron en la carpeta temporal de la sesión, fuera del proyecto, y **se borraron después** porque algunos contienen datos individuales.
- Herramientas: `curl` y Python sin bibliotecas externas. No se agregó código al proyecto.

---

## 1. Módulos de Dato Joven

La portada de Dato Joven tiene 5 módulos. Cada uno lleva a una página con un tablero de Power BI.

| Módulo | Página | Contenido | Nivel geográfico máximo | Años | Filtros | Estado |
|---|---|---|---|---|---|---|
| Política Nacional de Juventud | `/politica-nacional-de-la-juventud/` | Indicadores de los objetivos prioritarios de la política, con valor esperado, valor obtenido y fuente | Nacional (el modelo no tiene columnas geográficas) | Por verificar | Objetivo, indicador, año | Estructura verificada |
| Datos Demográficos | `/dato-joven/datos-demograficos/` | Población joven y población total | **Distrito (UBIGEO)** | **2019–2026** | Rango de edad (15–19, 20–24, 25–29), sexo, año | **Verificado con consulta** |
| Indicadores de Juventud | `/indicadores/` | 8 categorías, 48 tableros de indicadores y un tablero consolidado ("Indicadores regionales") | Lima Metropolitana (encuestas) o distrito (algunos registros) | Varía por indicador | Ver sección 2 | Verificado |
| Organizaciones juveniles (RENOJ) | `/renoj/` | Organizaciones registradas y acreditadas: temática, tipo y año de acreditación | **Distrito (UBIGEO)** | Acreditación 2019–2026 | Temática, tipo, año, rango etario | **Verificado con consulta** |
| Programa de Voluntariado Juvenil | `/programa-de-voluntariado-juvenil/` | Personas inscritas como voluntarias (perfil, experiencia, intereses) y jornadas de movilización | **Distrito (UBIGEO)** para inscritos; región para movilizaciones | Movilizaciones: por verificar. Inscritos: sin columna de año | Edad, sexo, nivel educativo, ocupación | **Verificado con consulta** |

También hay un tablero de **portada** que consolida casi todo (118 tablas). Su última actualización es del 30/06/2026, más antigua que la de los tableros individuales (julio–septiembre de 2026), así que **no conviene usarlo como fuente principal**.

---

## 2. Indicadores de Juventud

La página `/indicadores/` tiene 8 categorías. Cada indicador tiene su propia página con un tablero de Power BI. Hay **48 tableros de indicadores**, de dos tipos.

### 2.1 Indicadores de encuestas (38 tableros)

Todos tienen la misma estructura: una tabla `datosRegionales` y otra `datosNacionales`, con las columnas `AÑO, POBLACION, REGION, CATEGORIA, INDICADOR, VALOR, CV, FUENTE`.

- **Nivel geográfico (verificado):** 25 regiones más "NACIONAL". **"LIMA METROPOLITANA"** aparece separada de "LIMA REGION" y "CALLAO". No hay provincia ni distrito.
- **Categorías para Lima Metropolitana (verificado):** total ("REGIONAL"), hombre, mujer y urbano. Los indicadores de ENDES solo tienen total y urbano. Algunos de ENAHO para 18 a 29 años también muestran rural.
- **Categorías solo a nivel nacional (verificado):** etnia, lengua materna, pobreza, nivel educativo y dominio geográfico (costa, sierra, selva, Lima Metropolitana).
- **CV:** cada valor viene con su coeficiente de variación, que sirve para evaluar la precisión de la estimación.
- **Formato:** los valores vienen como texto (por ejemplo, `"12.5%"`) y hay que convertirlos.

Resultados del barrido de los 38 tableros. La columna "Años disponibles para Lima Metropolitana" está **verificada** en cada tablero.

| Categoría | Indicador | Población | Fuente | Años disponibles para Lima Metropolitana |
|---|---|---|---|---|
| Educación | Años promedio de estudios alcanzados | 15–29 | ENAHO | 2019–2025 |
| Educación | Asistencia a educación superior | 17–24 | ENAHO | 2019–2025 |
| Educación | Conclusión de la educación secundaria | 17–18 | ENAHO | 2019–2025 |
| Educación | Conclusión de la educación superior | 22–24 | ENAHO | 2019–2025 |
| Educación | Nivel educativo alcanzado | 15–29 | ENAHO | 2019–2025 |
| Empleo | Actividades que realizan los jóvenes | 15–29 | ENAHO | 2019–2025 |
| Empleo | Empleo formal | 15–29 | ENAHO / EPEN | 2019–2023 |
| Empleo | Empleo informal | 15–29 | ENAHO / EPEN | 2019–2023 |
| Empleo | Ingreso promedio mensual | 15–29 | ENAHO / EPEN | 2022–2023 |
| Empleo | Jóvenes que no estudian ni trabajan (NINI) | 15–29 | ENAHO | 2019–2025 |
| Empleo | Población económicamente activa (PEA) | 15–29 | ENAHO / EPEN | 2019–2023 |
| Empleo | Tasa de desempleo | 15–29 | ENAHO / EPEN | 2019–2023 |
| Habilidades digitales | Actividades digitales (10 actividades) | 15–29 | ENAHO | 2019–2024 |
| Habilidades digitales | Dispositivo de acceso a internet | 15–29 | ENAHO | 2019–2024 |
| Habilidades digitales | Jóvenes usuarios de internet | 15–29 | ENAHO | 2019–2025 |
| Habilidades digitales | Frecuencia de uso de internet | 15–29 | ENAHO | 2019–2025 |
| Habilidades digitales | Lugar de acceso a internet | 15–29 | ENAHO | 2019–2025 |
| Salud | Consumo de cigarrillos | 15–29 | ENDES | 2019–2024 |
| Salud | Consumo de bebidas alcohólicas | 15–29 | ENDES | 2019–2025 |
| Salud | Embarazo adolescente | 15–19 | ENDES | 2019–2024 |
| Salud | Episodio depresivo | 15–29 | ENDES | 2022–2024 |
| Salud | Con algún seguro de salud | 15–29 | ENAHO | 2019–2025 |
| Salud | Con Seguro Integral de Salud (SIS) | 15–29 | ENAHO | 2019–2025 |
| Salud | Problema de salud crónico | 15–29 | ENAHO | 2019–2025 |
| Participación ciudadana | Participación juvenil en organizaciones | 15–29 | ENAHO | 2019–2025 |
| Participación ciudadana | Principales problemas del país (17 opciones) | 18–29 | ENAHO | 2021–2024 |
| Participación ciudadana | Percepción de la democracia | 18–29 | ENAHO | 2021–2025 |
| Participación ciudadana | Características asociadas a la democracia | 18–29 | ENAHO | 2021–2025 |
| Participación ciudadana | Importancia de la democracia en el Perú | 18–29 | ENAHO | 2021–2025 |
| Participación ciudadana | Funcionamiento de la democracia | 18–29 | ENAHO | 2021–2025 |
| Participación ciudadana | Confianza en las instituciones (21 instituciones) | 18–29 | ENAHO | 2021–2024 |
| Violencia y discriminación | Violencia familiar (física, psicológica y/o sexual) | 15–29 (mujeres) | ENDES | 2021–2025 |
| Violencia y discriminación | Violencia física y/o sexual | 15–29 (mujeres) | ENDES | 2021–2024 |
| Violencia y discriminación | Violencia psicológica | 15–29 | ENDES | 2021–2025 |
| Violencia y discriminación | Percepción de discriminación | 18–29 según la página; 15–29 según el tablero | ENAHO | 2019–2024 |
| Victimización y seguridad | Víctimas de algún hecho delictivo (área urbana) | 15–29 | ENAPRES | 2019–2024 |
| Victimización y seguridad | Percepción de inseguridad en los próximos 12 meses | 15–29 | ENAPRES | 2019–2025 |
| Victimización y seguridad | Inseguridad al caminar solo/a de noche | 15–29 | ENAPRES | 2019–2025 |

**Tablero consolidado "Indicadores regionales"** (`/indicadores-regionales/`): reúne 34 de estos indicadores en un solo modelo, con la misma estructura, más las tablas de población. Se comparó el indicador de desempleo:

- En el tablero individual, Lima Metropolitana tiene el dato **por sexo**.
- En el consolidado, solo tiene el total.

**Conviene extraer de los tableros individuales**, que tienen más detalle. El consolidado sirve para comprobar los resultados.

### 2.2 Tableros de registros administrativos (10 tableros)

Estos tableros tienen **tablas con un registro por persona o por caso**, y varios incluyen distrito.

| Tablero | Nivel geográfico máximo | Años | Edad | Sensibilidad | Estado |
|---|---|---|---|---|---|
| Certificado de nacidos vivos (CNV), madres de 15 a 19 años | **Distrito** (UBIGEO) | 2019–2026 (2026 hasta junio, según la página) | 15–16, 17–18, 19 | Media | **Verificado con consulta** |
| Certificación de discapacidad (MINSA) | **Distrito** (UBIGEO) | 2019–2025 | Grupo de edad | Alta | **Verificado con consulta** |
| CONADIS (Registro Nacional de la Persona con Discapacidad) | **Distrito** (UBIGEO) | 2019–2026 | Edad y rango | Alta | **Verificado con consulta** |
| Víctimas de violencia atendidas en los CEM | **Distrito** (UBIGEO) | 2019–2026 | 15–19, 20–24, 25–29 | **Muy alta** | **Verificado con consulta** |
| VIH / SIDA | Distrito (según el esquema) | Por verificar | Edad y grupo | **Muy alta** | Solo estructura; no se consultó a propósito |
| Trabajadores jóvenes del sector cultural | Departamento | Por verificar | 18–29 | Baja | Solo estructura |
| Registro de atletas del IPD | Sin residencia (solo centro de alto rendimiento) | Por verificar | Edad y grupo | Baja | Solo estructura |
| INPE (población penitenciaria) | Departamento | 2019–2025 (Excel) | 18–19, 20–24, 25–29 | Alta | Estructura y Excel |
| MININTER (detenidos, faltas, accidentes, violencia) | Departamento | 2018/2019–2025 (Excel) | Por verificar | Media | Estructura y Excel |
| Movimiento migratorio | Sin residencia (país, punto de control) | 2019–2025 | 15–29 | Baja | Estructura y Excel |

---

## 3. Formas de obtener los datos

Se evaluaron en el orden pedido: descarga directa, endpoint o API, requests/BeautifulSoup y Selenium.

### 3.1 Descarga directa — útil solo en parte

- **Excel de "Fuente de datos" (verificado):** son enlaces a SharePoint del MINEDU. Agregando `?download=1` al enlace, el archivo se descarga **sin iniciar sesión**.
  - Hay **42 enlaces, pero solo 6 archivos distintos**, y solo 5 páginas enlazan al archivo de su propio indicador.
  - **29 páginas enlazan al Excel del RENOJ** en lugar de al de su indicador. Parece un error en la plantilla del sitio. Otras 7 páginas de encuestas enlazan al archivo de MININTER, y la página del CNV enlaza al de discapacidad.
  - Los archivos correctos (discapacidad, CONADIS, MININTER, INPE, migración) tienen **totales por departamento y año**, no por distrito.
  - **Conclusión:** no sirven para los indicadores de encuestas ni para el nivel distrital. Pueden servir para comprobar resultados.
- **"Exportar PDF" (verificado):** solo abre la ventana de impresión del navegador (`window.print()`). No contiene datos.
- **"Manual" (verificado):** hay 24 PDF distintos, descargables sin iniciar sesión. Parecen ser fichas metodológicas; **su contenido no se revisó**.

### 3.2 Endpoints de Power BI — método recomendado

Cada tablero es un reporte de Power BI "publicado en la web". El visor obtiene los datos de endpoints públicos que responden sin autenticación. **Se verificó que funcionan con simples peticiones HTTP**. El detalle técnico está en el [Anexo](#anexo-flujo-técnico-de-consulta-a-power-bi).

- **Ventajas:** reproducible, sin navegador, devuelve JSON y permite pedir exactamente los filtros necesarios (distrito, año, sexo, edad). También informa la fecha de la última actualización de cada tablero.
- **Riesgos:**
  - Son endpoints **internos de Microsoft, no documentados**, y pueden cambiar sin aviso.
  - La respuesta viene en un formato comprimido que hay que decodificar.
  - Los valores pueden venir como texto (`"12.5%"`, `"479L"`).
  - Hay un límite de filas por consulta: en tablas grandes habrá que consultar por partes.

### 3.3 requests / BeautifulSoup — solo para el catálogo

El HTML del portal (WordPress con Elementor) no contiene datos. Sí contiene los **enlaces a los tableros**, con la clave pública de cada reporte, y las descripciones de los indicadores. Sirve para armar y actualizar el **catálogo de tableros** de forma automática antes de consultar los endpoints.

### 3.4 Selenium — no necesario

Ningún módulo lo requiere: todos los tableros respondieron a las consultas directas. Solo sería una alternativa de respaldo si Microsoft cambiara los endpoints.

---

## 4. Qué se puede obtener para los siete distritos

Códigos UBIGEO confirmados en el propio tablero: Ate `150103`, Chaclacayo `150107`, El Agustino `150111`, La Molina `150114`, Lurigancho `150118`, San Juan de Lurigancho `150132` y Santa Anita `150137`.

| Dato | Tablero | Detalle disponible | Estado |
|---|---|---|---|
| Población joven | Datos Demográficos | Distrito × rango de edad (15–19, 20–24, 25–29) × sexo × año (2019–2026) | **Verificado.** Ejemplo: Santa Anita 2026 devuelve 6 valores (3 rangos × 2 sexos). |
| Población total | Datos Demográficos | Distrito × sexo × año | **Verificado** |
| Organizaciones juveniles | RENOJ | Distrito × temática × tipo × año de acreditación | **Verificado.** Total acumulado: Ate 30, Chaclacayo 3, El Agustino 12, La Molina 47, Lurigancho 12, San Juan de Lurigancho 60, Santa Anita 18. |
| Personas voluntarias inscritas | Voluntariado | Distrito × edad × sexo × intereses de voluntariado × experiencia | **Verificado:** devuelve totales para los 7 distritos |
| Nacimientos de madres de 15 a 19 años | CNV | Distrito × año × edad de la madre | **Verificado:** devuelve totales para los 7 distritos |
| Casos de violencia atendidos en los CEM | CEM | Distrito × año × grupo de edad × sexo × tipo de violencia | **Verificado:** devuelve totales para los 7 distritos |
| Certificación de discapacidad y registro CONADIS | Discapacidad / CONADIS | Distrito × año × edad | **Verificado:** devuelve totales para los 7 distritos |
| Educación, empleo, salud, internet, participación, seguridad | Indicadores de encuestas | **Solo Lima Metropolitana**, que agrupa 43 distritos | Verificado. **No representa a Lima Este.** |

Los totales de la tabla sirven solo para comprobar el acceso; no son datos finales. No se publican cifras de los registros sensibles.

---

## 5. Propuesta de extracción para la Capa 1

Esta sección define **qué** extraer y con qué reglas. El **orden** de extracción está en la [sección 8.18](#818-orden-de-extracción-propuesto).

### Datos distritales básicos

| # | Dato | Tablero | Detalle | Uso en el proyecto |
|---|---|---|---|---|
| 1 | Población joven | Datos Demográficos | 7 distritos × 3 rangos de edad × sexo × 2019–2026 | Tamaño de la población objetivo y denominador para calcular tasas |
| 2 | Población total | Datos Demográficos | 7 distritos × sexo × 2019–2026 | Porcentaje de jóvenes por distrito |
| 3 | Organizaciones juveniles | RENOJ, tabla `Representantes` | Conteo por distrito × temática × tipo × año. **No se extrae la tabla `Miembros`.** | Participación y tejido organizativo; también alimenta la Capa 3 |
| 4 | Voluntariado | Voluntariado, tabla `fact_Voluntarios` | Conteo por distrito × rango de edad × sexo, y por cada campo `INTERES_VOLUNTARIADO_*` | Participación, e **intereses declarados** que conectan con la Capa 2 |
| 5 | Maternidad adolescente | CNV | Conteo por distrito × año × rango de edad (15–16, 17–18, 19) | Aproximación al embarazo adolescente por distrito |

### Registros sensibles, solo agregados

| # | Dato | Tablero | Detalle | Condición |
|---|---|---|---|---|
| 6 | Violencia atendida en los CEM | CEM | Conteo por distrito × año × grupo de edad × sexo × tipo de violencia | Solo conteos, sin datos individuales. Ocultar celdas pequeñas. |
| 7 | Discapacidad | Certificación de discapacidad y CONADIS | Conteo por distrito × año × grupo de edad | Igual que la anterior |

### Contexto de Lima Metropolitana

| # | Dato | Tablero | Detalle | Uso |
|---|---|---|---|---|
| 8 | Los 38 indicadores de encuestas | Tableros individuales, tabla `datosRegionales` | Regiones "LIMA METROPOLITANA" y "NACIONAL" × categoría × año, **incluido el CV** | Contexto. Siempre etiquetado como "Lima Metropolitana", nunca como "Lima Este". |

### Qué no se extrae

- **VIH / SIDA:** es muy sensible, con conteos distritales pequeños que podrían permitir identificar a personas, y aporta poco al diseño de actividades.
- **INPE y MININTER:** solo tienen nivel departamental.
- **IPD y migración:** no tienen distrito de residencia.
- **Sector cultural:** solo tiene nivel departamental. Queda como contexto opcional.
- **Tablas con un registro por persona** de cualquier tablero: RENOJ `Miembros`, CEM, CONADIS, CNV, voluntarios y otras.

### Reglas para la extracción

- **Solo consultas agregadas** (conteos o sumas por grupo). Nunca se descargan registros individuales.
- **Ocultar las celdas pequeñas** de los registros sensibles. Propuesta: menos de 10 casos. El umbral está por decidir.
- **Guardar el CV** de los indicadores de encuestas y marcar las estimaciones poco precisas. El umbral habitual del INEI está por confirmar en los manuales.
- **Guardar metadatos** con cada archivo: tablero, clave del reporte, tabla, filtros, fecha de extracción y fecha de última actualización del tablero.
- **Formato de salida propuesto:** CSV en formato largo (una fila por combinación de filtros) en `data/raw/dato_joven/`, que no se sube al repositorio.
- **Ritmo:** como máximo una consulta por segundo.

---

## 6. Verificado, supuestos y pendientes

### Verificado

- Los 5 módulos y sus 54 tableros de Power BI, con fecha de última actualización entre junio y septiembre de 2026.
- La estructura (tablas y columnas) de los 54 tableros.
- Los endpoints públicos de Power BI responden sin autenticación y devuelven datos.
- Los códigos UBIGEO de los 7 distritos.
- La disponibilidad de datos distritales en Datos Demográficos, RENOJ, Voluntariado, CNV, CEM, Certificación de discapacidad y CONADIS.
- Los años, las categorías y las fuentes de los 38 indicadores de encuestas para Lima Metropolitana.
- Que Lima Metropolitana está separada de Lima Región y del Callao.
- Los rangos de edad de Datos Demográficos: 15–19, 20–24 y 25–29. No hay datos para 30 años.
- Los enlaces de Excel descargables y los enlaces cruzados; que "Exportar PDF" es solo `window.print()`.

### Supuestos o pendientes de verificar

- **Fuente de las estimaciones de población:** resuelto. Es el Repositorio Único Nacional de Información en Salud (REUNIS) y las proyecciones de población del INEI; ver `metodologia_capa1.md` (D5) sobre la inestabilidad de sus series por edad.
- **Qué significa el distrito** en cada registro:
  - CNV: probablemente es la residencia de la madre, porque hay columnas aparte para el establecimiento de salud. Por verificar.
  - CEM: no está claro si `ubigeo` es el domicilio de la víctima o la ubicación del CEM.
  - Voluntariado: probablemente es la residencia. Por verificar.
- **Años** del RENOJ (solo se verificó el año de acreditación), de las movilizaciones del voluntariado, de VIH, del IPD y del sector cultural.
- **Contenido de los 24 manuales PDF:** definiciones, metodología y umbral de CV.
- **Límite de filas por consulta** en tablas grandes y cómo consultarlas por partes.
- **Condiciones de uso:** el portal no indica condiciones para reutilizar los datos. Se sugiere confirmar con el Observatorio (senaju_onajuv@minedu.gob.pe) o solicitar los datos formalmente. Así el proyecto no dependería de endpoints no documentados.
- **Coherencia entre tableros:** el consolidado tiene menos detalle que los individuales. No se comparó indicador por indicador.

---

## 7. Observaciones sobre la fuente

- **Enlaces de "Fuente de datos" incorrectos:** 37 de 42 páginas enlazan a un Excel de otro indicador. Conviene tenerlo en cuenta y no citar esos archivos como fuente de esos indicadores.
- **Datos personales expuestos:** el Excel del RENOJ, enlazado en 29 páginas, incluye una hoja `Miembros` con **fecha de nacimiento, edad, sexo, cargo y organización** de más de 25 000 integrantes. El Excel del INPE incluye registros individuales de personas liberadas. Varios modelos de Power BI también contienen tablas individuales con datos sensibles (VIH, CEM, discapacidad, voluntarios). **El proyecto no usará ni guardará esos datos individuales.** Se podría informar de esto al Observatorio.
- **Edad:** ninguna fuente de Dato Joven incluye a personas de 30 años.

---

## 8. Mapa analítico de la Capa 1

Este mapa ordena, por dimensión, lo que Dato Joven permite responder sobre el contexto, las características y las necesidades de las juventudes. Se construyó **solo con lo ya verificado** en esta exploración; no se hizo ninguna extracción nueva.

**Cómo leer las tablas**

- **Periodo prioritario: 2022–2026.** En `años_disponibles` se indican los años exactos de ese periodo y, entre paréntesis, desde cuándo empieza la serie.
- **Años de las encuestas:** son los verificados para Lima Metropolitana. A nivel nacional pueden variar en un año; solo se verificaron en 5 indicadores.
- **Nivel geográfico:**
  - **Distrito:** puede usarse como evidencia específica de los siete distritos de Lima Este.
  - **Lima Metropolitana:** contexto metropolitano (43 distritos). **No se atribuye a Lima Este.**
  - **Departamento / Nacional:** contexto general. **No se atribuye a Lima Este.**
  - **Sin territorio de residencia:** el dato no indica dónde viven las personas.
- **Categorías de las encuestas en Lima Metropolitana:** total, hombre, mujer y urbano. Las excepciones se indican en cada fila. Cada valor viene con su coeficiente de variación (CV).
- **"Por verificar"** significa que el dato existe en los tableros, pero falta confirmar su contenido.
- **Edad:** ninguna fuente incluye a personas de 30 años.

### 8.1 Demografía

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Demografía | ¿Cuántos jóvenes viven en cada uno de los siete distritos y cómo cambió esa cifra entre 2022 y 2026? | Población joven por distrito, sexo y grupo de edad | Estimaciones de población (fuente por verificar) | 2022–2026 (desde 2019) | 15–19, 20–24, 25–29 | **Distrito** | Dimensiona la población objetivo de cada distrito. Es el denominador para calcular tasas en otras dimensiones. | No incluye 30 años. El método de estimación está por verificar. |
| Demografía | ¿Qué peso tienen los jóvenes en la población total de cada distrito? | Población total por distrito y sexo, junto con la población joven | Estimaciones de población (fuente por verificar) | 2022–2026 (desde 2019) | Todas las edades | **Distrito** | Permite comparar distritos según la proporción de jóvenes. | Igual que la fila anterior. |
| Demografía | ¿Cómo se reparte la población joven por sexo y grupo de edad en cada distrito? | Población joven por distrito, sexo y grupo de edad | Estimaciones de población (fuente por verificar) | 2022–2026 (desde 2019) | 15–19, 20–24, 25–29 | **Distrito** | Distingue adolescentes (15–19) de jóvenes adultos (20–29), que suelen tener necesidades distintas. | Solo tres grupos de edad. |

### 8.2 Educación

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Educación | ¿Cuántos años de estudio alcanzan en promedio los jóvenes y cómo evolucionó entre 2022 y 2025? | Años promedio de estudios alcanzados | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Contexto del nivel educativo juvenil y su evolución. | No hay dato distrital. Es una estimación de encuesta (revisar CV). |
| Educación | ¿Qué nivel educativo alcanzan los jóvenes y hay diferencias entre hombres y mujeres? | Nivel educativo alcanzado (4 categorías) | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Muestra la distribución por nivel educativo y las brechas de género. | No hay dato distrital. |
| Educación | ¿Qué proporción de jóvenes accede a la educación superior? | Asistencia a educación superior (2 indicadores) | ENAHO | 2022–2025 (desde 2019) | 17–24 | Lima Metropolitana | Acceso a estudios superiores. | Rango de edad parcial. No hay dato distrital. |
| Educación | ¿Qué proporción termina la secundaria a la edad esperada? | Conclusión de la educación secundaria | ENAHO | 2022–2025 (desde 2019) | 17–18 | Lima Metropolitana | Rezago o abandono escolar. | Solo cubre a quienes tienen 17 o 18 años. |
| Educación | ¿Qué proporción concluye la educación superior? | Conclusión de la educación superior | ENAHO | 2022–2025 (desde 2019) | 22–24 | Lima Metropolitana | Culminación de estudios superiores. | Solo cubre a quienes tienen de 22 a 24 años. |
| Educación | ¿Hay algún indicador educativo por distrito? | **No hay un indicador educativo representativo por distrito.** Solo existe el nivel educativo de algunos subgrupos: madres adolescentes (CNV), personas con discapacidad (CONADIS), víctimas atendidas en los CEM y personas voluntarias. | — | — | — | Distrito (solo subgrupos) | Podría describir a esos subgrupos específicos. | No describe a la juventud del distrito. |

### 8.3 Empleo y situación laboral

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Empleo | ¿Cómo evolucionó el desempleo juvenil entre 2022 y 2023, y hay brecha entre hombres y mujeres? | Tasa de desempleo | ENAHO / EPEN | 2022–2023 (desde 2019) | 15–29 | Lima Metropolitana | Dificultad para conseguir empleo. | En Lima Metropolitana no hay datos de 2024 ni 2025. Falta confirmar qué año viene de cada encuesta. |
| Empleo | ¿Qué proporción de jóvenes trabaja o busca trabajo? | Población económicamente activa (PEA) | ENAHO / EPEN | 2022–2023 (desde 2019) | 15–29 | Lima Metropolitana | Inserción en el mercado laboral. | Igual que la fila anterior. |
| Empleo | ¿Qué proporción de los empleos juveniles son formales o informales? | Empleo formal; empleo informal | ENAHO / EPEN | 2022–2023 (desde 2019) | 15–29 | Lima Metropolitana | Calidad del empleo. | Igual que la fila anterior. |
| Empleo | ¿Cuánto ganan en promedio los jóvenes que trabajan? | Ingreso promedio mensual | ENAHO / EPEN | **Solo 2022 y 2023** | 15–29 | Lima Metropolitana | Nivel de ingresos. | Serie muy corta. |
| Empleo | ¿A qué se dedican los jóvenes (estudiar, trabajar, otras situaciones) y cómo cambió entre 2022 y 2025? | Actividades que realizan los jóvenes (4 categorías) | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Combina estudio y trabajo en una sola lectura. | Faltan confirmar los nombres de las 4 categorías. |
| Empleo | ¿Hay algún indicador laboral por distrito? | **No hay un indicador laboral representativo por distrito.** Solo existe la ocupación de las personas voluntarias y si trabajan las víctimas atendidas en los CEM. | — | — | — | Distrito (solo subgrupos) | — | No describe a la juventud del distrito. |

### 8.4 Jóvenes que no estudian ni trabajan

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| No estudian ni trabajan | ¿Qué proporción de jóvenes no estudia ni trabaja, cómo evolucionó entre 2022 y 2025 y hay diferencias entre hombres y mujeres? | Jóvenes que no estudian ni trabajan (NINI) | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Identifica a la población desconectada de la educación y el empleo. | No hay dato distrital. |

### 8.5 Salud

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Salud | ¿Qué proporción de jóvenes tiene seguro de salud, y cuántos dependen del SIS? | Con algún seguro de salud; con Seguro Integral de Salud (SIS) | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Acceso a servicios de salud. | No hay dato distrital. |
| Salud | ¿Qué proporción de jóvenes tiene algún problema de salud crónico? | Problema de salud crónico | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Carga de enfermedad crónica. | No hay dato distrital. |
| Salud mental | ¿Qué proporción de jóvenes tuvo un episodio depresivo en los últimos 12 meses? | Episodio depresivo | ENDES | 2022–2024 (el nacional llega a 2025) | 15–29 | Lima Metropolitana | Único indicador de salud mental en las encuestas. | Serie corta. No hay dato distrital. |
| Salud | ¿Qué proporción de jóvenes consume alcohol o tabaco? | Consumo de bebidas alcohólicas; consumo de cigarrillos | ENDES | Alcohol: 2022–2025. Cigarrillos: 2022–2024 (ambos desde 2019). | 15–29 | Lima Metropolitana | Conductas de riesgo. | No hay dato distrital. |
| Salud sexual y reproductiva | ¿Cuántos nacimientos de madres de 15 a 19 años hay en cada distrito y cuál es la tasa respecto a las mujeres de esa edad? | Nacidos vivos de madres de 15 a 19 años | Registro de certificados de nacido vivo (entidad por verificar) | 2022–2026; 2026 solo hasta junio (desde 2019) | Madres de 15–16, 17–18 y 19 | **Distrito** | Evidencia distrital de maternidad adolescente. La tasa usa como denominador la población de la sección 8.1. | Mide nacimientos, no embarazos. Falta confirmar si el distrito es el de residencia de la madre. |
| Salud sexual y reproductiva | ¿Qué proporción de adolescentes es madre o está embarazada? | Embarazo adolescente | ENDES | 2022–2024 (desde 2019) | 15–19 | Lima Metropolitana (solo total y urbano) | Contraste metropolitano para el dato distrital anterior. | No hay desagregación por sexo, porque el indicador es solo de mujeres. |
| Discapacidad | ¿Cuántos jóvenes con discapacidad certificada o registrada hay en cada distrito? | Certificación de discapacidad; inscripción en el registro del CONADIS | MINSA; CONADIS | Certificación: 2022–2025. CONADIS: 2022–2026 (ambos desde 2019). | 15–29 (valores de los grupos por verificar) | **Distrito** | Inclusión y accesibilidad. | Son registros administrativos, no prevalencia. Son sensibles: solo agregados, ocultando celdas pequeñas. |
| Salud | VIH / SIDA | Existe en los tableros, con distrito. | — | Por verificar | 15–29 | Distrito | — | **Excluido** por su sensibilidad y por su poca utilidad para el diseño de actividades. |

### 8.6 Internet y competencias digitales

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Internet | ¿Qué proporción de jóvenes usa internet y con qué frecuencia? | Jóvenes usuarios de internet; frecuencia de uso (3 categorías) | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Nivel de conectividad. | No hay dato distrital. |
| Internet | ¿Desde dónde y con qué dispositivo se conectan los jóvenes? | Lugar de acceso (7 categorías); dispositivo de acceso (6 categorías) | ENAHO | Lugar: 2022–2025. Dispositivo: 2022–2024 (ambos desde 2019). | 15–29 | Lima Metropolitana | Condiciones de acceso, por ejemplo si dependen solo del celular. | No hay dato distrital. |
| Competencias digitales | ¿Qué habilidades digitales tienen los jóvenes y cuáles son las menos frecuentes? | Actividades digitales (10 actividades: por ejemplo, usar fórmulas en hojas de cálculo, crear presentaciones, programar, instalar software) | ENAHO | 2022–2024 (desde 2019) | 15–29 | Lima Metropolitana | Identifica brechas de habilidades digitales concretas. | En Lima Metropolitana no hay dato de 2025. No hay dato distrital. |

### 8.7 Seguridad y victimización

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Victimización | ¿Qué proporción de jóvenes fue víctima de algún delito y cómo evolucionó? | Jóvenes víctimas de algún hecho delictivo | ENAPRES | 2022–2024 (desde 2019) | 15–29 (área urbana) | Lima Metropolitana (total, hombre y mujer) | Exposición al delito. | No hay dato distrital. |
| Percepción de inseguridad | ¿Cuánta inseguridad perciben los jóvenes en general y al caminar solos de noche por su barrio? | Percepción de inseguridad en los próximos 12 meses; inseguridad al caminar solo/a de noche | ENAPRES | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana (total, hombre y mujer) | Percepción de seguridad en el espacio público. | No hay dato distrital. |
| Seguridad | ¿Qué actividades dejan de hacer los jóvenes por miedo a la inseguridad? ¿Cuántos son víctimas más de una vez? | Tablas "Actividad que dejó de realizar" y "Revictimización" | Por verificar | Por verificar | Por verificar | Por verificar | Podría mostrar cómo la inseguridad limita el uso del tiempo y del espacio. | Solo aparecen en el tablero consolidado. Falta verificar su contenido. |
| Seguridad | ¿Cuántos jóvenes son detenidos o intervenidos por la policía? | Detenidos por delitos; intervenidos por faltas | MININTER | 2022–2025 (desde 2018/2019). En el Excel, la hoja de detenidos no tiene 2022. | 18–29 | Departamento | Contexto general. | No hay distrito. "Lima" incluye más que Lima Este. |
| Seguridad | ¿Cuántos jóvenes están privados de libertad? | Población penitenciaria | INPE | 2022–2025 (desde 2019) | 18–29 | Departamento | Contexto general. | No hay distrito de residencia. |

### 8.8 Violencia y discriminación

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Violencia | ¿Cuántos casos de violencia contra jóvenes atienden los CEM en cada distrito, de qué tipo, con qué vínculo con el agresor y a quién afectan? | Casos atendidos en los Centros Emergencia Mujer y Familia | Registros de los CEM | 2022–2026 (desde 2019). Falta confirmar si 2026 es parcial. | 15–19, 20–24, 25–29 | **Distrito** | Evidencia distrital sobre violencia. | Cuenta casos atendidos, no cuánta violencia hay. Falta confirmar si el distrito es el de residencia o el del CEM. Es sensible: solo agregados. |
| Violencia | ¿Qué proporción de mujeres jóvenes sufrió violencia de su pareja? | Violencia familiar (física, psicológica y/o sexual); violencia física y/o sexual | ENDES | Familiar: 2022–2025. Física/sexual: 2022–2024 (ambos desde 2021). | Mujeres 15–29 | Lima Metropolitana (solo total y urbano) | Prevalencia de la violencia de pareja. | Solo mujeres. No hay dato distrital. |
| Violencia | ¿Qué proporción de jóvenes sufrió violencia psicológica de su pareja? | Violencia psicológica | ENDES | 2022–2025 (desde 2021) | 15–29 | Lima Metropolitana (solo total y urbano) | Prevalencia de la violencia psicológica. | No hay dato distrital. |
| Discriminación | ¿Qué proporción de jóvenes se sintió discriminada en el último año? | Percepción de discriminación | ENAHO | 2022–2024 (desde 2019) | 15–29 según el tablero; 18–29 según la página | Lima Metropolitana (también rural) | Exclusión percibida. | El rango de edad es inconsistente entre la página y el tablero. No hay dato distrital. |
| Violencia | ¿Cuántos jóvenes sufrieron alguna vez violencia física, o violencia física, sexual o psicológica? | Tablas "Física alguna vez" y "Física, sexual o psicológica alguna vez" | Por verificar | Por verificar | Por verificar | Por verificar | Complementaría los indicadores anteriores. | Solo aparecen en el tablero consolidado. |

### 8.9 Participación ciudadana

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Participación | ¿Qué proporción de jóvenes participa en alguna organización y cómo evolucionó entre 2022 y 2025? | Participación juvenil en organizaciones | ENAHO | 2022–2025 (desde 2019) | 15–29 | Lima Metropolitana | Nivel de participación organizada. | No hay dato distrital. No indica el tipo de organización. |
| Percepciones | ¿Cuáles consideran los jóvenes los principales problemas del país? | Principales problemas del país (17 opciones) | ENAHO | 2022–2024 (desde 2021) | 18–29 | Lima Metropolitana (también rural) | Muestra qué problemas priorizan los jóvenes. | Se refiere a problemas del país, no del barrio ni del distrito. |
| Ciudadanía | ¿Cómo valoran los jóvenes la democracia? | Percepción de la democracia; importancia de la democracia; funcionamiento de la democracia; características asociadas (8) | ENAHO | 2022–2025 (desde 2021) | 18–29 | Lima Metropolitana (también rural) | Actitudes cívicas. | Relación indirecta con el diseño de actividades. |
| Ciudadanía | ¿Cuánto confían los jóvenes en las instituciones? | Confianza en las instituciones (21 instituciones) | ENAHO | 2022–2024 (desde 2021) | 18–29 | Lima Metropolitana (también rural) | Confianza institucional, relevante si las actividades involucran a instituciones públicas. | No hay dato de 2025. |
| Ciudadanía | ¿Conocen los jóvenes la democracia y la prefieren siempre? | Tablas "Conoce democracia" y "Democracia siempre preferible" | Por verificar | Por verificar | Por verificar | Por verificar | — | Solo aparecen en el tablero consolidado. |

### 8.10 Organizaciones juveniles

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Organizaciones juveniles | ¿Cuántas organizaciones juveniles acreditadas hay en cada distrito y cuántas se acreditaron entre 2022 y 2026? | Organizaciones registradas en el RENOJ, por distrito y año de acreditación | RENOJ | Acreditaciones 2022–2026 (desde 2019) | No aplica (son organizaciones) | **Distrito** | Mide el tejido organizativo juvenil. Identifica posibles organizaciones aliadas y se cruza con la Capa 3. | Solo incluye organizaciones registradas. El total es acumulado y no indica si siguen activas. |
| Organizaciones juveniles | ¿En qué temáticas y tipos de organización se concentran en cada distrito? | Temática 1 y 2; tipo y detalle de tipo. Algunos valores vistos: "Cultura y arte", "Deporte y recreación", "Educación y desarrollo", "Inclusión y derechos", "Ambiente y sostenibilidad". | RENOJ | Igual que la fila anterior | No aplica | **Distrito** | Muestra en qué temas se organizan los jóvenes; es una señal de interés organizado. | La lista completa de temáticas está por verificar. Los datos de los miembros (edad, sexo) son individuales y no se extraen. |

### 8.11 Voluntariado e intereses declarados

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Voluntariado | ¿Cuántos jóvenes de cada distrito están inscritos en el Programa de Voluntariado Juvenil? | Personas voluntarias inscritas por distrito | Programa de Voluntariado Juvenil (SENAJU) | **Sin año** (la tabla de inscritos no tiene columna de año) | Edad y rango de edad (valores por verificar) | **Distrito** | Mide la disposición a participar. | Las personas se inscriben por decisión propia: no representan a la juventud del distrito. Algunos distritos tienen pocos inscritos. Falta confirmar si el distrito es el de residencia. |
| Intereses declarados | ¿En qué temáticas declaran interés las personas voluntarias de cada distrito? | 6 intereses: educación integral; salud mental y bienestar; participación ciudadana; educación para la empleabilidad; poblaciones en situación de vulnerabilidad; participación juvenil mediante el deporte, el arte y la cultura | Programa de Voluntariado Juvenil | Sin año | Por verificar | **Distrito** | Es el único dato de Dato Joven sobre **intereses declarados**; conecta con la Capa 2. | Solo representa a las personas voluntarias. Las categorías son las del programa, no una pregunta abierta. |
| Experiencia previa | ¿En qué temáticas tienen experiencia de voluntariado? | 9 temáticas: cultura, ciencia, economía, educación, medio ambiente, democracia, deporte, salud y otra | Programa de Voluntariado Juvenil | Sin año | Por verificar | **Distrito** | Indica en qué temas ya hay trayectoria de participación. | Igual que la fila anterior. |
| Perfil | ¿Qué perfil tienen las personas voluntarias: nivel educativo, ocupación, área de estudio y participación en organizaciones o consejos de juventud? | Campos de perfil del registro de inscritos | Programa de Voluntariado Juvenil | Sin año | Por verificar | **Distrito** | Caracteriza a los jóvenes que ya participan. | El registro también tiene campos sensibles (salud, discapacidad, comunidad LGTBIQ+) que **no se extraen**. |
| Movilización | ¿Cuántas personas voluntarias se movilizan y en qué tipo de actividades? | Jornadas de movilización | Programa de Voluntariado Juvenil | Por verificar | No aplica | Región | Contexto del funcionamiento del programa. | No tiene distrito. |

### 8.12 Migración

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Migración | ¿Cuántos jóvenes entran y salen del país y por qué motivos? | Movimiento migratorio de jóvenes | Registros de control migratorio (entidad por verificar) | 2022–2025 (desde 2019) | 15–29 | Nacional, sin territorio de residencia (país y punto de control) | Contexto general. | No se puede atribuir a Lima Este. |
| Migración | ¿Cuántos jóvenes migrantes viven en el territorio? | Tabla "Población inmigrante" | Por verificar | Por verificar | Por verificar | Por verificar | Sería relevante si tuviera distrito. | Solo aparece en el tablero de portada. Falta verificar su contenido. |
| Migración | ¿Hay datos de migración interna o de jóvenes migrantes por distrito? | **No hay información disponible** en lo explorado. | — | — | — | — | — | — |

### 8.13 Cultura y deporte

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Cultura | ¿Cuántos jóvenes trabajan en el sector cultural y en qué subsectores? | Trabajadores jóvenes del sector cultural | Registros del sector cultural (entidad por verificar) | Por verificar | 18–29 | Departamento | Contexto del empleo cultural. | No hay distrito. Mide empleo, no participación cultural. |
| Deporte | ¿Cuántos jóvenes son atletas registrados en el IPD y en qué disciplinas? | Registro de atletas del IPD | IPD | Por verificar | 15–29 | Sin territorio de residencia (centro de alto rendimiento) | Contexto del deporte de alto rendimiento. | No refleja la práctica deportiva general. |
| Cultura y deporte | ¿Hay intereses, experiencia u organizaciones vinculadas a la cultura y el deporte en cada distrito? | Interés en "participación juvenil mediante el deporte, el arte y la cultura" y experiencia en cultura o deporte (voluntariado); organizaciones con temáticas de cultura, arte, deporte y recreación (RENOJ) | Voluntariado; RENOJ | Ver secciones 8.10 y 8.11 | Ver secciones 8.10 y 8.11 | **Distrito** | Única evidencia distrital relacionada con cultura y deporte. | Solo representa a personas voluntarias y organizaciones registradas. |
| Cultura y deporte | ¿Qué proporción de jóvenes practica deporte o participa en actividades culturales? | **No hay información disponible** en Dato Joven. | — | — | — | — | — | Habrá que buscarla en la Capa 2 o en otras fuentes. |

### 8.14 Otras dimensiones

| dimension | pregunta_analitica | indicador_disponible | fuente_original | años_disponibles | rango_edad | nivel_geografico | utilidad_para_el_proyecto | limitaciones |
|---|---|---|---|---|---|---|---|---|
| Política pública | ¿Cómo avanzan los indicadores de la Política Nacional de Juventud respecto de sus metas? | Valor esperado y valor obtenido por indicador y objetivo prioritario | Varias (campo "Fuente" del tablero) | Por verificar | Por verificar | Nacional | Marco de política con el que alinear el diagnóstico. | No es territorial. |
| Pobreza y diversidad | ¿Hay brechas por pobreza, etnia o lengua materna? | Desagregaciones de los indicadores de encuestas: pobre / no pobre, etnia, lengua materna, nivel educativo | ENAHO, ENDES, ENAPRES | Según el indicador | Según el indicador | **Solo nacional** | Muestra brechas estructurales. | No existen para Lima Metropolitana ni por distrito. |
| Justicia juvenil | ¿Cuántos adolescentes y jóvenes están en centros juveniles? | Tabla "PRONACEJ" | Por verificar | Por verificar | Por verificar | Por verificar | — | Solo aparece en el tablero de portada. |
| Emprendimiento | ¿Qué proporción de jóvenes emprende? | **No hay indicador en Dato Joven.** Biblio Joven tiene una categoría "Empleo y emprendimiento" con documentos, no con indicadores. | — | — | — | — | — | Habrá que buscarlo en la Capa 2 o en otras fuentes. |
| Uso del tiempo | ¿Cómo distribuyen los jóvenes su tiempo, incluido el trabajo no remunerado? | **No hay indicador en los tableros.** Existe el documento *Juventud y trabajo no remunerado 2024* en Biblio Joven. | — | — | — | Nacional (documento) | — | Solo documental. |

### 8.15 Resumen por nivel geográfico

| Dimensión | Evidencia por distrito | Contexto de Lima Metropolitana | Solo departamento o nacional | Sin información |
|---|---|---|---|---|
| Demografía | Población joven y total | — | — | — |
| Educación | Solo subgrupos | 5 indicadores | — | Indicador distrital |
| Empleo | Solo subgrupos | 6 indicadores | Sector cultural | Indicador distrital; datos de 2024–2025 |
| No estudian ni trabajan | — | NINI | — | Indicador distrital |
| Salud | Maternidad adolescente; discapacidad | 7 indicadores | — | Salud mental por distrito |
| Internet y competencias digitales | — | 5 indicadores | — | Indicador distrital |
| Seguridad y victimización | — | 3 indicadores | MININTER; INPE | Indicador distrital |
| Violencia y discriminación | Casos atendidos en los CEM | 4 indicadores | — | — |
| Participación ciudadana | — | 7 indicadores | — | Indicador distrital |
| Organizaciones juveniles | RENOJ | — | — | — |
| Voluntariado e intereses | Inscritos, intereses y experiencia | — | Movilizaciones (región) | Intereses de la juventud en general |
| Migración | — | — | Movimiento migratorio | Migración por distrito |
| Cultura y deporte | Intereses de voluntariado; temáticas del RENOJ | — | Sector cultural; IPD | Práctica deportiva y participación cultural |
| Emprendimiento | — | — | — | Sin indicador |

### 8.16 Evidencia que podría servir para decidir actividades

Esta tabla **no propone actividades**. Solo indica qué evidencia de la Capa 1 podría usarse después, al cruzarla con la Capa 2 (intereses) y la Capa 3 (oferta).

| Ámbito de decisión | Evidencia de la Capa 1 | Nivel | Posible cruce con otras capas |
|---|---|---|---|
| Educación y capacitación | Nivel educativo, asistencia y conclusión de secundaria y superior | Lima Metropolitana | Intereses educativos (Capa 2); becas y talleres (Capa 3) |
| Empleo y empleabilidad | Desempleo, informalidad, ingresos, NINI; interés en "educación para la empleabilidad" | Lima Metropolitana; distrito (solo voluntariado) | Aspiraciones laborales (Capa 2); en la Capa 3 hasta ahora no hay oferta de empleo |
| Competencias digitales | Uso de internet, dispositivos, 10 habilidades digitales | Lima Metropolitana | Uso digital (Capa 2); talleres de computación (Capa 3) |
| Participación y organización | Participación en organizaciones; RENOJ; voluntariado | Distrito y Lima Metropolitana | Eventos como FestiJoven (Capa 3) |
| Cultura | Temáticas del RENOJ; intereses y experiencia de voluntariado | Distrito | Intereses culturales (Capa 2); talleres culturales (Capa 3) |
| Deporte | Temáticas del RENOJ; intereses y experiencia de voluntariado | Distrito | Intereses deportivos (Capa 2); talleres deportivos (Capa 3) |
| Salud mental y bienestar | Episodio depresivo; interés en "salud mental y bienestar" | Lima Metropolitana; distrito (solo voluntariado) | En la Capa 3 hasta ahora no hay oferta de salud |
| Salud sexual y reproductiva | Maternidad adolescente | Distrito | Oferta por identificar |
| Prevención de la violencia | Casos atendidos en los CEM; violencia de pareja; discriminación | Distrito y Lima Metropolitana | Oferta por identificar |
| Seguridad y uso del espacio público | Percepción de inseguridad; inseguridad de noche | Lima Metropolitana | Horarios y lugares de las actividades (Capa 3) |
| Inclusión | Discapacidad por distrito | Distrito | Accesibilidad de la oferta (Capa 3) |

### 8.17 Brechas de la Capa 1

- **Casi todo el diagnóstico de necesidades es metropolitano.** Educación, empleo, NINI, internet, salud (encuestas), seguridad y participación solo llegan a Lima Metropolitana.
- **Los datos distritales se limitan a** población, organizaciones juveniles, voluntariado, maternidad adolescente, violencia atendida y discapacidad.
- **Años:** los indicadores de encuestas llegan como máximo a 2025. Algunos terminan en 2023 (empleo) o 2024. Solo los registros administrativos llegan a 2026.
- **No hay datos de** emprendimiento, práctica deportiva, participación cultural, uso del tiempo ni migración por distrito.
- **El único dato de intereses declarados** es el de las personas voluntarias, que no representa a toda la juventud. La Capa 2 tendrá que cubrir ese vacío.
- **Falta verificar** 8 tablas que solo aparecen en los tableros consolidados (actividades que se dejan de hacer por inseguridad, revictimización, violencia alguna vez, conocimiento y preferencia por la democracia, población inmigrante, PRONACEJ).

### 8.18 Orden de extracción propuesto

Antes de empezar conviene resolver tres pendientes de la sección 6: el umbral para ocultar celdas pequeñas, la fuente de las estimaciones de población y las condiciones de uso de los datos.

| Paso | Conjunto de datos | Por qué en este orden |
|---|---|---|
| 1 | **Población joven y total por distrito** (2019–2026) | Es la base de todo: dimensiona la población objetivo y es el denominador de todas las tasas distritales. No es sensible y tiene pocas filas, así que sirve para probar el método de extracción. |
| 2 | **Los 38 indicadores de encuestas** para Lima Metropolitana y el total nacional, con CV | Evita que la Capa 1 quede reducida a demografía: cubre educación, empleo, NINI, salud, internet, seguridad, violencia y participación. Todos tienen la misma estructura, así que un mismo procedimiento sirve para todos. No son sensibles. |
| 3 | **Las 8 tablas que solo están en los tableros consolidados** (primero verificarlas y, si son útiles, extraerlas) | Algunas pueden ser muy relevantes, como las actividades que los jóvenes dejan de hacer por inseguridad. Conviene verificarlas mientras se trabaja con la misma estructura del paso 2. |
| 4 | **RENOJ y voluntariado**, solo como conteos por distrito | Son evidencia distrital de participación e intereses declarados, y conectan directamente con las Capas 2 y 3. Tienen una sensibilidad baja si se extraen solo como conteos. |
| 5 | **Maternidad adolescente por distrito** (CNV) | Es evidencia distrital de una necesidad concreta. Usa como denominador la población del paso 1. Antes hay que confirmar qué significa el distrito en este registro. |
| 6 | **Casos atendidos en los CEM y discapacidad** por distrito | Son los más sensibles. Van al final, cuando ya esté decidido el umbral para ocultar celdas pequeñas y confirmado el significado del distrito. |
| 7 | **Contexto departamental o nacional** (opcional): MININTER, INPE, sector cultural, IPD, migración, Política Nacional de Juventud | Aportan poco para Lima Este. Solo se extraerían si el análisis lo necesita. |

---

## Anexo: flujo técnico de consulta a Power BI

Este anexo documenta el mecanismo para poder reproducirlo. No es el scraper definitivo.

1. **Clave del reporte:** cada página del portal inserta un `iframe` con la URL `https://app.powerbi.com/view?r=<r>`. El parámetro `r` es un JSON en base64 con la forma `{"k": <clave>, "t": <tenant>, "c": 4}`. Todos los tableros comparten el tenant `179bdda8-d964-43ff-ad3b-674186a2fa28`.
2. **Servidor de la API:** el visor indica `resolvedClusterUri = https://wabi-south-central-us-redirect.analysis.windows.net/`. Quitando `-redirect` y agregando `-api` se obtiene `https://wabi-south-central-us-api.analysis.windows.net`.
3. **Metadatos:** `GET /public/reports/<k>/modelsAndExploration?preferReadOnlySession=true` con la cabecera `X-PowerBI-ResourceKey: <k>`. Devuelve `modelId`, `dbName` (id del conjunto de datos), `reportId`, `LastRefreshTime` y las páginas del reporte.
4. **Esquema:** `POST /public/reports/conceptualschema` con el cuerpo `{"modelIds": [<modelId>]}` y la misma cabecera. Devuelve las tablas y columnas.
5. **Datos:** `POST /public/reports/querydata?synchronous=true` con una consulta semántica (`SemanticQueryDataShapeCommand`) que indica tabla, columnas, filtros (`Where` con `In`) y límite de filas (`DataReduction`).
6. **Respuesta:** JSON comprimido con gzip en formato "DSR". Las filas vienen en `DS[0].PH[0].DM0`: `C` son los valores, `R` indica valores repetidos de la fila anterior, `Ø` indica nulos y `ValueDicts` contiene los diccionarios de texto.

Claves de los reportes de los módulos. Las de los 48 indicadores se obtienen del `iframe` de cada página.

| Reporte | Clave (`k`) |
|---|---|
| Datos Demográficos | `ebddf39c-9fde-4695-9385-4ff363a3ffcf` |
| Indicadores regionales (consolidado) | `e53bf32b-4313-45fa-966b-33172bd8d50f` |
| RENOJ | `a8e15d92-0bea-4689-8269-cbf2f1161419` |
| Programa de Voluntariado Juvenil | `b6d288e4-c6a4-4890-a3e7-90f63632e731` |
| Política Nacional de Juventud | `b962ae86-3eb8-4ecf-961c-b38912811c8a` |
| Portada de Dato Joven (consolidado) | `45bd4507-845f-4073-a748-099f05060d12` |
