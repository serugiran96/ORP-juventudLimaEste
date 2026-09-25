# Catálogo de fuentes

Registro formal de las fuentes del proyecto, organizado por capa de análisis (ver `README.md`). Este catálogo se completa **antes** de la extracción de datos: aquí no hay datos extraídos, solo la descripción de cada fuente.

- **Fecha de elaboración:** 23/09/2026.
- **Última actualización:** 25/09/2026. Se reemplazaron las fichas de actividades de la Capa 3 por fichas de fuentes y un registro de oferta (`capa3_registro_oferta.csv`). Antes, ese mismo día, se agregaron las fuentes representativas de la Capa 2 (C2-05 a C2-07) y se actualizaron las fichas de Ipsos. Antes (24/09/2026) se actualizaron C1-01 y C1-02 con la exploración técnica de Dato Joven.
- **Alcance del proyecto:** jóvenes de 15 a 30 años en siete distritos de Lima Este: Ate, Chaclacayo, El Agustino, La Molina, Lurigancho-Chosica, San Juan de Lurigancho y Santa Anita.

## Cómo se construyó

Cada página se consultó una vez, el 23/09/2026, solo para leer su descripción. No se hizo scraping, no se descargaron archivos y no se escribió código.

- Las páginas del Observatorio Nacional de Juventud, de Ipsos y de munichosica.pe **sí pudieron consultarse**.
- Las páginas de **gob.pe rechazaron la consulta automatizada** (respuesta HTTP 418) ese día. El 25/09/2026 sí respondieron, y la Capa 3 se construyó con ellas (ver "Capa 3").
- **Excepción:** las fichas C1-01 y C1-02 se completaron el 24/09/2026 con una exploración técnica de los tableros de Dato Joven. Esa exploración sí hizo consultas pequeñas a los tableros y revisó archivos de muestra. El método y los detalles están en [`exploracion_dato_joven.md`](exploracion_dato_joven.md).

## Convenciones

| Término | Significado |
|---|---|
| **No indica** | La página se consultó y no menciona el dato. |
| **Por verificar** | No se pudo consultar la página, o el dato requiere revisar el documento completo. |
| **Por identificar** | Todavía no hay una fuente para ese caso. |
| **Explorada técnicamente** | Además de leer la página, se revisaron la estructura de sus datos y cómo obtenerlos (ver `exploracion_dato_joven.md`). |
| (título) / (URL) | El dato se tomó del título o de la dirección de la página, no de su contenido. |

## Resumen

| ID | Capa | Fuente | Año | Población | Cobertura | Estado |
|---|---|---|---|---|---|---|
| C1-01 | 1 | Dato Joven — Observatorio Nacional de Juventud | 2019–2026 | 15–29 años (según módulo) | Distrito (población, RENOJ, voluntariado) | **Explorada técnicamente** |
| C1-02 | 1 | Indicadores de Juventud — Observatorio Nacional de Juventud | 2019–2026 (varía por indicador) | 15–29 años (según indicador) | Lima Metropolitana (encuestas); distrito (algunos registros) | **Explorada técnicamente** |
| C1-03 | 1 | Biblio Joven — Observatorio Nacional de Juventud | 2019–2026 | Según documento | Nacional (según documento) | Consultada |
| C2-01 | 2 | Ipsos — Generación Z | 2017 | 15 a 21 años | Lima Metropolitana | Consultada (el PDF no trae cifras) |
| C2-02 | 2 | Ipsos — Gen Z: Perfil del adolescente y joven del Perú urbano 2019 | 2019 | 13 a 20 años | Perú urbano | Consultada |
| C2-03 | 2 | Ipsos — Perfil del adolescente y joven en el Perú Urbano 2020 | 2020 | 13 a 20 años | 11 ciudades del Perú urbano | Consultada |
| C2-04 | 2 | Ipsos — Generaciones en el Perú 2022 | 2021–2022 | Gen Z: nacidos 1997–2009 | Perú urbano (según la infografía) | Consultada |
| C2-05 | 2 | ENUT 2024 — Encuesta Nacional de Uso del Tiempo (INEI) | 2024 | 12+ (se usan 15–29) | Nacional; Lima Metropolitana; Lima Este (estimación propia) | **Procesada** |
| C2-06 | 2 | ENAPRES, capítulo 800A: patrimonio, servicios y bienes culturales (INEI) | 2022–2025 | 14+ (se usan 15–29) | Nacional; Lima Metropolitana; Lima Este (estimación propia) | **Procesada** |
| C2-07 | 2 | ENAHO, Módulo 03: educación e internet (INEI) | 2022–2025 | 15–29 | Nacional; Lima Metropolitana; Lima Este (estimación propia) | **Procesada** |
| C3-01 | 3 | Notas de prensa de las siete municipalidades en gob.pe | 2024–2026 | Vecinos; se registra la edad de cada actividad | Los siete distritos | **Procesada** |
| C3-02 | 3 | munichosica.pe (Municipalidad de Lurigancho-Chosica) | 2024–2026 | Ídem | Lurigancho-Chosica | **Procesada** |
| C3-03 | 3 | SERPAR — clubes metropolitanos de Lima Este | 2024–2026 | Ídem | SJL y Ate | **Procesada** |
| C3-04 | 3 | SENAJU — actividades con sede en Lima Este | 2024–2026 | 15–29 años (casi siempre) | Varios distritos | **Procesada** |
| C3-05 | 3 | gob.pe: MTPE, IPD, Ministerio de Cultura, DEVIDA, Municipalidad de Lima | 2024–2026 | Ídem | Notas que mencionan los distritos | **Procesada** |
| C3-06 | 3 | Prensa y buscador web | 2024–2026 | Ídem | Complementaria | Consultada |

