# Metodología de la Capa 1

Registro del proceso, las transformaciones y las decisiones metodológicas de la Capa 1 (contexto,
características y necesidades de las juventudes). Complementa `exploracion_dato_joven.md` (fuente y mapa
analítico) y `data/README.md` (diccionario de datos).

- **Última actualización:** 24/09/2026.
- **Extracción de datos:** 25/09/2026 (UTC). Los tableros de Dato Joven se habían actualizado por última vez
  entre el 12/06/2026 y el 16/09/2026.

## 1. Proceso

```
scripts/catalogo_dato_joven.py   -> fuentes/catalogo_tableros_dato_joven.csv  (54 tableros)
scripts/extraer_dato_joven.py    -> data/raw/dato_joven/*.csv + _metadatos.json
scripts/empleo_enaho.py          -> data/raw/enaho/*.dta y data/processed/capa1_empleo_enaho*.csv
scripts/procesar_capa1.py        -> data/processed/capa1_*.csv
notebooks/01_capa1_diagnostico.ipynb -> análisis, gráficos y capa1_resumen_lima_metropolitana.csv
```

`empleo_enaho.py calcular` necesita `capa1_indicadores_encuestas.csv` para validar, así que se ejecuta
después de `procesar_capa1.py`.

`scripts/powerbi_publico.py` es el cliente que consulta los tableros de Power BI publicados en la web. Hace
una consulta por segundo como máximo, pagina los resultados y decodifica el formato de respuesta.

| Conjunto | Tablero de origen | Qué se extrae |
|---|---|---|
| Población | Datos Demográficos | Población joven (3 grupos de edad × sexo) y total, 43 distritos de Lima Metropolitana, 2019–2026; totales del país |
| Encuestas | 38 tableros de indicadores | Tablas `datosRegionales` (Lima Metropolitana y Nacional) y `datosNacionales` |
| Consolidado | Indicadores regionales | 34 tablas; solo se usan las 5 que no están en los tableros individuales |
| RENOJ | Organizaciones juveniles | Número de organizaciones por distrito, año de acreditación, tipo y temática |
| Voluntariado | Programa de Voluntariado Juvenil | Número de personas inscritas por distrito, una variable a la vez |
| Registros sensibles | CNV, CEM, certificación de discapacidad, CONADIS | Conteos por distrito, año y edad/sexo/tipo; se ocultan las celdas menores de 10 al procesar |
| Empleo 2022–2025 | Microdatos de la ENAHO (INEI), Módulo 05 | Desempleo y tasa de actividad de 15–29 años, calculados por el proyecto |

Todas las consultas a Dato Joven son **agregadas**. No se descarga ningún registro individual. Los
microdatos de la ENAHO son anónimos y los publica el INEI. El proyecto solo guarda en `data/processed/`
las estimaciones agregadas.

## 2. Decisiones metodológicas

| ID | Decisión | Motivo |
|---|---|---|
| D1 | Dato Joven se consulta mediante los endpoints públicos de Power BI. | Es la única vía reproducible: los Excel del portal están mal enlazados o solo tienen datos departamentales. |
| D2 | La población objetivo de 15–30 años se aproxima con 15–29. | Ninguna fuente de Dato Joven incluye a personas de 30 años (README). |
| D3 | La evidencia se separa en cuatro niveles (distrito, Lima Este agregado, Lima Metropolitana, nacional) y nunca se mezcla. | Evitar atribuir a Lima Este resultados de geografías mayores. "Lima Este agregado" solo se construye sumando datos distritales. |
| D4 | "Lima Metropolitana" son los 43 distritos de la provincia de Lima, sin el Callao. | Así la define la fuente, que publica el Callao por separado. |
| D5 | La población se usa como **estimación de nivel del año 2026**. **No se interpretan las variaciones entre años.** Las tasas por distrito usan como denominador la población joven de 2026. | Las series de población joven del REUNIS/INEI oscilan ±5–10 % entre años sin cambios equivalentes en la población total. Eso indica cambios de método en la estructura por edad (ver sección 3). |
| D6 | Un valor de encuesta es **referencial** si su CV es mayor de 15 %. "(¬)" se trata como sin dato. | Coincide exactamente con el criterio de la fuente: todos los valores entre paréntesis tienen CV > 15 % y ninguno de los demás lo supera. |
| D7 | Se excluyen 39 filas con etiquetas ambiguas en "Dispositivo de acceso a internet" y "Lugar de acceso a internet". | La fuente repite una misma etiqueta con valores distintos en el mismo año (por ejemplo, tres filas "Celular sin plan de datos"), así que no se puede saber a qué categoría corresponde cada valor. |
| D8 | Del tablero consolidado solo se usan las tablas ausentes en los tableros individuales: actividad que dejó de realizar por la delincuencia, revictimización, violencia física alguna vez, violencia física/sexual/psicológica alguna vez y "democracia siempre preferible". | Los 399 valores que están en ambos tableros coinciden exactamente, así que el consolidado no aporta nada distinto en los indicadores comunes. |
| D9 | Los cambios entre años en las encuestas se evalúan con una prueba aproximada: `z = diferencia / √(ee₁² + ee₂²)`, con `ee = valor × CV / 100`. Un cambio es "distinguible" si \|z\| ≥ 1,96. | Evitar interpretar como cambio real lo que puede ser error de muestreo. Es orientativa: supone muestras independientes. |
| D10 | RENOJ: se usa el total acumulado de organizaciones acreditadas (2019–2026), también por cada 10 mil jóvenes. | El registro no indica si las organizaciones siguen activas. La tasa permite comparar distritos de distinto tamaño. |
| D11 | Voluntariado: solo como **señal complementaria**. Se excluyen los campos sensibles (salud, discapacidad, comunidades, nacionalidad) y los de texto libre. | Son personas que se inscribieron por decisión propia y no representan a la juventud del distrito (indicación del equipo). |
| D12 | Los registros sensibles con datos distritales (maternidad adolescente, violencia atendida en los CEM, certificación de discapacidad, CONADIS) se usan **solo como conteos agregados**. Todo conteo **menor de 10 se oculta**, con **ocultación complementaria**: si en un grupo con total publicado queda una sola celda oculta, se oculta también la siguiente más pequeña. VIH queda excluido. | Decisión del equipo (24/09/2026, P1). Evita que una celda pequeña pueda deducirse restando del total. |
| D13 | Distrito de cada registro: CNV = **residencia de la madre**; CEM = **domicilio de la víctima** (ambos verificados); discapacidad = distrito registrado (sin verificar si es la residencia). | Se verificó que los casos de un distrito se atienden en establecimientos o CEM de otros distritos, y que el UBIGEO coincide con los códigos de domicilio. |
| D14 | Las tasas de los registros usan el promedio anual de 2022–2025 (años completos) y la población de 2026 (D5). Se publican por 1 000 mujeres de 15–19 (CNV) o por 10 000 jóvenes de 15–29. | Se evita usar las series de población por año, que son inestables. Los años parciales (CNV 2026, hasta junio) no entran en el promedio. |
| D15 | El desempleo y la tasa de actividad de Lima Metropolitana de 2024–2025 se calculan con los **microdatos de la ENAHO** (Módulo 05), con las mismas definiciones del INEI. Solo se aceptan si la réplica de 2022–2023 coincide con Dato Joven dentro de ±1 punto. | Decisión del equipo (P2). Resultado: 32 de 32 valores dentro de la tolerancia (diferencia máxima de 0,3 puntos). Los CV calculados por linealización también coinciden con los de Dato Joven. Se etiquetan como "cálculo propio". |
| D16 | La **informalidad no se extiende** a 2024–2025. | Desde 2024 el INEI no publica la variable `ocupinf` en el Módulo 05 ni en otro módulo de la ENAHO anual. Construirla con otra definición no sería comparable ni se podría validar. |
| D17 | Población: se mantiene el nivel de 2026 sin interpretar tendencias (D5). | Decisión del equipo (P3). |

