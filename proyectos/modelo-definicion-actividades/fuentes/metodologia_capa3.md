# Metodología de la Capa 3

Registro de fuentes, procesos, decisiones y limitaciones de la Capa 3 (evidencia territorial: oferta de
actividades para jóvenes en los siete distritos de Lima Este y evidencia de participación o demanda).
Complementa `fuentes.md` (catálogo) y `data/README.md` (diccionario de datos).

- **Fecha:** 25/09/2026.
- **Periodo cubierto:** enero de 2024 a septiembre de 2026.
- **Producto principal:** `fuentes/capa3_registro_oferta.csv`, una fila por actividad, programa, evento,
  servicio o espacio, codificada a mano.
- **Análisis:** `notebooks/03_capa3_oferta.ipynb`.

## 1. Qué mide y qué no mide esta capa

| Tipo de evidencia | Qué permite afirmar | Cuándo se registra |
|---|---|---|
| **Oferta** | La actividad se ofreció o se realizó. | La fuente la anuncia o la describe. |
| **Participación declarada** | Hubo inscritos, asistentes, participantes o egresados, según quien organiza. | La fuente publica una cifra o una mención explícita de participantes. |
| **Demanda observada** | Hubo más interesados que cupos. | Solo con una señal concreta: inscripciones agotadas, inscritos por encima del cupo previsto, lista de espera, ampliación de vacantes por la demanda. |

Reglas:

- **Que una actividad exista no prueba que interese a los jóvenes.** La oferta refleja las decisiones de quien
  organiza.
- **Las cifras son declaradas** por quien organiza, en notas de prensa. Suelen ser aproximadas ("más de") y no
  están auditadas. Se registran como aparecen.
- **No toda cifra es participación.** Los cupos o vacantes, el aforo de un espacio, la asistencia *prevista* y la
  población que "se beneficiará" de una obra describen la oferta, no la participación. Se registran en
  `cifra_tipo` y la fila queda como oferta.
- **Una cifra solo describe a los jóvenes si se refiere a ellos.** Si cuenta a "niños y adolescentes" o al
  "público", se registra con esa población (`cifra_poblacion`) y no se atribuye a los jóvenes de 15 a 29 años.
- **Expresiones como "gran acogida" o "masiva participación"** no son evidencia de demanda.

## 2. Fuentes

| Fuente | Qué cubre | Cómo se obtuvo | Verificación |
|---|---|---|---|
| **Notas de prensa de las siete municipalidades en gob.pe** | Las siete municipalidades | `scripts/capa3_noticias_gobpe.py`: búsqueda por términos, enero de 2024 a septiembre de 2026 | Texto completo |
| **munichosica.pe** (sitio de Lurigancho-Chosica) | Lurigancho-Chosica | `scripts/capa3_noticias_wp.py` (API de WordPress) | Texto completo |
| **SERPAR** (clubes metropolitanos Wiracocha, en SJL; Cahuide y Huaycán, en Ate) | Oferta de la Municipalidad de Lima en Lima Este | `scripts/capa3_noticias_wp.py` | Texto completo |
| **SENAJU** (juventud.gob.pe) | Actividades nacionales con sede en Lima Este | `scripts/capa3_noticias_wp.py`, buscando nombres de distritos | Texto completo |
| **Notas en gob.pe del MTPE, IPD, Ministerio de Cultura, DEVIDA y Municipalidad de Lima** | Oferta nacional y metropolitana en los siete distritos | `scripts/capa3_noticias_gobpe.py sectores`, buscando nombres de distritos | Texto completo |
| **Prensa y buscador web** | Vacíos de las fuentes anteriores | Búsqueda manual | Texto completo cuando el artículo pudo leerse; si no, resumen del buscador |

Todas las consultas respetan el `robots.txt` de cada sitio, se identifican con un agente de usuario propio
("ORP-juventudLimaEste") y esperan entre 2 y 10 segundos entre consultas según el sitio. En gob.pe, cuyo
`robots.txt` prohíbe paginar resultados (`sheet=`), cada búsqueda pide hasta 100 resultados en una sola
página; si hay más, se divide el rango de fechas.

**Fuentes revisadas y descartadas:**

- **Directorio de Puntos de Cultura (Ministerio de Cultura):** no indica el distrito de cada organización y su
  uso está sujeto a la Ley de Protección de Datos Personales.