---

## Capa 1 — Contexto, características y necesidades

Dato Joven es la **fuente estructural** de esta capa. Temas prioritarios: datos demográficos, educación, empleo, salud, victimización y seguridad, violencia y discriminación, participación ciudadana, competencias digitales, migración, organizaciones juveniles y voluntariado.

Se priorizarán los datos de 15 a 30 años y de Lima o Lima Este cuando la fuente lo permita. **Un dato nacional o regional no representa directamente a Lima Este.**

### C1-01 — Dato Joven

Esta ficha cubre la plataforma y sus módulos de población, organizaciones juveniles, voluntariado y Política Nacional. El módulo de indicadores se describe en C1-02.

| Campo | Valor |
|---|---|
| Capa | 1 — fuente principal |
| Institución | Observatorio Nacional de Juventud (MINEDU). Contacto: senaju_onajuv@minedu.gob.pe |
| URL | https://observatorio-juventud.minedu.gob.pe/dato-joven/ |
| Módulos | Política Nacional de Juventud; Datos Demográficos; Indicadores de Juventud (ver C1-02); Organizaciones juveniles (RENOJ); Programa de Voluntariado Juvenil. |
| Año / fecha | Datos Demográficos: 2019–2026. RENOJ: organizaciones acreditadas entre 2019 y 2026. Voluntariado y Política Nacional: por verificar. Los tableros se actualizaron por última vez entre el 20/08/2026 y el 26/08/2026. |
| Población / edad | Datos Demográficos: 15–19, 20–24 y 25–29 años, por sexo. **No incluye a personas de 30 años.** RENOJ y Voluntariado: edad y rango de edad de las personas registradas. |
| Cobertura geográfica | **Distrito (UBIGEO)** en Datos Demográficos, RENOJ y personas voluntarias inscritas; **verificado para los siete distritos**. Política Nacional: solo nacional. |
| Fuentes de origen | Según el portal: ENAHO, EPEN, ENDES, ENAPRES y registros administrativos. Las estimaciones de población provienen del Repositorio Único Nacional de Información en Salud (REUNIS) y de las proyecciones de población del INEI; sus series por edad son inestables entre años (ver `metodologia_capa1.md`, D5). |
| Aporte al proyecto | Población joven por distrito, edad, sexo y año, que sirve de denominador para calcular tasas. Organizaciones juveniles por distrito, temática y tipo, que también sirve para la Capa 3. Personas voluntarias por distrito, con sus **intereses declarados**, que conectan con la Capa 2. |
| Tipo de información | Estadística oficial y registros administrativos. |
| Formato | Tableros de Power BI publicados en la web. No hay descarga en CSV. |
| Posible método de extracción | **Consultas directas a los endpoints públicos de Power BI**: verificado que funcionan sin iniciar sesión y sin Selenium. Solo consultas agregadas. Alternativa: solicitar los datos formalmente al Observatorio. |
| Limitaciones | Los endpoints no están documentados y pueden cambiar. No hay datos para 30 años; se usará 15–29 como aproximación. Los modelos contienen tablas con datos individuales (miembros del RENOJ, personas voluntarias) que **no se extraerán**. Falta confirmar si el distrito de las personas voluntarias es el de residencia. |

### C1-02 — Indicadores de Juventud

