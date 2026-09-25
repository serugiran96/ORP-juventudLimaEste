# Catálogo de fuentes

Registro formal de las fuentes del proyecto, organizado por capa de análisis (ver `README.md`). Este catálogo se completa **antes** de la extracción de datos: aquí no hay datos extraídos, solo la descripción de cada fuente.

- **Fecha de elaboración:** 23/09/2026.
- **Última actualización:** 24/09/2026. Se actualizaron las fichas C1-01 y C1-02 con los resultados de la exploración técnica de Dato Joven.
- **Alcance del proyecto:** jóvenes de 15 a 30 años en siete distritos de Lima Este: Ate, Chaclacayo, El Agustino, La Molina, Lurigancho-Chosica, San Juan de Lurigancho y Santa Anita.

## Cómo se construyó

Cada página se consultó una vez, el 23/09/2026, solo para leer su descripción. No se hizo scraping, no se descargaron archivos y no se escribió código.

- Las páginas del Observatorio Nacional de Juventud, de Ipsos y de munichosica.pe **sí pudieron consultarse**.
- Las páginas de **gob.pe rechazaron la consulta automatizada** (respuesta HTTP 418). En esas fuentes solo se registra lo que dicen el título, la URL o la descripción del equipo; el resto queda **por verificar** con una revisión manual.
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
| C2-01 | 2 | Ipsos — Generación Z | 2017 | 15 a 21 años | Lima Metropolitana | Consultada |
| C2-02 | 2 | Ipsos — Gen Z: Perfil del adolescente y joven del Perú urbano 2019 | 2019 | 13 a 20 años | Perú urbano | Consultada |
| C2-03 | 2 | Ipsos — Perfil del adolescente y joven en el Perú Urbano 2020 | 2020 | 13 a 20 años | 11 ciudades del Perú urbano | Consultada |
| C2-04 | 2 | Ipsos — Generaciones en el Perú 2022 | 2021–2022 | Gen Z: nacidos 1997–2009 | No indica | Consultada |
| C3-01 | 3 | Ate — Talleres Vacaciones Útiles 2026 | 2026 | Por verificar | Ate | Por verificar |
| C3-02 | 3 | Chaclacayo | — | — | Chaclacayo | **Por identificar** |
| C3-03 | 3 | El Agustino — Muni Becas 2025 | 2025 | Jóvenes (título) | El Agustino | Por verificar |
| C3-04 | 3 | La Molina — Molitalleres de verano 2026 | 2026 | Por verificar | La Molina | Por verificar |
| C3-05 | 3 | La Molina — Talleres deportivos de verano 2026 | 2026 | Por verificar | La Molina | Por verificar |
| C3-06 | 3 | La Molina — Moltalleres gratuitos de computación | Por verificar | Niños y jóvenes (título) | La Molina | Por verificar |
| C3-07 | 3 | Lurigancho-Chosica — Talleres Municipales de Verano 2026 | 2026 | Niños y adolescentes | Lurigancho-Chosica | Consultada |
| C3-08 | 3 | Lurigancho-Chosica — Taller arqueológico "Aventureros de Cajamarquilla" | 2026 | Por verificar | Lurigancho-Chosica | Por verificar |
| C3-09 | 3 | San Juan de Lurigancho — FestiJoven 2025 | 2025 | Organizaciones juveniles (título) | San Juan de Lurigancho | Por verificar |
| C3-10 | 3 | Santa Anita — Talleres culturales y deportivos verano 2026 | 2026 | Por verificar | Santa Anita | Por verificar |
| C3-11 | 3 | Santa Anita — Impulsamos el talento de nuestros jóvenes | Por verificar | Jóvenes (título) | Santa Anita | Por verificar |

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
| Cobertura geográfica | No indica. |
| Metodología | Combina varios estudios. No indica la muestra ni el detalle metodológico. |
| Aporte al proyecto | Familia, trabajo, bancarización, ahorro, endeudamiento, entretenimiento y compras. Es el estudio más reciente de la lista. |
| Tipo de información | Estudio de mercado (síntesis de varias encuestas). |
| Formato | PDF de descarga libre (293 KB). |
| Posible método de extracción | Descarga manual del PDF y registro manual. |
| Limitaciones | Cobertura y muestra desconocidas. La definición por año de nacimiento no coincide con el rango de 15 a 30 años. Está orientado al consumo y no cubre temas como cultura, deporte o participación. |

