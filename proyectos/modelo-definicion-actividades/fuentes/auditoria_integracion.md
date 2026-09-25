# Auditoría metodológica de la integración de las tres capas

- **Fecha:** 25/09/2026.
- **Estado:** diagnóstico para revisión del equipo.
- **Qué no se modificó:** `propuestas.csv`, `hallazgos_integrados.csv`, `patrones.csv`, el informe final y el
  observatorio siguen sin cambios. La reconstrucción empezará después de la revisión del equipo.
- **Qué se revisó:**
  - las metodologías de las Capas 1, 2 y 3 y de la integración;
  - los 49 hallazgos, los 12 patrones y las 11 propuestas;
  - el informe final;
  - los datasets procesados;
  - el registro de oferta;
  - los microdatos del INEI ya descargados.
- **Cálculos nuevos:** `scripts/auditoria_factibilidad_enaho.py` (solo imprime; no escribe en `data/processed/`).
  - Cruza los Módulos 03 y 05 de la ENAHO 2022–2025 para comprobar qué denominadores de Lima Este son
    estimables.
  - Las cifras de la sección 5 marcadas **(prelim.)** salen de ese script. Son **cálculos propios
    preliminares**: prueban que el denominador existe y dan su orden de magnitud. Todavía **no están
    validados** contra Dato Joven (sección 5.3).
  - Las demás cifras nuevas se leen directamente de `data/processed/`. Las comparaciones Lima Este frente a
    Lima Metropolitana usan una prueba z aproximada, como la regla D9.

---

## Resumen

1. **Ninguna de las 11 propuestas se sostiene tal como está formulada.** La mayoría responde a algo real, pero
   varias agrupan componentes con evidencia muy distinta. Además, eligen segmentos que los datos no respaldan
   y califican con "alto" un interés que en realidad es una práctica relacionada.
   - Resultado preliminar: 0 se confirman (A), 9 se reformulan (B; P06 pierde además dos componentes) y 2 se
     descartan como actividad (C).
   - Hay alternativas y segmentos que la primera integración omitió.
2. **La escala alto/medio/bajo no es comparable entre propuestas.** Cada nivel mezcla cuatro cosas distintas:
   - el ámbito geográfico (Lima Este o Lima Metropolitana);
   - la cercanía entre el indicador y la actividad;
   - la precisión estadística;
   - el tipo de evidencia.

   Además, "bajo" en convocatoria se lee como "convoca poco", cuando casi siempre significa "casi no hay datos".