| Campo | Valor |
|---|---|
| Capa | 1 — módulo de Dato Joven (C1-01) |
| Institución | Observatorio Nacional de Juventud (MINEDU) |
| URL | https://observatorio-juventud.minedu.gob.pe/indicadores/ y el tablero consolidado https://observatorio-juventud.minedu.gob.pe/indicadores-regionales/ |
| Contenido | 8 categorías y **48 tableros**: 38 indicadores de encuestas y 10 tableros de registros administrativos. Temas: educación, empleo, habilidades digitales, salud, participación ciudadana, violencia y discriminación, victimización y seguridad, y juventud migrante. |
| Año / fecha | Encuestas: entre 2019 y 2025, según el indicador. Por ejemplo, para Lima Metropolitana: NINI 2019–2025, empleo formal 2019–2023, episodio depresivo 2022–2024. Registros con distrito: CNV, CEM y CONADIS 2019–2026; certificación de discapacidad 2019–2025. Los tableros se actualizaron por última vez entre junio y septiembre de 2026. |
| Población / edad | La mayoría: 15–29 años. Algunos indicadores usan 15–19, 17–18, 17–24, 18–29 o 22–24 años, y los de violencia de pareja, mujeres de 15 a 29. **Ninguno incluye a personas de 30 años.** |
| Cobertura geográfica | **Encuestas:** 25 regiones más el total nacional. **"Lima Metropolitana" aparece separada de "Lima Región" y del "Callao"**, pero no hay datos por distrito. **Registros:** CNV, CEM, certificación de discapacidad y CONADIS tienen distrito (verificado para los siete). INPE, MININTER y sector cultural solo tienen departamento. IPD y migración no tienen lugar de residencia. |
| Categorías | Lima Metropolitana: total, sexo y área urbana. Solo a nivel nacional: etnia, lengua materna, pobreza, nivel educativo y dominio geográfico. Cada valor de encuesta viene con su **coeficiente de variación (CV)**. |
| Fuentes de origen | Encuestas: ENAHO, EPEN, ENDES y ENAPRES (verificado en cada indicador). Registros administrativos: certificación de discapacidad (MINSA), CONADIS, CEM, certificados de nacido vivo, INPE, MININTER, IPD y movimiento migratorio. |
| Aporte al proyecto | Contexto de necesidades en Lima Metropolitana: educación, empleo, salud, uso de internet, participación y seguridad. Datos por distrito sobre maternidad adolescente, violencia atendida en los CEM y discapacidad. |
| Tipo de información | Estadística oficial (encuestas) y registros administrativos. |
| Formato | Tableros de Power BI. El botón "Fuente de datos" (Excel) **no es fiable**: 37 de 42 enlaces apuntan al archivo de otro indicador. Cada indicador tiene manuales en PDF (24 archivos distintos), aún sin revisar. |
| Posible método de extracción | Endpoints de Power BI, usando los **tableros individuales**, que tienen más detalle que el consolidado. Solo consultas agregadas; en los registros sensibles se ocultan las celdas pequeñas. VIH/SIDA queda excluido. |
| Limitaciones | Los indicadores de encuestas corresponden a Lima Metropolitana (43 distritos) y **no representan a Lima Este**. Los años disponibles varían según el indicador. Falta confirmar si el distrito del CNV y del CEM es el de residencia o el del establecimiento. Los registros sensibles solo se usarán agregados. |

### C1-03 — Biblio Joven

| Campo | Valor |
|---|---|
| Capa | 1 — complementaria (algunos documentos también sirven a la Capa 2) |
| Institución | Observatorio Nacional de Juventud (MINEDU) |
| URL | https://observatorio-juventud.minedu.gob.pe/biblio-joven/ |
| Año / fecha | Filtros de publicación entre 2019 y 2026. |
| Población / edad | Varía según el documento. |
| Cobertura geográfica | Varía según el documento. En el listado no se encontraron documentos específicos sobre Lima o Lima Este. |
| Contenido | "Publicaciones científicas, informes de política, boletines estadísticos y estudios temáticos". Filtros temáticos: Población y demografía, Educación, Empleo y emprendimiento, Salud y bienestar, Participación juvenil, Violencia y seguridad, Habilidades digitales, Victimización, Otros. |
| Documentos a revisar | *Juventud en Cifras Panorama Nacional 2019-2024* (2025); *Habilidades digitales juveniles 2024* (2025); *Juventud y trabajo no remunerado 2024* (2025); *Jóvenes víctimas de violencia 2025* (2026); *Jóvenes en Agenda 2026* (2026). |
| Aporte al proyecto | Contexto e interpretación de los indicadores. Algunos documentos pueden aportar datos recientes sobre uso del tiempo y competencias digitales. |
| Tipo de información | Estudios, boletines e informes. |
| Posible método de extracción | Revisión documental manual. |
| Limitaciones | Mayormente de alcance nacional. El formato de los archivos está por verificar. |

