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

### Prioridad 1 — datos distritales básicos

| # | Dato | Tablero | Detalle | Uso en el proyecto |
|---|---|---|---|---|
| 1 | Población joven | Datos Demográficos | 7 distritos × 3 rangos de edad × sexo × 2019–2026 | Tamaño de la población objetivo y denominador para calcular tasas |
| 2 | Población total | Datos Demográficos | 7 distritos × sexo × 2019–2026 | Porcentaje de jóvenes por distrito |
| 3 | Organizaciones juveniles | RENOJ, tabla `Representantes` | Conteo por distrito × temática × tipo × año. **No se extrae la tabla `Miembros`.** | Participación y tejido organizativo; también alimenta la Capa 3 |
| 4 | Voluntariado | Voluntariado, tabla `fact_Voluntarios` | Conteo por distrito × rango de edad × sexo, y por cada campo `INTERES_VOLUNTARIADO_*` | Participación, e **intereses declarados** que conectan con la Capa 2 |
| 5 | Maternidad adolescente | CNV | Conteo por distrito × año × rango de edad (15–16, 17–18, 19) | Aproximación al embarazo adolescente por distrito |

### Prioridad 2 — registros sensibles, solo agregados

| # | Dato | Tablero | Detalle | Condición |
|---|---|---|---|---|
| 6 | Violencia atendida en los CEM | CEM | Conteo por distrito × año × grupo de edad × sexo × tipo de violencia | Solo conteos, sin datos individuales. Ocultar celdas pequeñas. |
| 7 | Discapacidad | Certificación de discapacidad y CONADIS | Conteo por distrito × año × grupo de edad | Igual que la anterior |

### Prioridad 3 — contexto de Lima Metropolitana

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

- **Fuente de las estimaciones de población** de Datos Demográficos: el tablero tiene un campo "Fuente:" cuyo contenido no se extrajo.
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