3. **Hay un error de población en un hallazgo central.** Los motivos para no estudiar ("31 % trabaja, 28 %
   problemas económicos, 2 % falta de interés") son de jóvenes de **15–24 años** que no asisten: la ENAHO no
   hace esa pregunta a mayores de 24. Se citan como "quienes no estudian en Lima Este" (15–29). Afecta a H2-12,
   PT-01, P01, P02 y al resumen del informe.
4. **La integración no aprovechó datos que ya teníamos.** Con los microdatos descargados se puede estimar para
   **Lima Este** la situación de estudio y trabajo, la búsqueda de empleo, la informalidad (2022–2023), el
   trabajo independiente y la población compatible con la preparación preuniversitaria. Estas estimaciones
   cambian el diagnóstico de P01, P02 y P09.
   - **Ejemplo P02:** entre los jóvenes de Lima Este que no estudian ni trabajan, solo **~1 de cada 5 busca
     trabajo**. Entre las mujeres de ese grupo, **~6 de cada 10 se dedica a los quehaceres del hogar**
     (prelim.). Eso contradice que P02 priorice a "mujeres NINI" para un taller de empleabilidad.
5. **Los denominadores de población no están reconciliados.**
   - Dato Joven (REUNIS/INEI) da **712 mil** jóvenes en 2026.
   - La expansión de la ENAHO da **778–908 mil** en 2022–2025.
   - Cualquier conversión de porcentajes a personas debe darse como **rango** y con ambas bases.
6. **Hay saltos inferenciales sistemáticos.** Los principales son:
   - de práctica a interés por una actividad organizada (cine → cineforo; deporte → liga);
   - de consumo a producción (ver video → taller de video);
   - de "no mencionó falta de interés" a "tiene interés";
   - de problema existente a "esta actividad lo resuelve" (por ejemplo, de informalidad a emprendimiento).
7. **El informe final ordena las propuestas de hecho**, aunque la metodología lo prohíbe: "las más
   respaldadas son…", "las mejores candidatas para pilotos…".
8. **Lo que está bien construido se conserva.** Se mantienen:
   - la separación de niveles geográficos;
   - las reglas de CV y la estimación de Lima Este como dominio no planificado;
   - la tipología oferta / participación / demanda de la Capa 3;
   - las reglas I-R1 a I-R7;
   - los códigos de trazabilidad y el campo "qué no permite".
9. **Propuesta de reemplazo** (sección 8): una ficha por actividad y segmento con la cadena
   contexto → población → interés → alcance → oferta → convocatoria → barreras → vacíos → afirmaciones →
   hipótesis.
   - Cada eslabón se apoya en registros de evidencia atómicos, con categorías descriptivas y reglas escritas.
   - No lleva puntaje ni orden.

---

## 1. Problemas encontrados en la integración actual

### 1.1 Errores de dato, de población o de lectura

| # | Dónde | Problema | Evidencia | Corrección necesaria |
|---|---|---|---|---|
| E1 | H2-12, PT-01, P01, P02, informe (resumen y §2) | Los motivos para no estudiar se atribuyen a "quienes no estudian en Lima Este" (15–29). La pregunta (p313/t313a) **solo se hace hasta los 24 años**. | En la muestra 2022–2025, las personas de 25–29 con motivo registrado son 6 frente a más de 36 mil de 15–24 (salida 7 del script). En `capa2_educacion_internet_enaho.csv`, `n_muestral` de 25–29 es 0. | Citar como "jóvenes de 15–24 que no asisten". Recalcular cualquier cifra derivada. |
| E2 | H2-12, PT-01, P01 | "La falta de interés es mínima (2,1 %)" se lee como evidencia de interés por estudiar. | Es un motivo principal de respuesta única, referencial, y puede estar subdeclarado. Además, 16,7 % responde "terminó sus estudios o asiste a academia preuniversitaria", una categoría del INEI que mezcla dos situaciones opuestas. | Registrar que **no sabemos** cuántos quieren continuar estudios ni cuántos ya están en academias. |
| E3 | H1-02 | "Ninguna [organización] tiene como temática … la participación y ciudadanía." | El 48 % de las organizaciones (87 de 182) está en la categoría agrupada "Otros". Dentro de ella hay 7 de "Democracia y Derechos Humanos", 2 de ética y anticorrupción y **18 de ciencia, tecnología y TIC**. | Corregir el enunciado. Usar `tematica_1`. La ausencia de temática deportiva sí se mantiene. |
| E4 | H1-08 | La precisión figura como "confiable". | El 10,3 % de los hombres es **referencial** (CV > 15). | Marcarlo como referencial. |
| E5 | H2-04, P10 | "Hacer voluntariado o ayudar a la comunidad (9,0 %)" se usa como práctica de voluntariado. | La categoría de la ENUT es "Voluntariado y ayuda a la comunidad **u otros hogares**": incluye ayudar a familiares o vecinos. También es referencial. | Tratarla como proxy amplio, no como voluntariado. |
| E6 | H2-09 | Dice que no permite "barreras en Lima Este por separado". | Las barreras de Lima Este existen y son confiables en los ítems principales (por ejemplo, dinero en conciertos 21,2 %, falta de tiempo en cine 31,6 %). P06 ya usa una (18,8 %). | Usar las barreras de Lima Este donde sean publicables. |
| E7 | PT-02 | "Más de dos tercios tienen 20–29 años **y practican** deporte, cultura y actividades digitales." | La práctica se midió para 15–29, no para 20–29. En deporte, solo el 27,6 % practica cada semana. | Separar el dato de edad del dato de práctica. |
| E8 | PT-03, informe | "El deporte es una de las prácticas juveniles más extendidas." | Uno de cada cuatro (27,6 %). La diferencia con Lima Metropolitana (34,8 %) **no es distinguible** (z ≈ −1,7). | Enunciar la magnitud sin adjetivos. |
| E9 | PT-06 | Las mujeres tienen "mucha menos práctica deportiva y de juegos", leído como un rasgo general. | En cultura, las mujeres de Lima Este participan igual o más: espectáculos en vivo 47,2 % frente a 41,7 %; cine 66,6 % frente a 59,3 %. | Acotar la brecha a deporte y videojuegos. |
| E10 | H1-06, P02, P09 | La informalidad se cita solo para Lima Metropolitana (65,1 %, 2023). | Para Lima Este se puede estimar la de 2022–2023: **70,0 % de los ocupados** (CV 3,1) (prelim.). | Incorporarla con su periodo. |
| E11 | Informe (resumen) | "Las más respaldadas son…" y "las mejores candidatas para pilotos…". | Es un orden implícito, contrario a la metodología (sección 3) y al pedido del equipo. | Eliminarlo. |
| E12 | H1-01 y cualquier conversión a personas | Se usa 712 mil como un dato cierto. | La ENAHO expande la población joven de Lima Este a 778–908 mil (2022–2025). La serie REUNIS ya era inestable (D5). | Presentar rangos con ambas bases (sección 5.3). |
| E13 | H2-11 | "43 % entre 20 y 24 años" junto a valores agrupados 2022–2025. | Es el valor de Lima Este de **un solo año** (2024). El agrupado de 20–24 es 38,3 %. | No mezclar periodos en un mismo enunciado. |

### 1.2 La escala alto / medio / bajo / sin evidencia

La rúbrica (`metodologia_integracion.md` §3) tiene reglas escritas, lo cual es positivo, pero:

- **Mezcla dimensiones heterogéneas en un solo nivel.**
  - En interés, "alto" exige a la vez "la misma práctica", "Lima Este" y "confiable".
  - "Medio" acepta cualquiera de tres condiciones distintas (práctica relacionada, *o* solo Lima
    Metropolitana, *o* referencial).
  - Así, dos propuestas "medio" pueden estar en situaciones opuestas: una con el indicador exacto pero de
    Lima Metropolitana, y otra con un indicador lejano pero de Lima Este.
- **Se aplicó con laxitud en "la misma práctica o actividad".**
  - P04: ir a hacer deporte no es jugar en una liga organizada.
  - P05: ir a un concierto, casi siempre pagado, no es ir a un escenario gratuito de cultura urbana.
  - P06: ir al cine comercial no es ir a un cineforo con conversación.

  Las tres recibieron "alto" en interés, pero son **prácticas relacionadas**. Con la propia rúbrica les
  corresponde "medio".
- **Se asignó interés sin evidencia de interés.** P08 tiene "bajo" citando H2-02 (práctica deportiva) y H2-05
  (satisfacción con el tiempo para amistades). Ninguno de los dos informa sobre interés en espacios de
  bienestar. Corresponde "sin evidencia".
- **"Bajo" en convocatoria confunde falta de datos con baja convocatoria.** P04 recibe "bajo" porque solo hay
  un taller de 30 alumnos y carreras para todas las edades. Eso no indica que el deporte para 18–29 convoque
  poco: indica que no lo sabemos. **No existe en el análisis ningún caso de evidencia de baja convocatoria**
  (cupos sin llenar, actividades canceladas), y la escala no tiene cómo registrarlo.
- **"Necesidad" mezcla tres cosas que no son lo mismo:**
  - prevalencia medida en encuestas (P08: episodio depresivo);
  - registros de atención que dependen del acceso a servicios (P11: nacimientos y casos de los CEM);
  - objetivos institucionales (P10: "la participación organizada es baja" es un problema para la
    organización, no una necesidad declarada ni medida en los jóvenes).

  La rúbrica permite "alto" con un registro distrital, cuando la propia Capa 1 establece que los registros no
  miden prevalencia.
- **La magnitud no aparece en ninguna parte.** Una necesidad de 1–2 % de las adolescentes y una de un tercio de
  los jóvenes pueden recibir el mismo "alto". La escala no dice a cuántas personas se aplica cada cosa.

### 1.3 Segmentación

- **Algunos segmentos se eligieron sin datos que los respalden.** P03, P05, P06 y P07 se dirigen a 15–24, pero
  los datos culturales de Lima Este procesados solo existen para 15–29 y por sexo. Ninguna cifra de esas
  propuestas es de 15–24.
- **Otros segmentos contradicen la evidencia disponible.**
  - P02 prioriza a las "mujeres que no estudian ni trabajan" para un taller de empleabilidad.
  - En Lima Este, el 62 % de esas mujeres se dedica a los quehaceres del hogar y solo el 19 % busca trabajo
    (prelim.).
  - Para la mayoría de ese grupo, el problema no es prepararse para buscar empleo.
- **No se usaron segmentos de Lima Este ya disponibles**, como sexo en la ENAPRES o edad en la ENAHO y la ENUT.
  En su lugar se tomaron brechas de Lima Metropolitana. Ejemplo: P07 usa "aficiones: 27 % hombres, 9 % mujeres
  (Lima Metropolitana)", pero existe el dato de Lima Este: videojuegos multijugador, 52,8 % de hombres y 18,9 %
  de mujeres.
- **Nunca se conectó un porcentaje con la población que representa.** Por eso no se distingue una necesidad
  intensa en un grupo pequeño de una señal moderada en un grupo grande.

### 1.4 Construcción de las propuestas

- **Propuestas compuestas.** Varias agrupan componentes con evidencia distinta, y la evidencia de uno se
  transfiere al conjunto:
  - P01: preparación + orientación + becas;
  - P04: liga + entrenamiento + opción femenina;
  - P06: proyección + conversación + taller de video;
  - P07: torneo + habilidades digitales + inclusión de mujeres.
- **Condiciones de diseño sin datos.** Algunas recomendaciones de diseño no tienen datos que las sostengan:
  - PT-08: "fines de semana, cerca de casa";
  - P05: "evitar patrocinio de alcohol";
  - P03: "garantizar acceso a equipos".

  No se midieron horarios, distancias ni consumo de alcohol en eventos. El dato de alcohol en los últimos 30
  días existe (ENDES, Lima Metropolitana, 37,2 %) pero no se usó.
- **Los patrones se leyeron como hallazgos más fuertes.** Por ejemplo, PT-01 dice "la barrera no es el
  interés", una conclusión que la evidencia no alcanza (E1, E2).

---

## 2. Dimensiones bien construidas (se conservan)

| Dimensión | Por qué está bien |
|---|---|
| Niveles geográficos (D3, I-R5) | Cada hallazgo tiene `geografia`. Lima Este solo se usa para estimaciones del dominio o sumas distritales. |
| Precisión (D6, C2-D1) | Hay umbrales de CV explícitos, errores estándar por linealización y validaciones con Dato Joven (32 de 32 dentro de ±1 punto en empleo; ≤ 1 punto en educación e internet). |
| Tipología de la Capa 3 | Oferta / participación declarada / demanda observada, más C3-D9: la demanda es solo por la oferta concreta. El marcador de adolescentes está aplicado. |
| Reglas I-R1 a I-R7 | Son correctas y se respetaron en los enunciados de los hallazgos. |
| Trazabilidad | Códigos H1/H2/H3, PT, P y C3-###, con verificación automática en el notebook 04. |
| Campo "qué no permite" | Es buena práctica; varios problemas de la sección 1 están anticipados ahí, pero no se trasladaron a los niveles. |
| Datos sensibles (D12) | Celdas menores de 10 ocultas, con ocultación complementaria. |
| Sin puntaje total | Las tres dimensiones nunca se suman. |
| Cautelas por propuesta | Casi siempre identifican el salto; el problema es que el nivel asignado no lo refleja. |

---

## 3. Dimensiones que necesitan redefinirse

| Dimensión | Hoy | Debe distinguir |
|---|---|---|
| **Necesidad** | Un nivel ordinal. | (a) si existe; (b) **tipo**: prevalencia en población, registro de atención, brecha de acceso u objetivo institucional; (c) **población afectada** y magnitud, en % y en personas, o "no estimable"; (d) ámbito y año. |
| **Interés o práctica** | Un nivel ordinal. | La **distancia inferencial** entre lo medido y la actividad (sección 8.3): práctica relacionada, práctica de la misma actividad, interés declarado en el tema, interés en participar en la actividad propuesta. Hoy las fuentes casi nunca pasan del primer o segundo peldaño. |
| **Convocatoria** | Un nivel ordinal. | Sin evidencia, solo oferta, participación declarada (con o sin cifra y segmento compatible), demanda observada y **evidencia de baja convocatoria**. Además, la **comparabilidad** con la actividad propuesta (segmento, territorio, formato, costo) y si la cifra está verificada o es declarada. |
| **Alcance potencial** | No existe. | Nueva dimensión con denominadores: pertinencia amplia, segmento identificable (con tamaño) o alcance desconocido. |
| **Barreras** | Texto libre por propuesta. | Registro por barrera: dónde se midió, para qué actividad y en qué segmento. Distinguir **barrera medida** de **condición de diseño supuesta**. |
| **Segmento** | Texto libre. | Campos explícitos: edad, sexo, situación educativa, situación laboral, ámbito y otros. Cada segmento con su denominador. |
| **Unidad "propuesta"** | Un paquete de componentes. | Un **componente evaluable** por ficha, o componentes evaluados por separado dentro de ella. |

---

## 4. Datos que no se están aprovechando

### Ya procesados en `data/processed/`

- **ENAPRES 2022–2025, Lima Este por sexo** (confiable en la mayoría de los ítems).
  - Videojuegos, hombres frente a mujeres: 60,9 % y 33,6 % en el celular; 52,8 % y 18,9 % en línea.
  - Cine, mujeres frente a hombres: 66,6 % y 59,3 %.
  - Revistas digitales: 24,2 % frente a 14,3 %.
- **ENAPRES, forma de entrada en Lima Este.**
  - El **41 % de quienes fueron al cine tuvo la entrada pagada por otra persona**: el acceso depende de
    terceros.
  - Bibliotecas (96 %), festivales locales (93 %) y ferias del libro (77 %) son sobre todo de entrada libre.
- **ENAPRES, diferencias de Lima Este frente a Lima Metropolitana:**
  - **festivales locales o tradicionales** 19,6 % frente a 15,0 % (z ≈ 2,3);
  - **bibliotecas** 14,1 % frente a 10,4 % (z ≈ 2,1);
  - conciertos **menos**: 21,4 % frente a 26,8 % (z ≈ −2,6).

  Nada de esto se usó: la lectura, las bibliotecas y los festivales tradicionales no aparecen en ninguna
  propuesta.
- **ENAPRES, barreras de Lima Este:** son publicables en los ítems principales (E6).
- **ENUT 2024:**
  - cuidado de otras personas del hogar: 48,9 % de los jóvenes de Lima Este y 58,1 % de 25–29; en Lima
    Metropolitana, 56,6 % de las mujeres frente a 36,3 % de los hombres;
  - insatisfacción con el tiempo para pasatiempos: 36,0 % en Lima Este frente a 28,6 % (z ≈ 2,0).
- **ENAHO por edad en Lima Este:**
  - uso de internet para educación: 38,3 % entre los de 20–24;
  - asistencia: 62,4 % entre los de 15–19 y 10,8 % entre los de 25–29.
- **Dato Joven, Lima Metropolitana:**
  - alcohol en los últimos 30 días, 37,2 % (ENDES 2025);
  - **alguna vez embarazada, 3,4 % de las mujeres de 15–19 (referencial, 2024)**, que ayuda a dimensionar P11;
  - superior completa a los 22–24: 28,7 % de las mujeres frente a 19,8 % de los hombres;
  - maltrato o discriminación, 14,6 % (referencial);
  - dispositivo de acceso a internet (computadora o laptop).
- **RENOJ `tematica_1`:** 18 organizaciones de ciencia y tecnología, 7 de democracia y derechos humanos y 3 de
  derechos sexuales y reproductivos. Sirven como aliados posibles (no como demanda).

### En microdatos ya descargados, sin procesar

- **ENAHO 2022–2025, Módulos 03 + 05.** Todo en Lima Este (sección 5):
  - situación de estudio y trabajo;
  - búsqueda de empleo e inactivos que quieren trabajar;
  - actividad principal de los inactivos;
  - categoría ocupacional (independientes);
  - informalidad 2022–2023;
  - nivel educativo alcanzado;
  - si el centro de estudios está en otro distrito (`p308c1`);
  - gestión estatal o privada (`p308d`).
  - Además, **`p310`** ("en los últimos 12 meses, ¿recibió enseñanza en algún centro o programa…"). Responde
    "sí" un ~14 % de la muestra de jóvenes (sin ponderar), y **hay que verificar en el cuestionario qué mide**
    antes de usarla.
- **ENAPRES 2022–2025 por grupo de edad dentro de Lima Este.** Permitiría comprobar los segmentos de 15–24.
  - Precisión esperable (extrapolada, a verificar): cine con CV ≈ 5; conciertos con CV ≈ 14; videojuegos en
    línea con CV ≈ 10.
- **ENUT 2024: día de semana frente a fin de semana.** Es la única base para decir algo sobre *cuándo* tienen
  tiempo los jóvenes. Lima Metropolitana probablemente confiable; Lima Este probablemente referencial.

---

## 5. Denominadores que podemos calcular

### 5.1 Ya calculados y validados

| Denominador | Fuente | Ámbito | Valor |
|---|---|---|---|
| Población 15–29 por distrito, sexo y edad | Dato Joven (REUNIS/INEI) | Distrito | 2026: 712 mil; 226 mil de 15–19, 221 mil de 20–24, 265 mil de 25–29 |
| Asistencia educativa por edad | ENAHO 2022–2025 | Lima Este | 15–19: 62,4 %; 20–24: 36,3 %; 25–29: 10,8 % |
| Práctica semanal (ENUT) | ENUT 2024 | Lima Este (15–29; edades casi todas referenciales) | Deporte 27,6 %; pantallas 92,7 %; etc. |
| Práctica cultural anual | ENAPRES 2022–2025 | Lima Este (15–29, por sexo) | Cine 63,2 %; espectáculos en vivo 44,6 %; etc. |
| Nacimientos de madres de 15–19 y casos de los CEM | Registros | Distrito | Tasas por 1 000 o por 10 000 |

### 5.2 Calculables con datos ya descargados (factibilidad comprobada; valores preliminares)

Lima Este, ENAHO 2022–2025, dominio no planificado. Las definiciones son provisionales (ver 5.3).

| Segmento o denominador | % del grupo (IC 95 %) | CV | Personas: base Dato Joven 2026 | Personas: base expansión ENAHO |
|---|---|---|---|---|
| 15–29 que no estudia ni trabaja | 20,4 (18,7–22,0) | 4,1 | 133–157 mil | 159–186 mil |
| 15–29 que busca trabajo (desocupado) | 5,8 (4,8–6,8) | 9,1 | 34–48 mil | 40–58 mil |
| 15–29 sin trabajo que busca o quiere trabajar | 11,4 (10,1–12,7) | 6,0 | 72–91 mil | 85–108 mil |
| Mujeres 15–29 que no estudian ni trabajan y se dedican al hogar | 15,3 (13,2–17,5) | 7,1 | 50–67 mil | 56–75 mil |
| 15–29 que estudia y trabaja | 10,3 (8,9–11,7) | 6,9 | 63–83 mil | 76–99 mil |
| 15–29 que trabaja como independiente o empleador | 9,9 (8,7–11,1) | 6,1 | 62–79 mil | 74–94 mil |
| 15–29 con empleo informal (2022–2023) | 37,6 (34,5–40,7) | 4,2 | 246–290 mil | 276–326 mil |
| 15–24 que no estudia y cuyo nivel máximo es secundaria completa | 29,1 (26,8–31,4) | 4,0 | 120–140 mil | 145–170 mil |
|  … y su motivo principal son los problemas económicos | 9,8 (8,2–11,4) | 8,4 | 36–51 mil | 44–61 mil |
|  … y su motivo principal es que está trabajando | 10,0 (8,3–11,6) | 8,3 | 37–52 mil | 45–63 mil |
|  … y responde "terminó estudios o asiste a academia" (categoría mixta) | 6,3 (5,1–7,4) | 9,8 | 23–33 mil | 27–40 mil |

Otros resultados:

- **Composición de quienes no estudian ni trabajan (15–29):**

  | Situación | Total | Mujeres | Hombres |
  |---|---|---|---|
  | Busca trabajo | 20 % | 19 % | 21 % |
  | Inactivo que quería trabajar | 14 % | 16 % | 11 %, referencial |
  | Se dedica a los quehaceres del hogar | 50 % | **62 %** | 31 % |
  | Declara estar estudiando | 15 % | — | — |
  | De vacaciones | 14 % | — | — |

- **Informalidad entre los ocupados de 15–29 (2022–2023):** 70,0 % (CV 3,1). En Lima Metropolitana, 66,7 %.
- **Independientes o empleadores entre los ocupados:** 18,2 %.
- **Estudiantes cuyo centro está en otro distrito:** 23,8 % de los de 15–19 y **62,0 % de los de 20–29**. Es un
  dato sobre desplazamiento que no existía en el análisis.

### 5.3 Condiciones antes de usar estos denominadores

1. **Validar la definición de "no estudia ni trabaja".**
   - Con la definición provisional (asiste = matriculado y asiste; trabaja = ocupado), la réplica para Lima
     Metropolitana da 22–25 %. Dato Joven publica 18–20 %.
   - "Trabaja y estudia" coincide (±0,1 punto); "solo estudia" queda 3–5 puntos por debajo.
   - La diferencia parece venir de quienes están **de vacaciones** entre ciclos: la ENAHO se levanta todo el
     año, y el 13,6 % de este grupo en Lima Este declara estar de vacaciones.
   - Hay que encontrar la definición del INEI y validarla con tolerancia de ±1 punto, como en D15. Hasta
     entonces, las cifras de 5.2 sirven para dimensionar, no para publicar.
2. **Decidir la base de población.**
   - La ENAHO expande a 778–908 mil jóvenes; REUNIS/INEI da 712 mil en 2026.
   - Propongo **no publicar un número único de personas**: siempre un rango con ambas bases, o solo
     porcentajes con una frase de orden de magnitud.
3. **Mantener "agrupado 2022–2025"** como periodo de referencia. No describe 2026.
4. **Comparar Lima Este con el resto de Lima Metropolitana**, no con el total. Lima Este forma parte de Lima
   Metropolitana, así que la prueba z actual es solo aproximada.

---

## 6. Denominadores que no podemos calcular

| Lo que haría falta | Por qué no | Consecuencia |
|---|---|---|
| **Intención de continuar estudios o de postular** | Ninguna fuente lo pregunta. | Para P01 hay población en situación compatible (5.2), pero **no sabemos cuántos quieren prepararse**. |
| Cuántos ya asisten a academias preuniversitarias | La ENAHO lo agrupa con "terminó sus estudios". | No sabemos cuántos ya están cubiertos. |
| **Interés declarado en cualquier actividad concreta** | Ninguna fuente pregunta a los jóvenes de Lima Este qué harían. | Todas las fichas quedan con interés = práctica relacionada o sin evidencia. |
| Cualquier indicador de encuesta por distrito | Sin representatividad distrital. | La elección de distrito sigue siendo operativa (I-R7). |
| Práctica deportiva por sexo en Lima Este | Muestra de la ENUT insuficiente (~230 jóvenes). | La brecha por sexo solo se conoce para Lima Metropolitana. |
| Deporte **organizado** (ligas, clubes) frente a informal | La ENUT no lo distingue. | El interés por ligas no se puede estimar. |
| Público de la "cultura urbana" (géneros) | La ENAPRES no pregunta géneros. | P05 no puede sostener su foco en la cultura urbana. |
| Aspiración a emprender, reciente y local | Solo hay Ipsos 2019–2020, 13–20 años, Perú urbano. | P09 sin evidencia actual de interés. |
| Prevalencia de salud mental en Lima Este | Solo hay Lima Metropolitana (ENDES). | El alcance de P08 no es estimable en Lima Este. |
| Inseguridad en Lima Este | Solo hay Lima Metropolitana. | PT-10 queda como contexto metropolitano. |
| Horarios preferidos, distancia aceptable, disposición a pagar | No medidos. | Las condiciones de diseño de tiempo y costo son supuestos. |
| Tasas de inscripción al voluntariado por situación | Decisión D18 (periodo y categorías). | Solo es posible una comparación descriptiva. |
| Cifras de convocatoria con denominador (cupos) | Las notas casi nunca informan cupos. | No se puede distinguir baja convocatoria de oferta pequeña. |
| Jóvenes de 30 años | Ninguna fuente los separa (D2). | La población objetivo sigue aproximada con 15–29. |

---

## 7. Saltos inferenciales detectados

| ID | Salto | Dónde | Por qué es un salto | Tratamiento propuesto |
|---|---|---|---|---|
| S1 | Práctica → interés por una actividad **organizada** | P04, P05, P06, P07; PT-02, PT-03, PT-04 | Hacer deporte, ir al cine o jugar en línea no implica querer una liga, un cineforo o un torneo presencial. | Clasificar como "práctica relacionada". La hipótesis se enuncia explícitamente. |
| S2 | Consumo → producción | P06 (taller de video), P07 (streaming, diseño) | Ver video el 92,8 % no dice nada sobre querer producirlo. | Sin evidencia para el componente de producción. |
| S3 | "No dijo falta de interés" → tiene interés | PT-01, P01, informe | Motivo principal, de respuesta única y subdeclarable; su universo es 15–24. | "No sabemos si quieren continuar estudios." |
| S4 | Problema existente → la actividad lo resuelve | P03 (programar 14,5 % → talleres), P09 (informalidad → emprendimiento), P10 (baja participación → voluntariado), P08 (depresión → grupos de pares) | La existencia del problema no muestra que esta actividad sea pertinente ni aceptada. En P09 la relación incluso puede ir en contra: más autoempleo puede significar más informalidad. | Registrar la necesidad y, aparte, la pertinencia de la respuesta como hipótesis. |
| S5 | Lima Metropolitana → Lima Este | P02 (necesidad), P08, PT-06, PT-10 | Está etiquetado, pero los segmentos se diseñan con brechas metropolitanas cuando ya había datos de Lima Este. | Usar Lima Este cuando exista; si no, "contexto metropolitano". |
| S6 | Segmento de edad sin datos | P03, P05, P06, P07 (15–24); P02 (18–29) | Los datos citados son de 15–29. | Segmentar solo con datos, o calcular por edad (sección 4). |
| S7 | Registro de atención → necesidad o prevalencia | P08 ("94 % mujeres" en los CEM), P11 (necesidad "alto") | Lo reconoce la Capa 1, pero no se tradujo en el nivel. | Tipo de necesidad = "registro de atención", sin magnitud poblacional. |
| S8 | Demanda por una oferta concreta → convocatoria de una actividad más amplia | P01 (beca → "medio"), P02 (talleres de SENAJU, que incluyen arte) | C3-D9 está en el texto, pero pesó en el nivel. | La demanda observada queda como un registro con comparabilidad "parcial". |
| S9 | Componente → paquete | P01, P04, P06, P07 | La evidencia de un componente sostiene al conjunto. | Evaluar por componente. |
| S10 | Falta de datos → convocatoria "baja" | P03, P04, P05, P08, P09, P10, P11 | "Bajo" se lee como baja convocatoria. | Categoría "sin evidencia", distinta de "evidencia de baja convocatoria". |
| S11 | Diferencia Lima Este – Lima Metropolitana no distinguible, presentada en paralelo | H2-02 (deporte), PT-03 | z ≈ −1,7. | No enunciar contrastes sin prueba. |
| S12 | Condición de diseño sin dato | PT-08, P03, P05 | Horario, cercanía, alcohol y equipos no se midieron. | Etiquetarlas como "supuesto de diseño". |

---

## 8. Propuesta de nuevo esquema de integración

### 8.1 Unidad de análisis

La **ficha de actividad por segmento**: un tipo de actividad (o un componente) para un segmento definido con
datos. Un tipo de actividad puede tener varias fichas, por ejemplo "preparación preuniversitaria – 15–24 sin
estudios superiores con motivo económico". Las fichas se agrupan por tema, **no se ordenan** y no llevan
puntaje.

### 8.2 Registro de evidencia atómico (`evidencias.csv`)

Cada dato que entra en una ficha es una fila con los siguientes campos:

- **Identificación:** `id` (E-###), `capa`, `fuente`, `anio_o_periodo`.
- **Población:** `ambito` (Lima Este / Lima Metropolitana / distrito / Perú urbano / nacional / otro) y
  `poblacion` (edad, sexo y condición).
- **Medición:** `n_muestral`, `indicador`, `valor`, `ee`/`cv`/`ic95`, `precision`.
- **Tipo:**
  - `tipo`: dato observado / cálculo derivado / interpretación / hipótesis;
  - `relacion`: directa / proxy, y qué representa;
  - `antiguedad`: reciente (2022+) u orientativa (anterior).
- **Límites:** `limitacion` y `referencia` (archivo, notebook o C3-###).

Los hallazgos actuales (H1–H3) se descomponen en estos registros. Muchos hallazgos contienen varios datos con
ámbitos distintos (por ejemplo, H2-02 mezcla Lima Este y Lima Metropolitana).

### 8.3 Categorías por dimensión, con reglas escritas

Las categorías son **descriptivas**. Son ordenables solo dentro de cada dimensión, y ninguna se suma con otra.

**Necesidad o problemática**

- **Tipo:**
  - `prevalencia` (encuesta representativa);
  - `brecha de acceso` (por ejemplo, no asiste con secundaria completa);
  - `registro de atención` (depende del acceso; no mide prevalencia);
  - `objetivo institucional` (lo que la organización quiere cambiar; no es necesidad declarada ni medida);
  - `sin evidencia`.
- **Ámbito y año** (del registro de evidencia).
- **Población afectada:** % del segmento y de la juventud total, rango de personas con ambas bases, o "no
  estimable".

**Interés o práctica: distancia inferencial**

| Código | Qué se observó | Ejemplo |
|---|---|---|
| P0 | Sin evidencia. | — |
| P1 | **Práctica relacionada**: un dominio más amplio u otro formato. | Deporte o ejercicio semanal para una liga organizada. |
| P2 | **Práctica de la misma actividad**, en el mismo formato. | Asistencia a festivales locales para un festival local. |
| I1 | Interés declarado en el tema. | Solo Ipsos 2019–2022 (antiguo, Perú urbano). |
| I2 | Interés declarado en participar en la actividad propuesta. | No existe en ninguna fuente actual. |

Regla: una ficha llega a P2 solo si el indicador mide el mismo formato (organizado o no, gratuito o pagado,
presencial) y el mismo rango de edad. Si difiere en cualquiera de esos rasgos, queda en P1.

**Convocatoria**

| Código | Qué se observó |
|---|---|
| C0 | Sin evidencia: no se encontró actividad comparable con datos. **No es un resultado negativo.** |
| C1 | Solo oferta existente, sin información de participación. |
| C2 | Participación declarada sin cifra o sin segmento compatible. |
| C3 | Participación declarada con cifra, en segmento y territorio compatibles. |
| C4 | Demanda observada (más interesados que cupos) en una oferta comparable. |
| CB | **Evidencia de baja convocatoria**: cupos sin llenar, cancelaciones o asistencia menor que la inscripción. |

Cada registro de convocatoria lleva además:

- comparabilidad en segmento, territorio, formato y costo (sí / parcial / no);
- verificación (declarada por quien organiza / verificada);
- denominador (cupos, sí o no).

**Alcance potencial**

- `amplia`: la evidencia se refiere a toda la juventud y la actividad no exige una condición particular. Se
  indica el % que practica o está afectado.
- `segmento identificable`: la actividad solo tiene sentido para una condición medible. Se indica el tamaño con
  rango de personas.
- `desconocido`: no hay denominador. Se escribe "alcance potencial no estimable con la evidencia disponible".

No se fija un umbral para "amplia" frente a "segmento": se muestran las cifras. El tamaño **no se convierte en
importancia ni en recomendación**.

**Barreras**

Un registro por barrera con los campos:

- `medida en` (ámbito, población y actividad);
- `pertinencia`: directa (medida para esa actividad) / indirecta (otra actividad) / supuesto de diseño.

### 8.4 Ficha: la cadena de trazabilidad

```
CONTEXTO/NECESIDAD        tipo · ámbito · magnitud               → E-ids
POBLACIÓN A LA QUE APLICA segmento (edad, sexo, estudia/trabaja…) → definición + denominador
INTERÉS O PRÁCTICA        P0–P2 / I1–I2 · qué salto queda abierto → E-ids
ALCANCE POTENCIAL         amplia / segmento (rango) / desconocido → E-ids
OFERTA TERRITORIAL        qué existe y dónde (no es demanda)      → C3-ids
CONVOCATORIA              C0–C4 / CB · comparabilidad             → C3-ids
BARRERAS                  medidas / indirectas / supuestos        → E-ids
VACÍOS                    qué no sabemos (explícito)
QUÉ PODEMOS AFIRMAR       solo datos observados o cálculos derivados, con E-ids
QUÉ ES HIPÓTESIS          enunciados verificables con un piloto o una consulta
```

### 8.5 Productos

| Archivo | Contenido |
|---|---|
| `resultados/evidencias.csv` | Registros atómicos (8.2). |
| `resultados/segmentos.csv` | Definiciones de segmentos con denominador, IC, bases de población y fuente. |
| `resultados/fichas_actividad.csv` | Las fichas (8.4), con referencias a evidencias, segmentos y C3. |
| `resultados/hallazgos_integrados.csv` | Se conserva como capa de lectura, corregido (sección 1.1) y enlazado a E-ids. |
| `scripts/` | Nuevo script de denominadores (versión validada de la prueba de factibilidad), que escribe en `data/processed/`. |
| Notebook 04 | Se reconstruye: verifica que cada afirmación de una ficha cite al menos una evidencia de tipo observado o derivado, y que las categorías cumplan sus reglas. |
| Informe y observatorio | Se regeneran desde las fichas. |

Para que la asignación de categorías sea reproducible, propongo que una segunda persona del equipo codifique
por separado una muestra de fichas y se comparen los resultados.

---

## 9. Qué cambiaría respecto de las 11 propuestas actuales

Resultado **preliminar**: la clasificación final saldrá de aplicar el esquema de la sección 8.
A = confirmar · B = reformular · C = descartar como conclusión del análisis.

| Propuesta | Niveles actuales (N/I/C) | Qué respalda realmente la evidencia | Saltos | Resultado | Reformulación sugerida |
|---|---|---|---|---|---|
| **P01** Preuniversitaria + orientación + becas | alto / medio / medio | **Brecha de acceso con segmento dimensionable:** ~29 % de los jóvenes de 15–24 de Lima Este no estudia y su nivel máximo es secundaria completa. Un tercio de ellos cita problemas económicos, otro tercio está trabajando (prelim.). Hay participación declarada en academias municipales gratuitas (C3) y **una** demanda observada por una beca concreta (C4, oferta específica). | S3, S8, S9 | **B** | Separar tres componentes: preparación, orientación y apoyo para postular a becas. Segmento: 15–24 con secundaria completa sin estudios superiores (y el subsegmento con motivo económico). Registrar como vacío principal la **intención de continuar estudios** y cuántos ya van a academias. La "falta de interés 2 %" deja de ser evidencia. |
| **P02** Empleabilidad y primer empleo (prioridad mujeres NINI) | medio / medio / medio | La necesidad se puede medir **en Lima Este**: ~6 % de los jóvenes busca trabajo, ~11 % busca o quiere trabajar, 70 % de los ocupados es informal (prelim.). Entre las mujeres que no estudian ni trabajan predomina la dedicación al hogar (62 %), no la búsqueda de empleo. Convocatoria: cifras pequeñas y declaradas; SENAJU agotó cupos a escala de Lima (C4 parcial). | S5, S6, S8 | **B** | Segmento: jóvenes sin trabajo que buscan o quieren trabajar, con denominador. Retirar la "prioridad mujeres NINI" para este formato. La situación de las mujeres dedicadas al hogar pasa a ser un vacío y un segmento aparte (ver N4). Interés en talleres: P0. |
| **P03** Habilidades digitales + retos | medio / medio / bajo | La necesidad no está demostrada: que pocos programen no hace de eso una necesidad. Uso de internet para aprender: 32,7 % en Lima Este (P1). Una hackathon con 400 inscritos de 18 años o más, de varios distritos y no solo jóvenes (C2–C3 parcial). Hay 18 organizaciones de ciencia y tecnología en el RENOJ (aliados). | S4, S6 | **B** (parcial) | Mantener solo el formato con una señal de convocatoria (reto colaborativo para 18+). Necesidad = sin evidencia. Retirar el segmento 15–24. |
| **P04** Deporte organizado 18–29 + opción mujeres | bajo / alto / bajo | Práctica de deporte o ejercicio: 27,6 % semanal en Lima Este (15–29; las edades son referenciales), P1 respecto de una liga. Brecha por sexo solo en Lima Metropolitana. Convocatoria para 18–29: **C0**, sin evidencia, no "baja". | S1, S10, S11 | **B** | Interés P1 (no "alto"). Alcance: amplia para actividad física, desconocido para ligas. El componente femenino queda como hipótesis explícita, con la brecha de Lima Metropolitana como contexto. |
| **P05** Cultura urbana y música en vivo | sin ev. / alto / bajo | Espectáculos musicales: 21,4 % en Lima Este, **menos que en Lima Metropolitana**; se entra sobre todo pagando; el dinero es la barrera del 21 % de quienes no fueron. Festivales locales: 19,6 %, **más que en Lima Metropolitana**, con entrada libre. No hay datos del género "urbano" ni de jóvenes como artistas u organizadores. | S1, S6 | **B** | Reorientar a **festival o escenario local gratuito** (P2 para festivales locales). "Cultura urbana" y "jóvenes organizadores" quedan como hipótesis. Segmento 15–29 (o calcular por edad). |
| **P06** Cine + conversación + taller de video | sin ev. / alto / sin ev. | Cine comercial: 63,2 % en Lima Este, mujeres más que hombres. El 41 % de quienes fueron no pagó su propia entrada. El dinero es la barrera del 18,8 % de quienes no fueron. | S1, S2, S9 | **B** / **C** | B para **proyecciones gratuitas** (P1; hipótesis de sustitución del cine pagado). C para el taller de video y la conversación (sin evidencia). |
| **P07** Videojuegos y e-sports presenciales | sin ev. / medio / sin ev. | **Segmento claro en Lima Este:** 52,8 % de los hombres juega en línea y 60,9 % en el celular; las mujeres, 18,9 % y 33,6 %. Formato presencial: C0. | S1, S2, S6 | **B** | Segmento: hombres jóvenes (dato de Lima Este). Interés P1. El componente de inclusión de mujeres y el de habilidades digitales quedan como hipótesis aparte. |
| **P08** Bienestar para mujeres jóvenes | medio / bajo / bajo | Necesidad de prevalencia en Lima Metropolitana: episodio depresivo en 21,6 % de las mujeres; violencia en 31,5 % de las que tienen pareja. Registro de atención en Lima Este (CEM). Interés: **P0** (lo citado no es interés). Convocatoria voluntaria: C0 (las charlas escolares son de público cautivo). | S4, S5, S7 | **B** | Ficha "respuesta a una necesidad, con interés y convocatoria desconocidos". Alcance en Lima Este no estimable. Se muestran sin elegir las dos opciones de diseño (actividad propia o componente con derivación). |
| **P09** Emprendimiento y ventas por internet | medio / bajo / bajo | La informalidad no es una necesidad de emprender (S4). La aspiración es de 2019–2020, 13–20 años, Perú urbano. Sí hay una **práctica observada**: ~18 % de los ocupados (~10 % de los jóvenes) trabaja por cuenta propia o es empleador (prelim.). | S4 | **C** tal como está | Posible ficha nueva: **jóvenes que ya trabajan por cuenta propia** (segmento identificable). Interés y convocatoria: P0 y C0/C2. |
| **P10** Voluntariado corto | bajo / medio / bajo | "Necesidad" = objetivo institucional. La práctica de la ENUT incluye ayudar a otros hogares (E5) y es referencial. El registro de voluntariado muestra quién llega (estudiantes y mujeres), no que otros llegarían con otro formato. Hay participación declarada pequeña. | S4, S10 | **B** | Tipo de necesidad = objetivo institucional. La hipótesis de llegar a jóvenes que trabajan queda explícita y sin evidencia. |
| **P11** Educación sexual integral para adolescentes | alto / sin ev. / bajo | Registro de atención y nacimientos concentrado en mujeres de 15–19. Magnitud baja y descendente: los nacimientos cayeron a menos de la mitad entre 2019 y 2025, unos 14 por 1 000 al año; alguna vez embarazada, 3,4 % en Lima Metropolitana (referencial). Interés P0. Convocatoria cautiva. | S7 | **C** como actividad | Se conserva como **condición de diseño** transversal: protocolos de protección y rutas de derivación en cualquier actividad con adolescentes. No como "necesidad general de las juventudes". |

**Alternativas que la primera integración omitió** (a evaluar con el nuevo esquema; no son propuestas):

- **N1. Lectura, bibliotecas y ferias del libro.**
  - Práctica en Lima Este: bibliotecas 14,1 % (más que en Lima Metropolitana), ferias del libro 19,4 %, libros
    digitales 54,8 %.
  - Entrada mayormente libre.
  - La falta de información es la barrera del 12 % de quienes no fueron a ferias del libro.
  - Falta revisar la oferta en el registro de la Capa 3.
- **N2. Festivales y ferias locales o tradicionales.** Festivales 19,6 % (más que en Lima Metropolitana) y
  ferias artesanales 20,8 %, con entrada libre. Puede absorber parte de P05.
- **N3. Derechos laborales y formalización para jóvenes que ya trabajan.** Informalidad del 70 % de los
  ocupados de Lima Este (2022–2023), que equivale a ~38 % de todos los jóvenes. En el registro solo se
  identificó explícitamente un encuentro sobre formalización laboral (C3-061), sin cifras. Falta revisar el
  resto de la oferta de empleo con este criterio.
- **N4. Mujeres jóvenes que no estudian ni trabajan y se dedican al hogar** (~15 % de las mujeres jóvenes de
  Lima Este).
  - Es el segmento más grande que el análisis no cubre.
  - No hay evidencia sobre qué actividad sería pertinente; cualquier actividad debería ser compatible con el
    cuidado (48,9 % de los jóvenes cuida a alguien del hogar cada semana, según la ENUT).
  - **No es una propuesta: es un vacío** que solo una consulta directa puede resolver.
- **N5. Jóvenes que estudian y trabajan** (~10 %). No es una actividad sino un segmento con poco tiempo. Sirve
  como condición de diseño.

---

## 10. Vacíos que solo se resuelven con consulta directa u otra fuente

### Consulta directa a jóvenes de Lima Este

Es el único modo de pasar de P1/P2 a I1/I2. Debería preguntar:

1. **Interés en participar** en actividades concretas y en formatos concretos: liga o juego libre, proyección
   o cineforo, torneo presencial o en línea, festival, taller.
2. **Intención de continuar estudios**, preparación actual (academia, autodidacta) y postulación a becas.
3. **Disponibilidad:** días, horarios, tiempo de traslado aceptable y disposición a pagar.
4. **Condiciones para participar**, en especial para quienes cuidan a alguien o se dedican al hogar.
5. **Canales de información** que usan.
6. **Seguridad percibida** para ir a actividades, sobre todo de noche.

### Registros administrativos de convocatoria real

Solicitudes de acceso a la información pública (Ley 27806) a las municipalidades, SENAJU e IPD:

- inscritos, asistentes y cupos por edad y sexo en sus actividades juveniles;
- listas de espera.

Esto convertiría las cifras declaradas en cifras verificadas, con denominador (C3/C4 verificables, o CB).

### Fuentes públicas complementarias (a verificar; no incorporadas)

| Vacío | Fuente posible | Compatibilidad |
|---|---|---|
| Inseguridad en Lima Este | ENAPRES, módulo de seguridad ciudadana, 2022–2025 (misma encuesta y método del capítulo 800A ya usado) | Alta. Hay que verificar la muestra de jóvenes. |
| Salud mental en Lima Este | Microdatos de la ENDES (cuestionario de salud) | Por verificar: la muestra de jóvenes de Lima Este podría ser insuficiente. |
| Cohorte que termina la secundaria, por distrito | MINEDU (ESCALE): matrícula de 5.º de secundaria por distrito | Administrativa y reciente. Serviría como denominador distrital para P01. |
| Postulación a becas por distrito de procedencia | PRONABEC (Beca 18) | Por verificar si es pública, sin eludir bloqueos de acceso. |
| Cuándo tienen tiempo libre | ENUT 2024: día de semana frente a fin de semana (**ya descargada**) | Alta. Solo requiere cálculo. |

---

## Decisiones que necesito del equipo antes de reconstruir

1. **Esquema:** ¿aprueban reemplazar alto/medio/bajo por las categorías descriptivas de la sección 8.3 y la
   ficha de la sección 8.4?
2. **Nuevos denominadores de Lima Este (ENAHO 03 + 05):** ¿los incorporamos, sujetos a validar la definición de
   "no estudia ni trabaja" contra Dato Joven (±1 punto, como D15)?
3. **Base de población:** ¿rango con ambas bases (propuesta) o solo porcentajes?
4. **Fuentes complementarias:** ¿exploro el módulo de seguridad ciudadana de la ENAPRES y la ENUT por día de la
   semana (ambas compatibles), o nos limitamos a los datos actuales?
5. **P11 y P09:** ¿de acuerdo con retirarlas como actividades (P11 como condición de diseño; P09 con posible
   reformulación hacia jóvenes que ya trabajan por cuenta propia)?
6. **Alternativas N1–N5:** ¿se evalúan con el nuevo esquema junto con las reformulaciones?