- **datosabiertos.gob.pe:** rechazó la consulta automatizada (HTTP 418). No se intentó eludir el bloqueo.
- **Sitios propios de las municipalidades de Ate, El Agustino, Chaclacayo, San Juan de Lurigancho y Santa
  Anita:** no respondieron, rechazaron la consulta (HTTP 403) o redirigen a gob.pe. La página del "Área de
  Juventudes" de Ate existe, pero también rechaza la consulta (403); no se intentó eludir el bloqueo.
- **Sitio de La Molina (portal.munimolina.gob.pe):** responde, pero repite las notas que la municipalidad publica
  en gob.pe; no se usó para no duplicar.

## 3. Proceso

```
scripts/capa3_noticias_gobpe.py listar            → data/raw/capa3/gobpe_listado.csv
scripts/capa3_noticias_gobpe.py detalle           → data/raw/capa3/noticias_gobpe.csv
scripts/capa3_noticias_gobpe.py sectores          → data/raw/capa3/gobpe_sectores_listado.csv
scripts/capa3_noticias_gobpe.py detalle_sectores  → data/raw/capa3/noticias_gobpe_sectores.csv
scripts/capa3_noticias_wp.py                      → data/raw/capa3/noticias_{munichosica,serpar,senaju}.csv
scripts/capa3_triaje.py                           → data/processed/capa3_notas_candidatas.csv
(codificación manual)                             → fuentes/capa3_registro_oferta.csv
scripts/capa3_validar_registro.py                 → revisa listas cerradas y reglas de evidencia
notebooks/03_capa3_oferta.ipynb                   → resúmenes por distrito, tema, edad, costo y evidencia
```

| Paso | Resultado (consulta del 25/09/2026) |
|---|---|
| Notas municipales en gob.pe que coinciden con la búsqueda | 1 304 (Ate 150, Chaclacayo 6, El Agustino 408, La Molina 201, Lurigancho-Chosica 72, SJL 225, Santa Anita 242) |
| Notas municipales descargadas (términos sobre juventud o títulos de empleo, becas y cursos gratuitos) | 555 |
| Notas de entidades nacionales y de la Municipalidad de Lima que mencionan los distritos | 483 (IPD 135, Municipalidad de Lima 190, Ministerio de Cultura 92, MTPE 48, DEVIDA 18) |
| Notas de munichosica.pe, SERPAR y SENAJU | 69, 57 y 19 |
| Notas revisadas por el triaje / candidatas | 1 183 / 589 |
| **Actividades registradas** | **150**: 88 con evidencia de oferta, 58 con participación declarada y 4 con demanda observada |

La codificación se hizo leyendo las notas candidatas y, en los distritos con notas breves, también el inicio de
las demás notas descargadas (C3-D6). La fecha de consulta de cada fila está en `fecha_consulta`.

## 4. Decisiones metodológicas