---

## Capa 3 — Evidencia territorial de Lima Este

### Tipos de evidencia

Cada fuente se clasifica según lo que permite afirmar:

| Tipo | Qué significa | Cuándo se registra |
|---|---|---|
| **Oferta** | La actividad existe. | Cuando la fuente la anuncia o la describe. |
| **Participación** | Hay cifras de inscritos, participantes o asistentes. | Solo cuando la fuente publica cifras. |
| **Demanda o interés** | Los jóvenes quieren o buscan la actividad. | Solo con evidencia suficiente: por ejemplo, vacantes agotadas, listas de espera o consultas a jóvenes. **No se infiere del solo hecho de que una municipalidad ofrezca una actividad.** |

| ID | Distrito | Oferta | Participación | Demanda o interés |
|---|---|---|---|---|
| C3-01 | Ate | Sí (título) | Por verificar | Sin evidencia |
| C3-02 | Chaclacayo | Por identificar | — | — |
| C3-03 | El Agustino | Sí (título) | Por verificar | Sin evidencia |
| C3-04 | La Molina | Sí (título) | Por verificar | Sin evidencia |
| C3-05 | La Molina | Sí (título) | Por verificar | Sin evidencia |
| C3-06 | La Molina | Sí (título) | Por verificar | Sin evidencia |
| C3-07 | Lurigancho-Chosica | Sí | **Sí**: más de 1 500 niños y adolescentes, según la municipalidad | Sin evidencia |
| C3-08 | Lurigancho-Chosica | Sí (título) | Por verificar | Sin evidencia |
| C3-09 | San Juan de Lurigancho | Sí (título) | Por verificar | Sin evidencia |
| C3-10 | Santa Anita | Sí (título) | Por verificar | Sin evidencia |
| C3-11 | Santa Anita | Sí (título) | Por verificar | Sin evidencia |

### Consideraciones para toda la capa

- **Método de extracción:** gob.pe rechazó la consulta automatizada (HTTP 418), así que el scraping de esas páginas probablemente no sea viable. Se prevé un registro manual y, más adelante, revisar sus términos de uso. munichosica.pe sí permitió la consulta; su scraping podría evaluarse respetando `robots.txt` y los términos del sitio.
- **Población objetivo:** varios talleres de verano están dirigidos a niños y adolescentes. Hay que verificar en cada caso si incluyen a personas de 15 a 30 años antes de usarlos en el análisis.
- **Cifras de participación:** las publica la propia municipalidad en notas de prensa. Suelen ser aproximadas ("más de") y no están auditadas.
- **Sesgo de visibilidad:** solo se registra lo que las municipalidades publican en internet, y no todas publican con el mismo detalle.

### C3-01 — Ate: Talleres de verano Vacaciones Útiles 2026

| Campo | Valor |
|---|---|
| Distrito | Ate |
| Actividad / programa | Talleres de verano "Vacaciones Útiles 2026" (título) |
| Categoría | Talleres de verano; tipos por verificar |
| Población objetivo / edad | Por verificar. Hay que confirmar si incluye a jóvenes de 15 a 30 años. |
| Fecha | Verano 2026 (título). Fechas exactas por verificar. |
| Lugar | Por verificar |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de Ate |
| Fuente | https://www.gob.pe/institucion/muniate/noticias/1342368-en-ate-inauguran-talleres-de-verano-vacaciones-utiles-2026 |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-02 — Chaclacayo

| Campo | Valor |
|---|---|
| Distrito | Chaclacayo |
| Estado | **Fuente por identificar.** Todavía no se ha verificado una fuente oficial suficientemente útil y reciente. |
| Próximo paso | Buscar publicaciones oficiales de la Municipalidad de Chaclacayo sobre actividades, programas u oportunidades para jóvenes. |