---

## Capa 2 — Intereses, hábitos y aspiraciones

Variables de interés: entretenimiento, cultura, deporte, tecnología, internet y redes sociales, educación y capacitación, empleo, emprendimiento, consumo, aspiraciones, uso del tiempo y preferencias.

**Los estudios de esta capa difieren en año, población y cobertura.** Los más antiguos sirven para identificar dimensiones e hipótesis, **no para describir a la juventud de Lima Este en 2026**.

Desde el 25/09/2026, la evidencia principal de esta capa son tres encuestas representativas del INEI (C2-05 a C2-07), procesadas por el proyecto con sus microdatos. Lima Este se estima como dominio no planificado, con umbrales de CV. Los estudios de Ipsos (C2-01 a C2-04) se usan solo para identificar dimensiones. Detalles en `metodologia_capa2.md`.

### Comparación entre estudios

| ID | Estudio | Trabajo de campo | Edad estudiada | Edad de esa cohorte en 2026 | Cobertura | Muestra |
|---|---|---|---|---|---|---|
| C2-01 | Generación Z | No indica (publicado jul. 2017) | 15–21 | ≈ 24–30 | Lima Metropolitana | 500 |
| C2-02 | Gen Z: Perfil... Perú urbano 2019 | may.–jun. 2019 | 13–20 | ≈ 20–27 | Perú urbano | 1 003 |
| C2-03 | Perfil... Perú Urbano 2020 | 27 feb.–15 mar. 2020 | 13–20 | ≈ 19–26 | 11 ciudades del Perú urbano | 995 |
| C2-04 | Generaciones en el Perú 2022 | 2021–2022 (varios estudios) | Gen Z nacida 1997–2009; foco en 18–25 | ≈ 17–29 | No indica | No indica |

La columna "edad de esa cohorte en 2026" es un cálculo aproximado. Muestra que **las personas encuestadas ya no tienen la edad que tenían entonces**: los jóvenes de 15 a 30 años de hoy no son los que respondieron estos estudios.

### C2-01 — Generación Z (2017)

| Campo | Valor |
|---|---|
| Capa | 2 |
| Institución | Ipsos Perú |
| URL | https://www.ipsos.com/es-pe/generacion-z |
| Año / fecha | Publicado el 31/07/2017. Fecha del trabajo de campo: no indica. |
| Población / edad | 500 jóvenes de 15 a 21 años "de todos niveles socio-económicos". |
| Cobertura geográfica | Lima Metropolitana. |
| Metodología | Encuesta. |
| Aporte al proyecto | Perfil laboral y de consumo; expectativas laborales, uso de internet, interés por trabajar en tecnología. |
| Tipo de información | Estudio de mercado (encuesta). |
| Formato | PDF de descarga libre (211 KB). |
| Posible método de extracción | Descarga manual del PDF y registro manual de las cifras relevantes. |
| Limitaciones | Es el estudio más antiguo (9 años). Es el único con cobertura de Lima Metropolitana, pero no por distrito. La muestra es pequeña. |

### C2-02 — Gen Z: Perfil del adolescente y joven del Perú urbano 2019

| Campo | Valor |
|---|---|
| Capa | 2 |
| Institución | Ipsos Perú |
| URL | https://www.ipsos.com/es-pe/gen-z-perfil-del-adolescente-y-joven-del-peru-urbano-2019 |
| Año / fecha | Publicado el 24/09/2019. Trabajo de campo entre mayo y junio de 2019. |
| Población / edad | 1 003 adolescentes y jóvenes de 13 a 20 años, de todos los niveles socioeconómicos. |
| Cobertura geográfica | Perú urbano. |
| Metodología | Encuesta. El tipo de encuesta no se indica. |
| Aporte al proyecto | "Gustos, preferencias, hábitos y actitudes". La página menciona actividades digitales como YouTube, redes sociales, música por aplicaciones y WhatsApp. |
| Tipo de información | Estudio de mercado (encuesta). |
| Formato | PDF de descarga libre (210 KB). |
| Posible método de extracción | Descarga manual del PDF y registro manual. |
| Limitaciones | Incluye a menores de 15 años (13–14), que están fuera del alcance del proyecto. Solo llega hasta los 20 años. Cobertura urbana nacional, sin desagregación confirmada para Lima. Es anterior a la pandemia. |