## 3. Hallazgos sobre la calidad de los datos

- **Población (D5).** La fuente es el *Repositorio Único Nacional de Información en Salud (REUNIS)* y las
  *proyecciones de población del INEI*, según el tablero. La población joven de Lima Metropolitana varía
  −12,5 % (2020), +8,1 % (2023) y −8,0 % (2025), mientras la población total cambia entre 0,7 % y 2,4 % al año. En
  26 de los 43 distritos hay alguna variación anual mayor de 10 % entre 2023 y 2026. En La Molina, el
  porcentaje de mujeres entre los jóvenes pasa de 54 % (2022) a 49 % (2026).
- **Total nacional.** Las tablas de población tienen una fila con el total del país (UBIGEO `000000`).
  Sumar todas las filas duplica la población, así que el total se toma de esa fila.
- **Etiquetas ambiguas (D7)** en dos tableros de internet.
- **Consolidado frente a tableros individuales:** los valores coinciden. El consolidado tiene menos
  desagregaciones en algunos indicadores (por ejemplo, desempleo en Lima Metropolitana sin datos por sexo).
- **Intereses declarados del voluntariado:** entre 81 % y 93 % de las personas marca "sí" en cada una de las
  seis temáticas. Por eso no sirven para priorizar temas.
- **Empleo:** los indicadores laborales de Dato Joven para Lima Metropolitana terminan en 2023 (ingresos:
  solo 2022–2023). Se extendieron el desempleo y la tasa de actividad a 2025 con la ENAHO (D15). La
  informalidad no se pudo extender (D16).
- **Registros sensibles:** en las desagregaciones más detalladas, entre el 21 % y el 73 % de las celdas
  tienen menos de 10 casos. Por eso se publican tablas más agregadas: distrito × año, y distrito ×
  categoría para 2022–2025. Si un distrito no aparece en un año, es porque no tiene casos registrados.
- **Los registros no miden prevalencia.** Los casos de los CEM dependen del acceso a los servicios y de la
  decisión de acudir. La certificación de discapacidad depende del acceso al trámite: sus tasas varían de 3 a
  25 por 10 mil jóvenes entre los siete distritos.

## 4. Decisiones del equipo (24/09/2026)

| ID | Decisión | Opción elegida | Alternativas evaluadas |
|---|---|---|---|
| P1 | Registros sensibles distritales | Agregados, ocultando celdas menores de 10 (D12) | Solo maternidad adolescente; solo totales con umbral de 20; no usarlos |
| P2 | Empleo 2024–2026 | Réplica con microdatos de la ENAHO, validada con 2022–2023 (D15) | Informe técnico del INEI con datos de la EPEN (llega a 2026, pero con grupos de 14–24 y 25–44 años, no comparables); Informe Anual del Empleo del MTPE (solo llega a 2023); quedarse en 2023 |
| P3 | Población | Nivel de 2026, sin tendencias (D5, D17) | Promedio 2024–2026; buscar estimaciones distritales por edad del INEI |

## 5. Pendientes

- **Empleo 2026:** la ENAHO anual de 2026 se publicará en 2027.
- **Informalidad 2024–2025:** solo se podría agregar si el INEI vuelve a publicar la variable o publica el
  indicador para jóvenes de 15–29 años.
- **Manuales en PDF de Dato Joven:** no se han revisado (definiciones de cada indicador).