### C3-03 — El Agustino: Muni Becas 2025

| Campo | Valor |
|---|---|
| Distrito | El Agustino |
| Actividad / programa | Muni Becas (título) |
| Categoría | Educación y capacitación (becas) |
| Población objetivo / edad | Juventud (título). Edad y requisitos por verificar. |
| Fecha | 2025 (descripción del equipo). Fecha exacta por verificar. |
| Lugar | Por verificar |
| Costo | Por verificar (tipo o porcentaje de beca) |
| Vacantes | Por verificar |
| Inscritos / beneficiarios | Por verificar |
| Organizador | Municipalidad de El Agustino. Instituciones aliadas por verificar. |
| Fuente | https://www.gob.pe/institucion/munielagustino/noticias/1230858-muni-becas-abre-camino-al-futuro-de-nuestra-juventud |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). Es de 2025; hay que verificar si sigue vigente. |

### C3-04 — La Molina: Molitalleres de verano 2026

| Campo | Valor |
|---|---|
| Distrito | La Molina |
| Actividad / programa | Molitalleres de verano 2026 (título) |
| Categoría | Arte, cultura, tecnología y educación (descripción del equipo) |
| Población objetivo / edad | Por verificar |
| Fecha | Verano 2026. La nota anuncia el cierre de inscripciones (título); fechas por verificar. |
| Lugar | Por verificar |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de La Molina |
| Fuente | https://www.gob.pe/institucion/munilamolina/noticias/1328590-este-viernes-cierran-las-inscripciones-para-los-molitalleres-de-verano-2026 |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-05 — La Molina: Talleres deportivos de verano 2026

| Campo | Valor |
|---|---|
| Distrito | La Molina |
| Actividad / programa | Talleres deportivos de verano 2026 (título) |
| Categoría | Deporte |
| Población objetivo / edad | Por verificar |
| Fecha | Verano 2026. La nota anuncia el inicio de inscripciones (título); fechas por verificar. |
| Lugar | Por verificar |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de La Molina |
| Fuente | https://www.gob.pe/institucion/munilamolina/noticias/1308761-empezaron-las-inscripciones-para-talleres-deportivos-de-verano-2026 |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-06 — La Molina: Moltalleres gratuitos de computación

| Campo | Valor |
|---|---|
| Distrito | La Molina |
| Actividad / programa | Moltalleres de computación (título) |
| Categoría | Tecnología y competencias digitales |
| Población objetivo / edad | Niños y jóvenes (título). Edades por verificar. |
| Fecha | 2026 según la descripción del equipo; por verificar. |
| Lugar | Por verificar |
| Costo | Gratuito (título) |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de La Molina |
| Fuente | https://www.gob.pe/institucion/munilamolina/noticias/1379493-la-molina-lanza-moltalleres-gratuitos-de-computacion-para-ninos-y-jovenes |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-07 — Lurigancho-Chosica: Talleres Municipales de Verano 2026

| Campo | Valor |
|---|---|
| Distrito | Lurigancho-Chosica |
| Actividad / programa | Talleres de Verano 2026 |
| Categoría | Deporte (fútbol, vóleibol, básquetbol, natación) y arte (dibujo, pintura). También un taller de danza para adultos mayores del CIAM, fuera del alcance del proyecto. |
| Población objetivo / edad | "Niños y adolescentes". No indica edades. |
| Fecha | Nota del 12/01/2026 (URL). No indica la duración de los talleres. |
| Lugar | Inauguración en el Coliseo Carmela Estrella. Talleres también en Huampaní, Ñaña, Carapongo, Huachipa, Nievería, Cajamarquilla y Cerro Camote. |
| Costo | No indica |
| Vacantes | No indica |
| Inscritos / participantes | "Más de 700 niños y adolescentes de Chosica" y "más de 800 niños" en otras sedes, en total "más de 1,500 niños y adolescentes". |
| Organizador | Municipalidad de Lurigancho-Chosica |
| Fuente | https://munichosica.pe/2026/01/12/inauguracion-de-talleres-municipales-de-verano-2026/ |
| Tipo de información | Publicación municipal (nota en el sitio web propio) |
| Tipo de evidencia | Oferta y participación |
| Posible método de extracción | Registro manual. El sitio permitió la consulta, así que podría evaluarse el scraping (revisar `robots.txt` y términos). |
| Limitaciones | Está dirigido a niños y adolescentes: no se sabe cuántos participantes tienen entre 15 y 30 años. Las cifras son aproximadas y declaradas por la municipalidad. |