### C2-03 — Perfil del adolescente y joven en el Perú Urbano 2020

| Campo | Valor |
|---|---|
| Capa | 2 |
| Institución | Ipsos Perú |
| URL | https://www.ipsos.com/es-pe/perfil-del-adolescente-y-joven-en-el-peru-urbano-2020 |
| Año / fecha | Publicado el 02/06/2020. Trabajo de campo del 27/02/2020 al 15/03/2020. |
| Población / edad | 995 adolescentes y jóvenes de 13 a 20 años, de todos los niveles socioeconómicos. |
| Cobertura geográfica | "Once principales ciudades del Perú Urbano". La lista de ciudades está por verificar. |
| Metodología | Encuesta. |
| Aporte al proyecto | Gustos, preferencias, hábitos y actitudes. Situación laboral antes de la cuarentena. |
| Tipo de información | Estudio de mercado (encuesta). |
| Formato | PDF de descarga libre (129 KB). |
| Posible método de extracción | Descarga manual del PDF y registro manual. |
| Limitaciones | Mismo rango de edad que C2-02 (13–20). El trabajo de campo terminó justo antes de la cuarentena por COVID-19, así que no refleja los cambios posteriores. |

### C2-04 — Generaciones en el Perú 2022

| Campo | Valor |
|---|---|
| Capa | 2 |
| Institución | Ipsos Perú |
| URL | https://www.ipsos.com/es-pe/generaciones-en-el-peru-2022 |
| Año / fecha | Publicado el 26/01/2023. Datos de "diferentes fuentes de estudios multiclientes realizados entre el 2021 y 2022". |
| Población / edad | Compara generaciones. La Generación Z son "peruanos nacidos entre 1997 y 2009", "centrándose entre los entrevistados de 18 a 25 años". |
| Cobertura geográfica | La página no lo indica; la infografía se titula "Generaciones en el Perú urbano". |
| Metodología | Combina varios estudios. No indica la muestra ni el detalle metodológico. |
| Aporte al proyecto | Familia, trabajo, bancarización, ahorro, endeudamiento, entretenimiento y compras. Es el estudio más reciente de la lista. |
| Tipo de información | Estudio de mercado (síntesis de varias encuestas). |
| Formato | PDF de descarga libre (293 KB). |
| Posible método de extracción | Descarga manual del PDF y registro manual. |
| Limitaciones | Cobertura y muestra desconocidas. La definición por año de nacimiento no coincide con el rango de 15 a 30 años. Está orientado al consumo y no cubre temas como cultura, deporte o participación. |

### C2-05 — ENUT 2024: Encuesta Nacional de Uso del Tiempo

| Campo | Valor |
|---|---|
| Capa | 2 — representativa |
| Institución | INEI |
| URL | https://proyectos.inei.gob.pe/microdatos/ (ENUT 2024, módulos 1850, 1854 y 1855) |
| Año / fecha | 2024 |
| Población / edad | 12 años o más. Se usan 15–29 (y 30+ como contraste). |
| Cobertura geográfica | Nacional. El proyecto estima Lima Metropolitana y Lima Este (dominio no planificado, ~230 jóvenes en la muestra). |
| Aporte al proyecto | Diario de 144 franjas de 10 minutos por día: horas y participación en estudio, trabajo, deporte, aficiones, eventos, uso de dispositivos, lectura, voluntariado, etc. Satisfacción con el tiempo libre. |
| Tipo de información | Encuesta oficial (microdatos). |
| Método de extracción | `scripts/capa2_uso_tiempo_enut.py` (descarga de microdatos y cálculo propio). Validado con las horas de estudio publicadas por el INEI (±0,6 h). |
| Limitaciones | Un solo año. La base no trae el estrato de diseño (se aproxima). Mide actividades realizadas, no preferencias. |

### C2-06 — ENAPRES, capítulo 800A: patrimonio, servicios y bienes culturales

| Campo | Valor |
|---|---|
| Capa | 2 — representativa |
| Institución | INEI (módulo diseñado con el Ministerio de Cultura) |
| URL | https://proyectos.inei.gob.pe/microdatos/ (ENAPRES 2022–2025, capítulo 800A) |
| Año / fecha | 2022–2025 (anual) |
| Población / edad | 14 años o más, una persona por hogar. Se usan 15–29 (y 30+ como contraste). |
| Cobertura geográfica | Nacional y Lima Metropolitana por año; Lima Metropolitana y Lima Este agrupando 2022–2025 (~180 jóvenes de Lima Este por año). |
| Aporte al proyecto | Asistencia a 11 servicios culturales (teatro, danza, circo, conciertos, cine, exposiciones, ferias, bibliotecas, festivales), visitas al patrimonio, 16 bienes culturales (incluye videojuegos y consumo digital), forma de entrada y **motivo de no asistencia**. |
| Tipo de información | Encuesta oficial (microdatos). |
| Método de extracción | `scripts/capa2_cultura_enapres.py`. Validado: teatro 14+ nacional 2024 = 8,6 %, igual al Ministerio de Cultura. |
| Limitaciones | La base de 2024–2025 no trae el estrato (se aproxima). Lima Este requiere agrupar años. |