| ID | Decisión | Motivo |
|---|---|---|
| C3-D1 | La unidad del registro es la **actividad**, no la nota. Si varias notas tratan la misma actividad (anuncio, inauguración, cierre) o sus ediciones anuales, van en una sola fila con todas sus fuentes. Los espacios deportivos nuevos o renovados se agrupan en una fila por distrito. | Evitar que las actividades más difundidas, o las obras que se inauguran una por una, pesen más en los conteos. |
| C3-D2 | **Regla de inclusión.** Se registra: (a) toda oferta dirigida a jóvenes, adolescentes o estudiantes; (b) talleres, cursos, competencias, voluntariados, ferias laborales y servicios abiertos a todas las edades cuando la fuente menciona explícitamente a los jóvenes, o cuando tratan de empleo, becas o cursos gratuitos para el público general; (c) eventos masivos (festivales, ferias culturales) solo si la fuente menciona a jóvenes o estudiantes como público o participantes; (d) espacios (centros culturales, complejos deportivos, bibliotecas) descritos para jóvenes o que acogen actividades registradas. Se excluyen ceremonias cívicas y desfiles, matrimonios, notas de gestión, obras sin mención de uso juvenil y actividades solo para niños pequeños o adultos mayores (salvo una, fuera de rango, que se conserva como referencia de demanda). | El registro debe describir la oferta relevante para jóvenes sin inflarse con toda la agenda municipal. La regla se aplica igual en los siete distritos. |
| C3-D3 | El campo `incluye_15_29` distingue la oferta dirigida a jóvenes (`juventud`), la que mezcla niños y adolescentes o "niños y jóvenes" (`adolescentes`), la abierta a todo público y la que queda fuera del rango (`no`). | Los talleres "para niños y adolescentes" suelen incluir a personas de 15 a 17 años. Excluirlos borraría buena parte de la oferta municipal; mezclarlos sin marcarlos la sobreestimaría. |
| C3-D4 | `ambito` describe **a quién está abierta la actividad**, no quién la organiza: `distrital` (vecinos o colegios del distrito), `metropolitano` (cualquier persona de Lima) o `nacional` (todo el país, aunque tenga sede en Lima Este). El organizador está en `tipo_organizador`. | Una actividad de SENAJU en un colegio de SJL es oferta local; un encuentro nacional en Huampaní no lo es. |
| C3-D5 | Solo se descarga el texto de las notas de gob.pe que la búsqueda devolvió con términos sobre juventud (jóvenes, juventud, juvenil, adolescentes, estudiantes, escolares, vacaciones útiles, orientación vocacional, preuniversitaria) o cuyo título trata de empleo, becas o cursos gratuitos. | Las demás no pueden cumplir la regla de inclusión. Reduce a menos de la mitad las consultas al servidor. |
| C3-D6 | El triaje automático solo selecciona notas y extrae fragmentos; **toda clasificación es manual**. Además, se revisaron los títulos y el inicio de las notas descargadas que el triaje no marcó. | Las palabras clave no distinguen entre una actividad y una mención de paso, y algunas notas son de una o dos líneas. La revisión encontró actividades que el triaje no marcaba (juegos florales, brigadas escolares, un consejo consultivo); se ampliaron los términos. |
| C3-D7 | En las entidades nacionales y metropolitanas (C3-05), "Ate" se busca como la frase "distrito de Ate", además de Vitarte y Huaycán. | La búsqueda de gob.pe encontraba "Ate" dentro de otras palabras: devolvía más de 1 000 notas ajenas al distrito. |
| C3-D8 | Periodo: enero de 2024 a septiembre de 2026. | "Reciente" dentro del periodo prioritario 2022–2026. |

## 5. Limitaciones

- **Sesgo de visibilidad:** solo se registra lo que se publica en internet. Las municipalidades publican con
  distinta frecuencia y detalle, así que las diferencias entre distritos en el número de actividades reflejan en
  parte cuánto comunica cada una. **El registro no es un censo de la oferta.**
- **Oferta no municipal:** las organizaciones sociales, parroquias, ONG, academias privadas y colectivos
  culturales casi no aparecen, porque no hay una fuente sistemática para ellos.
- **Cifras declaradas y no comparables:** cada fuente cuenta algo distinto (inscritos, asistentes, egresados) y
  con distinto rigor. No se suman ni se comparan entre distritos.
- **La demanda casi no se observa:** las notas rara vez informan de cupos y de inscritos a la vez. Solo 4
  actividades tienen una señal de demanda, y dos de ellas se miden para toda Lima Metropolitana.
- **Cobertura desigual en el tiempo:** San Juan de Lurigancho casi no publicó en gob.pe en 2024 (1 nota; su sitio
  anterior ya no está disponible) y La Molina publicó poco ese año (30 notas). Su oferta de 2024 está
  subrepresentada.
- **Notas muy breves:** El Agustino y Santa Anita publican notas de una o dos líneas, con poca información sobre
  edades, costos y participantes.
- **Chaclacayo:** 6 notas en gob.pe en casi tres años. Sus 3 actividades registradas son un taller de verano
  municipal (2024), un concierto del Ministerio de Cultura y un voluntariado de SENAJU en un CEDIF. Entre sus
  demás notas, una carrera ciclística (2024) no menciona a los jóvenes y no cumple la regla de inclusión.
- **Resúmenes de buscador:** dos datos de prensa (ferias laborales con Mall Aventura en SJL y más de 800 vacantes en
  una maratón del empleo de El Agustino) se citan en `notas` solo como referencia, porque no se pudieron leer.

## 6. Pendientes

- Buscar oferta de **organizaciones sociales, ONG y colectivos** (por ejemplo, Puntos de Cultura de Lima Este) con
  una fuente que permita identificar el distrito, o mediante consulta directa.
- Pedir a las municipalidades, sobre todo **Chaclacayo, Ate y San Juan de Lurigancho (2024)**, información sobre
  su oferta para jóvenes y sus cifras de inscritos y cupos, para compensar el sesgo de visibilidad.
- Para observar **demanda**, recoger cupos e inscritos de las mismas actividades (listas de espera, vacantes
  agotadas) o consultar directamente a jóvenes.