### C3-08 — Lurigancho-Chosica: Taller de verano arqueológico "Aventureros de Cajamarquilla"

| Campo | Valor |
|---|---|
| Distrito | Lurigancho-Chosica |
| Actividad / programa | Taller de verano arqueológico "Aventureros de Cajamarquilla" (título) |
| Categoría | Cultura y patrimonio (título) |
| Población objetivo / edad | Por verificar |
| Fecha | Verano 2026 (descripción del equipo). Fechas por verificar. |
| Lugar | Cajamarquilla (título). Sede exacta por verificar. |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de Lurigancho-Chosica. Aliados por verificar. |
| Fuente | https://www.gob.pe/institucion/munilurigancho/noticias/1329207-iniciamos-el-taller-de-verano-arqueologico-aventureros-de-cajamarquilla |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-09 — San Juan de Lurigancho: FestiJoven 2025

| Campo | Valor |
|---|---|
| Distrito | San Juan de Lurigancho |
| Actividad / programa | FestiJoven (título) |
| Categoría | Participación juvenil y organizaciones juveniles |
| Población objetivo / edad | Organizaciones juveniles de San Juan de Lurigancho (título). Edades por verificar. |
| Fecha | 2025 (descripción del equipo). Fecha exacta por verificar. |
| Lugar | Play Park (título). Dirección por verificar. |
| Costo | Por verificar |
| Vacantes | No aplica (evento) |
| Inscritos / asistentes | Por verificar (número de organizaciones y de asistentes) |
| Organizador | Municipalidad de San Juan de Lurigancho |
| Fuente | https://www.gob.pe/institucion/munisanjuandelurigancho/noticias/1255171-festijoven-reune-a-las-organizaciones-juveniles-de-san-juan-de-lurigancho-en-el-play-park |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual. Puede cruzarse con el RENOJ de Dato Joven (C1-01), que tiene organizaciones juveniles por distrito. |
| Limitaciones | Página no consultada (HTTP 418). Es un evento puntual de 2025. |

### C3-10 — Santa Anita: Talleres culturales y deportivos verano 2026

| Campo | Valor |
|---|---|
| Distrito | Santa Anita |
| Actividad / programa | Talleres culturales y deportivos verano 2026 (título) |
| Categoría | Cultura y deporte |
| Población objetivo / edad | Por verificar |
| Fecha | Verano 2026 (título). Fechas por verificar. |
| Lugar | Por verificar |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de Santa Anita |
| Fuente | https://www.gob.pe/institucion/munisantanita/noticias/1343996-inician-los-talleres-culturales-y-deportivos-verano-2026 |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). |

### C3-11 — Santa Anita: Impulsamos el talento de nuestros jóvenes

| Campo | Valor |
|---|---|
| Distrito | Santa Anita |
| Actividad / programa | Por verificar. El título es "Impulsamos el talento de nuestros jóvenes". |
| Categoría | Actividades y oportunidades educativas (descripción del equipo) |
| Población objetivo / edad | Jóvenes (título). Edades por verificar. |
| Fecha | Por verificar |
| Lugar | Por verificar |
| Costo | Por verificar |
| Vacantes | Por verificar |
| Inscritos / participantes | Por verificar |
| Organizador | Municipalidad de Santa Anita. Aliados por verificar. |
| Fuente | https://www.gob.pe/institucion/munisantanita/noticias/1377405-impulsamos-el-talento-de-nuestros-jovenes |
| Tipo de información | Publicación municipal (nota de prensa) |
| Tipo de evidencia | Oferta |
| Posible método de extracción | Registro manual |
| Limitaciones | Página no consultada (HTTP 418). El contenido concreto se desconoce. |