### C2-07 — ENAHO, Módulo 03: educación e internet

| Campo | Valor |
|---|---|
| Capa | 2 — representativa |
| Institución | INEI |
| URL | https://proyectos.inei.gob.pe/microdatos/ (ENAHO 2022–2025, Módulo 03) |
| Año / fecha | 2022–2025 (anual) |
| Población / edad | 15–29 |
| Cobertura geográfica | Nacional, Lima Metropolitana y Lima Este (~700 jóvenes de Lima Este por año) |
| Aporte al proyecto | Propósitos de uso de internet (entretenimiento, educación y capacitación, comunicación, compras, ventas), asistencia educativa y nivel, y motivo principal para no estudiar. |
| Tipo de información | Encuesta oficial (microdatos). |
| Método de extracción | `scripts/capa2_educacion_internet_enaho.py`. Validado con Dato Joven (uso de internet ±0,2; asistencia universitaria ±1 punto). |
| Limitaciones | No pregunta por cursos o talleres no formales ni por intereses de aprendizaje. |

### Fuentes revisadas y descartadas en la Capa 2

- **Ipsos, Reporte de Generaciones 2024:** encuesta global sobre el conocimiento de los términos generacionales; no trata intereses juveniles.
- **SENAJU, *Jóvenes en Agenda* (informe final, 2025):** concurso de investigaciones hechas por jóvenes; no es una consulta sobre intereses.
- **C2-01 (Ipsos, Generación Z 2017):** el PDF público es solo la portada de la revista; no aporta cifras.

---

## Capa 3 — Evidencia territorial de Lima Este

Desde el 25/09/2026 las actividades ya no se describen en fichas aquí: cada una es una fila de
[`capa3_registro_oferta.csv`](capa3_registro_oferta.csv). Esta sección describe las **fuentes** de las que salen.
El método, los criterios de codificación y las limitaciones están en [`metodologia_capa3.md`](metodologia_capa3.md).

### Tipos de evidencia

| Tipo | Qué permite afirmar | Cuándo se registra |
|---|---|---|
| **Oferta** | La actividad se ofreció o se realizó. | La fuente la anuncia o la describe. |
| **Participación declarada** | Hubo inscritos, asistentes o participantes, según quien organiza. | La fuente publica una cifra o una mención explícita de participantes. |
| **Demanda observada** | Hubo más interesados que cupos. | Solo con una señal concreta: inscripciones agotadas, inscritos por encima del cupo, lista de espera. **No se infiere de que una actividad exista.** |

### Fuentes

| ID | Fuente | Cobertura | Periodo | Acceso | Verificación |
|---|---|---|---|---|---|
| C3-01 | Notas de prensa de las siete municipalidades en gob.pe | Los siete distritos | 01/2024–09/2026 | `scripts/capa3_noticias_gobpe.py` (búsqueda por términos) | Texto completo |
| C3-02 | munichosica.pe, sitio de la Municipalidad de Lurigancho-Chosica | Lurigancho-Chosica | 01/2024–09/2026 | `scripts/capa3_noticias_wp.py` (API de WordPress) | Texto completo |
| C3-03 | SERPAR, Servicio de Parques de Lima (serpar.gob.pe) | Clubes metropolitanos Wiracocha (SJL), Cahuide y Huaycán (Ate) | 01/2024–09/2026 | `scripts/capa3_noticias_wp.py` | Texto completo |
| C3-04 | SENAJU, Secretaría Nacional de la Juventud (juventud.gob.pe) | Actividades con sede en Lima Este | 01/2024–09/2026 | `scripts/capa3_noticias_wp.py` (búsqueda por nombre de distrito) | Texto completo |
| C3-05 | Notas en gob.pe del MTPE, IPD, Ministerio de Cultura, DEVIDA y Municipalidad de Lima | Notas que mencionan un distrito de Lima Este | 01/2024–09/2026 | `scripts/capa3_noticias_gobpe.py sectores` | Texto completo |
| C3-06 | Prensa y buscador web | Vacíos de las fuentes anteriores | 2024–2026 | Búsqueda manual | Texto completo si el artículo pudo leerse; si no, resumen del buscador |