---

## Integración de las capas

Se mantiene el modelo metodológico del `README.md`:

**necesidades y contexto (Capa 1) + intereses y aspiraciones (Capa 2) + evidencia territorial: oferta y participación (Capa 3) → identificación posterior de coincidencias, brechas e hipótesis de oportunidades.**

### Cobertura temática preliminar

La siguiente tabla muestra qué fuentes tratan cada tema, según lo que describen las páginas y, en C1-01 y C1-02, según la exploración técnica. **No son resultados**: sirve para ver qué temas tienen fuentes en las tres capas y cuáles no.

| Tema | Capa 1 | Capa 2 | Capa 3 |
|---|---|---|---|
| Educación y capacitación | C1-02, C1-03 | Por verificar | C3-03, C3-04, C3-11 |
| Empleo | C1-02, C1-03 | C2-01, C2-03, C2-04 | — |
| Emprendimiento | C1-03 | Por verificar | — |
| Tecnología y competencias digitales | C1-02, C1-03 | C2-01, C2-02 | C3-04, C3-06 |
| Cultura y arte | C1-02 (trabajadores del sector cultural, solo por departamento) | Por verificar | C3-04, C3-07, C3-08, C3-10 |
| Deporte | C1-02 (atletas del IPD, sin distrito) | Por verificar | C3-05, C3-07, C3-10 |
| Entretenimiento y uso del tiempo | C1-03 | C2-02, C2-03, C2-04 | — |
| Consumo y finanzas | — | C2-01, C2-04 | — |
| Salud | C1-02, C1-03 | — | — |
| Seguridad, violencia y discriminación | C1-02, C1-03 | — | — |
| Participación y organizaciones juveniles | C1-01, C1-02, C1-03 | — | C3-09 |
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

- [ ] **No hay fuentes posteriores a 2022.** Buscar estudios recientes sobre intereses y hábitos de jóvenes, por ejemplo los documentos de 2024–2026 de Biblio Joven u otras fuentes confiables.
- [ ] **El tramo de 21 a 30 años casi no está cubierto:** dos estudios llegan solo hasta los 20 años y el de 2022 se centra en los 18 a 25.
- [ ] Revisar los PDF para confirmar qué variables contienen. En particular, falta confirmar cultura, deporte, emprendimiento, aspiraciones y educación y capacitación.
- [ ] Averiguar la cobertura geográfica y la muestra de C2-04, y la lista de ciudades de C2-03.
- [ ] Averiguar la fecha del trabajo de campo de C2-01.
- [ ] Verificar si algún estudio presenta resultados por separado para Lima.

### Capa 3

- [ ] **Revisar manualmente las 9 notas de gob.pe** (C3-01, C3-03 a C3-06, C3-08 a C3-11). Ninguna pudo consultarse, así que todos sus campos, salvo los del título, están por verificar.
- [ ] **Identificar una fuente oficial para Chaclacayo** (C3-02).
- [ ] Verificar si cada actividad incluye a personas de 15 a 30 años. Varios talleres de verano parecen dirigidos a niños y adolescentes.
- [ ] Buscar cifras de participación. Por ahora solo C3-07 tiene cifras, y corresponden a niños y adolescentes.
- [ ] Buscar oferta en los temas que no tienen fuentes en esta capa: empleo, emprendimiento, salud (incluida la salud mental) y seguridad.
- [ ] Buscar evidencia de demanda o interés (vacantes agotadas, listas de espera, consultas a jóvenes). Por ahora no hay ninguna.
- [ ] Evaluar la viabilidad y las condiciones de uso del scraping, considerando que gob.pe bloquea la consulta automatizada.