**Acceso a gob.pe.** El 23/09/2026 gob.pe respondió HTTP 418 a la consulta automatizada, así que las fichas
iniciales de esta capa quedaron "por verificar". El 25/09/2026 respondió con normalidad a un agente de usuario
identificado. Su `robots.txt` solo prohíbe `/admin/` y la paginación con `sheet=`; los scripts no la usan.

### Consideraciones para toda la capa

- **Sesgo de visibilidad:** solo se registra lo que se publica en internet. Las municipalidades publican con
  frecuencia muy distinta: Chaclacayo tiene 6 notas en gob.pe entre 2024 y 2026 que coinciden con la búsqueda;
  El Agustino, 365. **Pocas actividades registradas no significan poca oferta.**
- **Oferta no municipal:** organizaciones sociales, parroquias, ONG, colectivos culturales y academias privadas
  casi no aparecen, por falta de una fuente sistemática.
- **Cifras declaradas:** las publica quien organiza, en notas de prensa. Suelen ser aproximadas ("más de") y no
  están auditadas.

### Equivalencia con las fichas anteriores

Las fichas C3-01 a C3-11 del 23/09/2026 describían actividades, no fuentes. Su contenido se verificó y quedó en
el registro:

| Ficha anterior | Actividad | Dónde quedó |
|---|---|---|
| C3-01 | Ate: Vacaciones Útiles 2026 | Registro (fuente C3-01) |
| C3-02 | Chaclacayo: fuente por identificar | Sus notas están en gob.pe (C3-01), pero son muy pocas |
| C3-03 | El Agustino: Muni Becas 2025 | Registro (fuente C3-01) |
| C3-04, C3-05, C3-06 | La Molina: Molitalleres, talleres deportivos y talleres de computación | Registro (fuente C3-01) |
| C3-07 | Lurigancho-Chosica: Talleres Municipales de Verano 2026 | Registro (fuente C3-02) |
| C3-08 | Lurigancho-Chosica: "Aventureros de Cajamarquilla" | Registro. **Es para niños de 7 a 11 años**, fuera del rango del proyecto |
| C3-09 | San Juan de Lurigancho: FestiJoven 2025 | Registro (fuente C3-01) |
| C3-10, C3-11 | Santa Anita: talleres de verano 2026 y "Impulsamos el talento de nuestros jóvenes" | Registro (fuente C3-01) |

---

## Integración de las capas

Se mantiene el modelo metodológico del `README.md`:

**necesidades y contexto (Capa 1) + intereses y aspiraciones (Capa 2) + evidencia territorial: oferta y participación (Capa 3) → identificación posterior de coincidencias, brechas e hipótesis de oportunidades.**

### Cobertura temática

La siguiente tabla muestra qué fuentes tratan cada tema. En la Capa 3 se indica el número de actividades del registro (`capa3_registro_oferta.csv`) con ese tema, contando cada actividad una vez, y entre paréntesis cuántas se dirigen a jóvenes. **No es un cruce de resultados**: sirve para ver qué temas tienen evidencia en las tres capas y cuáles no.

| Tema | Capa 1 | Capa 2 | Capa 3 (actividades registradas) |
|---|---|---|---|
| Educación y capacitación | C1-02, C1-03 | C2-07 (asistencia, motivos para no estudiar, uso educativo de internet); C2-03 | Preparación preuniversitaria 19 (11); orientación vocacional 3 (3); idiomas 4 (0) |
| Empleo | C1-02, C1-03 | C2-01, C2-03, C2-04 | 25 (13) |
| Emprendimiento | C1-03 | C2-02, C2-03 (solo Ipsos, 2019–2020) | 11 (4) |
| Tecnología y competencias digitales | C1-02, C1-03 | C2-05, C2-06, C2-07; C2-02, C2-04 | 10 (2) |
| Cultura y arte | C1-02 (trabajadores del sector cultural, solo por departamento) | C2-06 (asistencia y consumo cultural); C2-05 | Arte y cultura 46 (9); patrimonio 8 (1) |
| Deporte | C1-02 (atletas del IPD, sin distrito) | C2-05 (práctica semanal); C2-02 | 39 (3) |
| Entretenimiento y uso del tiempo | C1-03 | C2-05, C2-06; C2-02, C2-03, C2-04 | Recreación 5 (0) |
| Consumo y finanzas | — | C2-01, C2-04 | Educación financiera 1 (0) |
| Salud | C1-02, C1-03 | — | Salud y salud mental 15 (3); inclusión y discapacidad 9 (0) |
| Seguridad, violencia y discriminación | C1-02, C1-03 | — | Prevención de drogas y violencia 10 (2); gestión de riesgos y primeros auxilios 2 (1) |
| Participación y organizaciones juveniles | C1-01, C1-02, C1-03 | — | Participación y voluntariado 22 (13) |
| Migración | C1-02 | — | — |

---

## Pendientes de investigación

### Capa 1

Resueltos con la exploración técnica del 24/09/2026:

- [x] Rango de edad de Dato Joven: llega hasta los 29 años. Se aplica la aproximación de 15 a 29 prevista en el `README.md`.
- [x] Nivel de los indicadores de encuestas: solo regional. "Lima Metropolitana" aparece separada de "Lima Región" y del "Callao".
- [x] Población por distrito: disponible para los siete distritos, en rangos de 15 a 19, 20 a 24 y 25 a 29 años. No hay datos para 30 años.
- [x] Años y fecha de actualización: registrados en las fichas C1-01 y C1-02.
- [x] Exportación de datos: no hay descarga útil. Los datos se pueden obtener consultando directamente los tableros de Power BI.
- [x] RENOJ por distrito: sí, verificado para los siete distritos.

Pendientes:

- [x] Fuente de las estimaciones de población: REUNIS y proyecciones del INEI. Sus series por edad son inestables entre años (ver `metodologia_capa1.md`).
- [ ] Confirmar si el distrito del CNV, del CEM y de las personas voluntarias es el de residencia o el del establecimiento.
- [ ] Revisar los manuales en PDF de los indicadores: definiciones, metodología y umbral de CV.
- [ ] Confirmar las condiciones de uso de los datos con el Observatorio, o solicitarlos formalmente.
- [ ] Decidir el umbral para ocultar celdas pequeñas en los registros sensibles (propuesta: menos de 10 casos).
- [ ] Buscar documentos sobre Lima o Lima Este en Biblio Joven; en el listado revisado no aparecen.

### Capa 2

- [x] Fuentes posteriores a 2022: se agregaron la ENUT 2024, la ENAPRES 2022–2025 y la ENAHO 2022–2025 (C2-05 a C2-07), que cubren a jóvenes de 15 a 29 años.
- [x] PDF de Ipsos revisados: las cifras están en `capa2_estudios_ipsos.csv`. Cubren diversión, medios, aspiraciones y emprendimiento; no cubren cultura ni deporte en detalle.
- [x] Resultados para Lima: ningún estudio de Ipsos los separa; las encuestas del INEI se procesaron para Lima Metropolitana y Lima Este.
- [ ] Buscar evidencia representativa y reciente sobre **aspiraciones laborales y emprendimiento** (solo hay datos de Ipsos 2019–2020).
- [ ] Lista de ciudades de C2-03 y fecha de campo de C2-01: no disponibles en las fuentes públicas.
- [ ] Las encuestas miden prácticas, no intereses declarados en actividades concretas: evaluar una consulta propia a jóvenes de Lima Este.

### Capa 3

Resueltos el 25/09/2026:

- [x] Notas de gob.pe revisadas: gob.pe volvió a responder y se recolectaron las notas de las siete municipalidades (ver `metodologia_capa3.md`).
- [x] Chaclacayo: su fuente son sus notas en gob.pe, pero publica muy poco (6 notas en 2024–2026).
- [x] Edad de cada actividad: registrada en `incluye_15_29`; la mayor parte de los talleres de verano es para 6 a 17 años.
- [x] Cifras de participación: 59 actividades con participación declarada.
- [x] Oferta en empleo, emprendimiento, salud mental y seguridad: registrada, aunque poca se dirige a jóvenes.
- [x] Evidencia de demanda: 4 actividades, cada una referida solo a esa oferta concreta (una beca de CEPREMUNI en Santa Anita, talleres de SENAJU, Academia IPD y un taller infantil).
- [x] Scraping: se hizo respetando el `robots.txt` de cada sitio (gob.pe sin paginación con `sheet=`).

Pendientes:

- [ ] Oferta de organizaciones sociales, ONG y colectivos, con una fuente que identifique el distrito.
- [ ] Información directa de las municipalidades (sobre todo Chaclacayo, Ate y SJL en 2024) sobre su oferta, cupos e inscritos.
- [ ] Evidencia de demanda de jóvenes de 18 a 29 años: listas de espera, cupos agotados o consulta directa.
