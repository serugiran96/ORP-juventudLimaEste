"""Contenido de la integración (segunda versión): hallazgos, patrones, segmentos y fichas de actividades.

Las cifras NO se escriben a mano. Los textos usan marcadores que integracion_construir.py reemplaza con los
valores de resultados/evidencias.csv y del registro de la Capa 3:
    {E-110}           valor con su unidad y precisión ("63,2 %"; "12,9 % (referencial)")
    {E-110:personas}  cantidad estimada con las dos bases de población
    {E-110:n}         tamaño de muestra
    {C3-070}          cifra declarada de una actividad del registro de la Capa 3
Un texto con un porcentaje escrito a mano no pasa la validación.

Códigos (reglas completas en fuentes/metodologia_integracion.md):
- Necesidad: prevalencia | brecha de acceso | registro de atención | situación documentada |
  objetivo institucional | sin evidencia.
- Interés o práctica (distancia inferencial): P0 sin evidencia; P1 práctica relacionada; P2 práctica de la misma
  actividad; I1 interés declarado en el tema; I2 interés declarado en participar en la actividad.
- Convocatoria: la calcula el constructor a partir del registro de la Capa 3 y de la comparabilidad declarada aquí
  (C0 sin evidencia; C1 solo oferta; C2 participación sin cifra o sin segmento/territorio compatibles; C3
  participación con cifra en segmento y territorio compatibles; C4 demanda observada en oferta comparable).
- Alcance: amplia | segmento identificable | desconocido.
"""

# ---------------------------------------------------------------------------------------------------------------
# HALLAZGOS: lectura por capa. estado = sin cambios | corregido | reemplazado | ampliado | nuevo
HALLAZGOS = [
    # Capa 1: contexto y necesidades
    dict(id="H1-01", capa=1, dimension="demografía", estado="ampliado",
         enunciado="Dato Joven proyecta {E-001} jóvenes de 15 a 29 años en los siete distritos en 2026: {E-002} de "
                   "15–19, {E-003} de 20–24 y {E-004} de 25–29. San Juan de Lurigancho tiene {E-010} y Ate {E-011}. "
                   "Las encuestas del INEI estiman otro total para Lima Este (ENAHO: {E-007}; ENAPRES: {E-008}; "
                   "ENUT: {E-009}), porque sus factores no se calibran por distrito.",
         no_permite="Tendencias de población (series inestables, D5); una cifra única y exacta de jóvenes.",
         evidencias="E-001; E-002; E-003; E-004; E-010; E-011; E-007; E-008; E-009",
         cambio="Se agregan las bases de población de las encuestas y se explica por qué difieren."),
    dict(id="H1-02", capa=1, dimension="organización juvenil", estado="corregido",
         enunciado="Hay {E-221} organizaciones juveniles acreditadas (RENOJ, 2019–2026). San Juan de Lurigancho tiene "
                   "{E-222} por 10 000 jóvenes, frente a una mediana metropolitana de {E-223}. Por temática "
                   "principal: {E-224} de ciencia y tecnología, {E-229} de democracia y derechos humanos, {E-225} de "
                   "cultura y arte (temática agrupada) y {E-219} de deporte.",
         no_permite="Que haya poca organización juvenil real: solo se cuentan las acreditadas.",
         evidencias="E-221; E-222; E-223; E-224; E-229; E-225; E-219",
         cambio="La primera versión decía que ninguna era de participación y ciudadanía; la categoría 'Otros' "
                "ocultaba 7 de democracia y derechos humanos y 18 de ciencia y tecnología."),
    dict(id="H1-03", capa=1, dimension="voluntariado", estado="sin cambios",
         enunciado="{E-226} personas de los siete distritos están inscritas en el Programa de Voluntariado Juvenil: "
                   "{E-227} mujeres y {E-228} solo estudia. Es un registro de autoselección.",
         no_permite="Intereses de la juventud en general.", evidencias="E-226; E-227; E-228", cambio=""),
    dict(id="H1-04", capa=1, dimension="voluntariado", estado="reemplazado",
         enunciado="Quienes llegan al voluntariado son sobre todo estudiantes: {E-228} de los inscritos solo "
                   "estudia, frente a {E-041} de los jóvenes de Lima Este (ENAHO).",
         no_permite="Tasas de inscripción por situación (D18): es una comparación descriptiva.",
         evidencias="E-228; E-041",
         cambio="Compara con Lima Este (antes, con Lima Metropolitana)."),
    dict(id="H1-05", capa=1, dimension="educación", estado="reemplazado",
         enunciado="En Lima Este asiste a educación {E-021} de los jóvenes de 15–19 y {E-022} de los de 25–29. "
                   "{E-023} de los jóvenes de 15–24 no estudia y su nivel máximo es secundaria completa.",
         no_permite="Intención de continuar estudios.", evidencias="E-021; E-022; E-023",
         cambio="Reemplaza indicadores de Lima Metropolitana por estimaciones de Lima Este."),
    dict(id="H1-06", capa=1, dimension="empleo", estado="reemplazado",
         enunciado="En Lima Este (2022–2025), la tasa de desempleo juvenil es {E-046} ({E-047} a los 15–19). "
                   "{E-056} de los jóvenes ocupados tiene empleo informal (2022–2023) y {E-058} trabaja por cuenta "
                   "propia o como empleador.",
         no_permite="Informalidad de 2024–2025 (el INEI dejó de publicar la variable, D16).",
         evidencias="E-046; E-047; E-056; E-058",
         cambio="Reemplaza cifras de Lima Metropolitana por estimaciones de Lima Este."),
    dict(id="H1-07", capa=1, dimension="empleo", estado="reemplazado",
         enunciado="Con la definición del proyecto, {E-043} de los jóvenes de Lima Este no estudia ni trabaja: "
                   "{E-044} de las mujeres y {E-045} de los hombres.",
         no_permite="Comparar con la cifra 'NINI' de Dato Joven (definición distinta, no equivalente).",
         evidencias="E-043; E-044; E-045", cambio="Estimación de Lima Este; antes solo había Lima Metropolitana."),
    dict(id="H1-08", capa=1, dimension="salud mental", estado="corregido",
         enunciado="En Lima Metropolitana (2024), {E-200} de las mujeres jóvenes y {E-201} de los hombres jóvenes "
                   "tuvo un episodio depresivo en el último año.",
         no_permite="Prevalencia en Lima Este.", evidencias="E-200; E-201",
         cambio="El dato de hombres es referencial (antes figuraba como confiable)."),
    dict(id="H1-09", capa=1, dimension="competencias digitales", estado="corregido",
         enunciado="En Lima Metropolitana, {E-230} de los jóvenes escribió un programa informático (2024).",
         no_permite="Que programar sea una necesidad de los jóvenes; brechas de Lima Este.", evidencias="E-230",
         cambio="Ya no se usa como evidencia de necesidad."),
    dict(id="H1-10", capa=1, dimension="seguridad", estado="reemplazado",
         enunciado="En Lima Este (2022–2025), {E-100} de los jóvenes se siente inseguro caminando solo de noche por "
                   "su barrio: {E-101} de las mujeres y {E-102} de los hombres. En el último año, {E-103} dejó o "
                   "evitó salir de noche y {E-106} llegar muy tarde a casa por temor a la delincuencia.",
         no_permite="Inseguridad por distrito; horarios concretos que evitan.",
         evidencias="E-100; E-101; E-102; E-103; E-106",
         cambio="Estimación propia de Lima Este con la ENAPRES, validada con Dato Joven (antes, Lima Metropolitana)."),
    dict(id="H1-11", capa=1, dimension="violencia", estado="corregido",
         enunciado="En Lima Metropolitana, {E-202} de las mujeres jóvenes con pareja sufrió violencia de su esposo o "
                   "compañero en el último año (2025).",
         no_permite="Prevalencia en Lima Este; tendencia (la serie varía mucho entre años).", evidencias="E-202",
         cambio="Se agrega la advertencia sobre la variabilidad de la serie."),
    dict(id="H1-12", capa=1, dimension="participación", estado="sin cambios",
         enunciado="La participación de los jóvenes de Lima Metropolitana en asociaciones u organizaciones es muy "
                   "baja ({E-220}, 2025).", no_permite="Participación en Lima Este.", evidencias="E-220", cambio=""),
    dict(id="H1-13", capa=1, dimension="maternidad adolescente", estado="ampliado",
         enunciado="En 2025 se registraron {E-207} nacimientos de madres de 15–19 años con residencia en Lima Este, "
                   "menos de la mitad que en 2019 ({E-208}). La tasa 2022–2025 (nacimientos por cada 1 000 mujeres de "
                   "15–19) supera la mediana metropolitana ({E-210}) en El Agustino ({E-209}), Santa Anita ({E-213}) y Ate ({E-214}). En Lima Metropolitana, "
                   "{E-211} de las mujeres de 15–19 estuvo alguna vez embarazada.",
         no_permite="Embarazos (solo se registran nacimientos).",
         evidencias="E-207; E-208; E-210; E-209; E-213; E-214; E-211", cambio="Se agrega la magnitud poblacional."),
    dict(id="H1-14", capa=1, dimension="violencia", estado="sin cambios",
         enunciado="Los CEM atendieron {E-203} casos de jóvenes con domicilio en Lima Este en 2025; entre las "
                   "víctimas de 2022–2025, {E-204} son mujeres, {E-205} tiene 15–19 años y {E-206} de los casos es de "
                   "violencia sexual.",
         no_permite="Prevalencia de la violencia (los CEM registran atenciones).",
         evidencias="E-203; E-204; E-205; E-206", cambio=""),
    dict(id="H1-15", capa=1, dimension="empleo", estado="nuevo",
         enunciado="Entre quienes no estudian ni trabajan, {E-052} busca trabajo y {E-053} se dedica a los quehaceres "
                   "del hogar; entre las mujeres de ese grupo, {E-054} se dedica al hogar y {E-055} busca trabajo.",
         no_permite="Si quieren estudiar o trabajar en el futuro.", evidencias="E-052; E-053; E-054; E-055",
         cambio="Nuevo: composición del grupo que no estudia ni trabaja."),
    dict(id="H1-16", capa=1, dimension="hogar y cuidado", estado="nuevo",
         enunciado="{E-070} de las mujeres de 15–29 de Lima Este no estudia ni trabaja y se dedica al hogar "
                   "({E-070:personas}); entre los hombres, {E-071}. De ellas, {E-078} tiene 25–29 años, {E-074} está en "
                   "unión (frente a {E-075} de las demás mujeres), {E-076} vive en un hogar con niños de 0 a 5 años "
                   "(frente a {E-077}), {E-079} terminó la secundaria y {E-081} usó internet, pero solo {E-082} lo usa "
                   "para aprender (frente a {E-083}). {E-080} quería trabajar.",
         no_permite="Sus intereses, su disponibilidad o qué actividad les sería útil.",
         evidencias="E-070; E-071; E-078; E-074; E-075; E-076; E-077; E-079; E-081; E-082; E-083; E-080",
         cambio="Nuevo: caracterización de un segmento que la primera versión no cubría."),
    dict(id="H1-17", capa=1, dimension="educación", estado="nuevo",
         enunciado="{E-023} de los jóvenes de 15–24 ({E-023:personas}) no estudia y su nivel máximo es secundaria "
                   "completa. Entre ellos, {E-025} menciona problemas económicos como motivo principal, {E-026} que "
                   "está trabajando y {E-027} que 'terminó sus estudios o asiste a una academia' (categoría mixta).",
         no_permite="Intención de continuar estudios; cuántos ya se preparan en una academia.",
         evidencias="E-023; E-025; E-026; E-027", cambio="Nuevo: población compatible con la preparación "
                                                         "preuniversitaria."),
    dict(id="H1-18", capa=1, dimension="empleo", estado="nuevo",
         enunciado="{E-049} de los jóvenes de Lima Este ({E-049:personas}) no tiene trabajo y busca o quiere trabajar: "
                   "{E-050} de las mujeres y {E-051} de los hombres. {E-048} busca trabajo activamente.",
         no_permite="Qué tipo de apoyo necesitan.", evidencias="E-049; E-050; E-051; E-048", cambio="Nuevo."),
    dict(id="H1-19", capa=1, dimension="empleo", estado="nuevo",
         enunciado="{E-040} de los jóvenes estudia y trabaja, {E-057} ({E-057:personas}) tiene un empleo informal "
                   "(2022–2023) y {E-059} ({E-059:personas}) trabaja por cuenta propia o como empleador.",
         no_permite="Ingresos o condiciones de trabajo.", evidencias="E-040; E-057; E-059", cambio="Nuevo."),
    dict(id="H1-20", capa=1, dimension="desplazamiento", estado="nuevo",
         enunciado="{E-030} de quienes estudian a los 20–24 años lo hace en otro distrito; a los 15–19, {E-031}.",
         no_permite="Distancia o tiempo de viaje; desplazamiento de quienes no estudian.",
         evidencias="E-030; E-031", cambio="Nuevo: único dato de desplazamiento disponible."),

    # Capa 2: intereses, hábitos y barreras
    dict(id="H2-01", capa=2, dimension="uso del tiempo", estado="sin cambios",
         enunciado="Casi todos los jóvenes de Lima Este usan computadora, tablet o celular cada semana ({E-167}) y "
                   "ven películas o video por internet ({E-166}).",
         no_permite="Interés en actividades grupales digitales.", evidencias="E-167; E-166", cambio=""),
    dict(id="H2-02", capa=2, dimension="deporte", estado="corregido",
         enunciado="{E-170} de los jóvenes de Lima Este hizo deporte o ejercicio en la semana (2024); la diferencia "
                   "con Lima Metropolitana ({E-174}) no es distinguible. En Lima Metropolitana, {E-171} de los hombres "
                   "y {E-172} de las mujeres.",
         no_permite="La brecha por sexo en Lima Este (muestra insuficiente); deporte organizado frente a informal.",
         evidencias="E-170; E-174; E-171; E-172", cambio="Ya no se describe como 'una de las prácticas más "
                                                         "extendidas' ni se sugiere que Lima Este practique menos."),
    dict(id="H2-03", capa=2, dimension="uso del tiempo", estado="sin cambios",
         enunciado="Aficiones, artes y juegos ocupan la semana de {E-190} de los jóvenes de Lima Este; asistir a "
                   "eventos, de {E-191} (en Lima Metropolitana, {E-192}).",
         no_permite="Qué aficiones concretas.", evidencias="E-190; E-191; E-192", cambio=""),
    dict(id="H2-04", capa=2, dimension="uso del tiempo", estado="corregido",
         enunciado="{E-147} de los jóvenes de Lima Este leyó en la semana y {E-175} hizo voluntariado o ayudó a la "
                   "comunidad u otros hogares.",
         no_permite="Voluntariado propiamente dicho: la categoría incluye ayudar a familiares o vecinos.",
         evidencias="E-147; E-175", cambio="Aclara que la categoría no es solo voluntariado."),
    dict(id="H2-05", capa=2, dimension="tiempo libre", estado="corregido",
         enunciado="{E-177} de los jóvenes de Lima Este está poco o nada satisfecho con la cantidad de su tiempo libre "
                   "y {E-176} con el tiempo para sus pasatiempos.",
         no_permite="Que la insatisfacción sea mayor que en Lima Metropolitana con certeza.",
         evidencias="E-177; E-176", cambio="Cifras recalculadas desde los datos procesados."),
    dict(id="H2-06", capa=2, dimension="uso del tiempo", estado="sin cambios",
         enunciado="La mitad de los jóvenes de Lima Este estudió en la semana ({E-063}) y {E-060} trabajó o buscó "
                   "trabajo; quienes trabajan dedican {E-061} a la semana.",
         no_permite="Horarios preferidos.", evidencias="E-063; E-060; E-061", cambio=""),
    dict(id="H2-07", capa=2, dimension="cultura", estado="sin cambios",
         enunciado="En 2022–2025, {E-110} de los jóvenes de Lima Este fue al cine en el año; {E-138} a algún "
                   "espectáculo en vivo; {E-120} a conciertos o festivales musicales; {E-130} a festivales locales; "
                   "{E-142} a ferias del libro; {E-136} a espectáculos de danza.",
         no_permite="Preferencias por distrito; interés en actividades organizadas por terceros.",
         evidencias="E-110; E-138; E-120; E-130; E-142; E-136", cambio=""),
    dict(id="H2-08", capa=2, dimension="cultura digital", estado="ampliado",
         enunciado="{E-166} de los jóvenes de Lima Este ve películas o video por internet y {E-169} escucha música por "
                   "internet. {E-168} juega videojuegos en línea: {E-160} de los hombres y {E-161} de las mujeres.",
         no_permite="Interés en actividades presenciales de videojuegos.",
         evidencias="E-166; E-169; E-168; E-160; E-161", cambio="Se agrega el dato por sexo de Lima Este."),
    dict(id="H2-09", capa=2, dimension="barreras", estado="corregido",
         enunciado="En Lima Este, entre quienes no fueron al cine, {E-115} lo atribuye a falta de interés, {E-116} a "
                   "falta de tiempo y {E-114} al dinero; entre quienes no fueron a conciertos, {E-125} al dinero. "
                   "La falta de información pesa en las ferias del libro ({E-144}).",
         no_permite="Barreras de actividades que la encuesta no pregunta (deporte, talleres).",
         evidencias="E-115; E-116; E-114; E-125; E-144",
         cambio="Usa barreras de Lima Este (antes decía que no había datos de Lima Este)."),
    dict(id="H2-10", capa=2, dimension="barreras", estado="ampliado",
         enunciado="En Lima Este casi todos entraron gratis a festivales locales ({E-132}), bibliotecas ({E-148}) y "
                   "ferias del libro ({E-143}); en cambio, {E-124} de los asistentes a conciertos compró su entrada y, "
                   "en el cine, {E-113} tuvo la entrada pagada por otra persona.",
         no_permite="Disposición a pagar.", evidencias="E-132; E-148; E-143; E-124; E-113",
         cambio="Se agrega la dependencia de terceros para pagar el cine."),
    dict(id="H2-11", capa=2, dimension="aprendizaje", estado="corregido",
         enunciado="{E-032} de los jóvenes usuarios de internet de Lima Este lo usa para educación o capacitación y "
                   "{E-231} para vender productos o servicios (2022–2025).",
         no_permite="Una brecha estable de Lima Este frente a Lima Metropolitana.", evidencias="E-032; E-231",
         cambio="Se quita la cifra de un solo año mezclada con el periodo agrupado."),
    dict(id="H2-12", capa=2, dimension="educación", estado="corregido",
         enunciado="Entre los jóvenes de 15–24 de Lima Este que no asisten a educación, el motivo principal es estar "
                   "trabajando ({E-033}) o problemas económicos ({E-034}); {E-037} 'terminó sus estudios o asiste a "
                   "academia' y {E-036} está de vacaciones. 'No le interesa' es poco mencionado ({E-035}).",
         no_permite="Interés por estudiar: es un motivo de respuesta única, y la pregunta no se hace después de los "
                    "24 años.", evidencias="E-033; E-034; E-037; E-036; E-035",
         cambio="Corrige la población (15–24, no 15–29) y deja de leer 'no le interesa' como interés."),
    dict(id="H2-13", capa=2, dimension="aspiraciones", estado="sin cambios",
         enunciado="En 2020, {E-240} de los adolescentes y jóvenes urbanos de 13–20 años decía que su trabajo ideal "
                   "era tener su propio negocio; en 2019, {E-241} de los de 18–20 sin negocio deseaba emprender.",
         no_permite="Aspiraciones actuales de los jóvenes de Lima Este.", evidencias="E-240; E-241", cambio=""),
    dict(id="H2-14", capa=2, dimension="aspiraciones", estado="sin cambios",
         enunciado="Entre quienes trabajaban en 2020 (13–20 años, Perú urbano), {E-243} lo hacía en algo relacionado "
                   "con su carrera.", no_permite="Desajuste actual en Lima Este.", evidencias="E-243", cambio=""),
    dict(id="H2-15", capa=2, dimension="diversión", estado="sin cambios",
         enunciado="En 2019, {E-244} de los adolescentes y jóvenes urbanos se divertía fuera de casa saliendo a comer; "
                   "en 2021–2022, {E-242} de la generación Z (18–25) tenía cuenta en TikTok.",
         no_permite="Preferencias actuales de los jóvenes de Lima Este.", evidencias="E-244; E-242", cambio=""),
    dict(id="H2-16", capa=2, dimension="cultura", estado="nuevo",
         enunciado="Las prácticas culturales cambian con la edad en Lima Este: fue a conciertos {E-121} de los de "
                   "15–19, {E-122} de los de 20–24 y {E-123} de los de 25–29; a festivales locales, {E-134} de los de "
                   "15–19 y {E-135} de los de 25–29. Frente a Lima Metropolitana, Lima Este va menos a conciertos "
                   "({E-120} frente a {E-128}) y más a festivales locales ({E-130} frente a {E-131}) y bibliotecas "
                   "({E-140} frente a {E-141}).",
         no_permite="Diferencias por distrito.",
         evidencias="E-121; E-122; E-123; E-134; E-135; E-120; E-128; E-130; E-131; E-140; E-141", cambio="Nuevo."),
    dict(id="H2-17", capa=2, dimension="cultura digital", estado="nuevo",
         enunciado="Los videojuegos en línea son más frecuentes entre los más jóvenes: {E-164} a los 15–19 y {E-165} a "
                   "los 25–29.", no_permite="Interés en formatos presenciales.", evidencias="E-164; E-165",
         cambio="Nuevo."),
    dict(id="H2-18", capa=2, dimension="tiempo disponible", estado="nuevo",
         enunciado="En un día registrado de 2024, tuvo al menos 2 horas seguidas sin obligaciones: {E-180} de los "
                   "jóvenes de Lima Este entre 18:00 y 22:00 de un día de semana, {E-183} el sábado entre 18:00 y "
                   "22:00, {E-184} el domingo entre 14:00 y 18:00, {E-182} el sábado entre 14:00 y 18:00 y {E-185} el "
                   "domingo entre 09:00 y 13:00; muchos menos el sábado entre 09:00 y 13:00 ({E-186}) y entre 14:00 y "
                   "18:00 de un día de semana ({E-181}). En Lima Metropolitana, las mujeres tienen menos noches libres en la semana que los hombres ({E-187} "
                   "frente a {E-188}).",
         no_permite="Preferencias de horario; tiempo de traslado.",
         evidencias="E-180; E-183; E-184; E-182; E-186; E-185; E-181; E-187; E-188", cambio="Nuevo."),
    dict(id="H2-19", capa=2, dimension="hogar y cuidado", estado="nuevo",
         enunciado="{E-088} de los jóvenes de Lima Este cuidó a otras personas del hogar en la semana. En Lima "
                   "Metropolitana, {E-089} de las mujeres y {E-090} de los hombres; las mujeres jóvenes que no "
                   "trabajaron ni estudiaron en la semana dedicaron {E-086} al trabajo doméstico y de cuidado (muestra "
                   "pequeña), frente a {E-087} de las que trabajaron o estudiaron.",
         no_permite="Cuidado por sexo en Lima Este.", evidencias="E-088; E-089; E-090; E-086; E-087",
         cambio="Nuevo."),
    dict(id="H2-20", capa=2, dimension="cultura", estado="nuevo",
         enunciado="{E-145} de los jóvenes de Lima Este leyó libros digitales y {E-146} libros impresos en el año; "
                   "{E-140} fue a una biblioteca y {E-142} a una feria del libro.",
         no_permite="Interés en actividades de lectura organizadas.", evidencias="E-145; E-146; E-140; E-142",
         cambio="Nuevo."),
    dict(id="H2-21", capa=2, dimension="cultura", estado="nuevo",
         enunciado="{E-150} de los jóvenes de Lima Este visitó un monumento histórico en el año, {E-151} un museo y "
                   "{E-152} un sitio arqueológico.", no_permite="Si fueron con su colegio, familia o por cuenta propia.",
         evidencias="E-150; E-151; E-152", cambio="Nuevo."),

    # Capa 3: oferta y convocatoria
    dict(id="H3-01", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="De {E-300} actividades publicadas en 2024–2026, {E-301} se dirigen a jóvenes, {E-302} a niños y "
                   "adolescentes (casi siempre de 6 a 17 años) y {E-303} a todo público.",
         no_permite="Que la oferta real sea escasa; ni que haya demanda por lo que falta.",
         evidencias="E-300; E-301; E-302; E-303", cambio=""),
    dict(id="H3-02", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="Lo dirigido a jóvenes se concentra en empleo ({E-306}), participación y voluntariado ({E-307}) y "
                   "preparación preuniversitaria ({E-308}); hay poco en arte y cultura ({E-315}), deporte ({E-309}), "
                   "salud ({E-310}), emprendimiento ({E-311}) y tecnología ({E-312}).",
         no_permite="Interés de los jóvenes por esos temas (la frecuencia de oferta no es interés).",
         evidencias="E-306; E-307; E-308; E-315; E-309; E-310; E-311; E-312", cambio=""),
    dict(id="H3-03", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="Deporte ({E-313}) y arte y cultura ({E-314}) son los temas más ofrecidos, sobre todo para niños y "
                   "adolescentes o todo público; hay espacios deportivos nuevos o reabiertos.",
         no_permite="Uso real de los espacios.", evidencias="E-313; E-314",
         c3="C3-009; C3-051; C3-054; C3-114; C3-120", cambio=""),
    dict(id="H3-04", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="La oferta publicada es casi toda gratuita ({E-304} de {E-300}) y presencial ({E-305}). Lo pagado "
                   "son talleres de verano, escuelas deportivas y academias preuniversitarias.",
         no_permite="Disposición a pagar.", evidencias="E-304; E-300; E-305", c3="C3-006; C3-123; C3-114",
         cambio=""),
    dict(id="H3-05", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Preparación preuniversitaria con participación declarada: {C3-070} matriculados en la academia "
                   "municipal gratuita de Lurigancho-Chosica, {C3-046} becarios de Muni Becas (El Agustino), {C3-096} "
                   "becas Beca2 (SJL), {C3-080} asistentes a una feria vocacional (estudiantes y vecinos) y {C3-006} "
                   "ingresantes de la academia pagada de Ate (resultado, no convocatoria).",
         no_permite="Comparar entre distritos ni con la población.", evidencias="",
         c3="C3-070; C3-046; C3-096; C3-080; C3-006; C3-123; C3-099; C3-141", cambio=""),
    dict(id="H3-06", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="En el concurso de becas de la academia municipal de Santa Anita (2024), más de {C3-125} jóvenes "
                   "compitieron por 10 becas. Es demanda por esa beca gratuita específica.",
         no_permite="Interés general por la formación (C3-D9).", evidencias="", c3="C3-125", cambio=""),
    dict(id="H3-07", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Empleabilidad juvenil con resultados declarados pequeños: {C3-003} jóvenes con empleo por 'Mi "
                   "Primera Chamba' (Ate), {C3-090} aprobados en un programa del CEBA de SJL, {C3-094} contratados tras "
                   "capacitación dual (SJL).", no_permite="Tasa de inserción ni comparación entre programas.",
         evidencias="", c3="C3-003; C3-090; C3-094; C3-105", cambio=""),
    dict(id="H3-08", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Los talleres juveniles gratuitos de SENAJU (arte, desarrollo y empleabilidad; 15–29) tuvieron más "
                   "de {C3-084} inscritos en 2024 para una meta de casi mil, en cinco sedes de Lima (una en SJL) y "
                   "talleres virtuales nacionales.", no_permite="Demanda en Lima Este por separado.", evidencias="",
         c3="C3-084", cambio=""),
    dict(id="H3-09", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Ferias y bolsas de empleo en cinco distritos ofrecen cientos o miles de vacantes; la asistencia se "
                   "describe como 'cientos' o 'miles' de vecinos de todas las edades.",
         no_permite="Cuántos jóvenes asisten.", evidencias="", c3="C3-044; C3-083; C3-093; C3-102; C3-135",
         cambio=""),
    dict(id="H3-10", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Una hackathon municipal en SJL (2025, mayores de 18) reunió {C3-100} inscripciones de jóvenes, "
                   "líderes vecinales, profesionales y emprendedores de varios distritos.",
         no_permite="Generalizar a otras actividades tecnológicas; separar a los jóvenes.", evidencias="",
         c3="C3-100", cambio=""),
    dict(id="H3-11", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Las cifras de participación más altas son de actividades para niños y adolescentes: {C3-051} "
                   "participantes en talleres deportivos de La Molina (2024) y la Academia IPD (6–17), que agotó "
                   "{C3-121} cupos en Lima Metropolitana.", no_permite="Generalizar a la juventud (decisión del "
                                                                         "equipo).",
         evidencias="", c3="C3-051; C3-079; C3-137; C3-121", cambio=""),
    dict(id="H3-13", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="Existe oferta de cultura urbana y juvenil (Urban Fest, Festi Rock, Cultura Urbana Fest, "
                   "FestiJoven, talleres de BMX), pero ninguna nota informa cuántos jóvenes asistieron. Un festival "
                   "intercultural en SJL reunió {C3-103} vecinos de todas las edades.",
         no_permite="Capacidad de convocatoria juvenil de estos eventos.", evidencias="",
         c3="C3-073; C3-091; C3-098; C3-103; C3-127; C3-136; C3-035", cambio=""),
    dict(id="H3-14", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="La oferta de salud mental y prevención llega sobre todo por colegios (charlas con hasta {C3-017} "
                   "estudiantes por colegio); para jóvenes hay una campaña de salud en SJL y un taller de autoestima, "
                   "sin cifras.", no_permite="Convocatoria voluntaria (las charlas escolares son de público cautivo).",
         evidencias="", c3="C3-017; C3-027; C3-037; C3-087; C3-113", cambio=""),
    dict(id="H3-15", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="No se encontró ninguna actividad publicada de videojuegos ni de creación audiovisual para jóvenes; "
                   "el cine aparece como 'Cine en tu Barrio' para familias y cine inclusivo.",
         no_permite="Que haya demanda (la ausencia de oferta no es demanda).", evidencias="", c3="C3-024; C3-097",
         cambio=""),
    dict(id="H3-16", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="En voluntariado y participación, las cifras son pequeñas o sin desglose por edad: {C3-011} "
                   "jóvenes en Minka Joven (Ate), {C3-072} voluntarios de edad no indicada (Chosica), {C3-119} "
                   "participantes de Lima y Callao en Defensores del Patrimonio.",
         no_permite="Interés por el voluntariado en general.", evidencias="", c3="C3-011; C3-072; C3-108; C3-119",
         cambio=""),
    dict(id="H3-17", capa=3, dimension="oferta", estado="sin cambios",
         enunciado="Hay espacios que podrían acoger actividades: Casa de la Juventud (Santa Anita), complejos del IPD, "
                   "clubes metropolitanos, Agencia Local de Empleo y coworking de SJL, CETPRO de La Molina.",
         no_permite="Disponibilidad real ni condiciones de uso.", evidencias="",
         c3="C3-009; C3-064; C3-075; C3-093; C3-111; C3-114; C3-120; C3-124; C3-145", cambio=""),
    dict(id="H3-18", capa=3, dimension="visibilidad", estado="sin cambios",
         enunciado="La visibilidad de la oferta es muy desigual: Chaclacayo publicó {E-320} en 2024–2026 y SJL {E-321} "
                   "en 2024; la oferta de organizaciones sociales casi no aparece.",
         no_permite="Comparar la oferta real entre distritos.", evidencias="E-320; E-321", cambio=""),
    dict(id="H3-19", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="En emprendimiento juvenil las cifras son vagas o no son de jóvenes: ferias de jóvenes "
                   "emprendedores sin cifras (Santa Anita) y {C3-064} alumnos de 14 a 60 años en el CETPRO de La "
                   "Molina.", no_permite="Convocatoria de jóvenes a emprendimiento.", evidencias="",
         c3="C3-132; C3-064", cambio=""),
    dict(id="H3-20", capa=3, dimension="convocatoria", estado="sin cambios",
         enunciado="Deporte dirigido a jóvenes con cifras: solo el taller de tiro con arco de La Molina ({C3-053} "
                   "alumnos por horario). Una carrera abierta a todas las edades reunió más de {C3-081} participantes.",
         no_permite="Convocatoria de jóvenes de 18–29 a deporte organizado.", evidencias="", c3="C3-053; C3-081; "
                                                                                              "C3-133",
         cambio=""),
    dict(id="H3-21", capa=3, dimension="oferta", estado="nuevo",
         enunciado="Hay ferias del libro en Ate, La Molina, Lurigancho-Chosica y SJL (todo público, sin cifras de "
                   "asistencia) y actividades de lectura en colegios ({C3-107} participantes en SJL).",
         no_permite="Asistencia juvenil a ferias del libro.", evidencias="",
         c3="C3-013; C3-065; C3-082; C3-104; C3-055; C3-107", cambio="Nuevo."),
    dict(id="H3-22", capa=3, dimension="oferta", estado="nuevo",
         enunciado="La oferta de patrimonio es sobre todo escolar o para todo público: {C3-019} participantes en "
                   "juegos en sitios arqueológicos (adolescentes) y {C3-076} asistentes a Cajamarquilla Raymi (todas "
                   "las edades).", no_permite="Convocatoria de jóvenes de 18–29.", evidencias="",
         c3="C3-019; C3-076; C3-119", cambio="Nuevo."),
]
# H3-12 (Academia IPD) se integra en H3-11; en la primera versión eran dos hallazgos.
HALLAZGOS_RETIRADOS = {"H3-12": "Integrado en H3-11 (ambos describen convocatoria de niños y adolescentes)."}

# ---------------------------------------------------------------------------------------------------------------
# PATRONES: dato observado -> interpretación -> lo que no permite afirmar (hipótesis)
PATRONES = [
    dict(id="PT-01", tipo="patrón", tema="Acceso a estudios superiores",
         dato="{E-023} de los jóvenes de 15–24 no estudia y su nivel máximo es secundaria completa; para un tercio "
              "el motivo principal es económico ({E-025}) y para otro tercio el trabajo ({E-026}). Las academias y "
              "becas municipales gratuitas publican participación con cifras y una beca tuvo más postulantes que "
              "cupos.",
         interpretacion="Hay un segmento grande en situación compatible con la educación superior, frenado sobre todo "
                        "por dinero y trabajo según su propia respuesta.",
         no_permite="Que quieran continuar estudios: ninguna fuente lo pregunta.",
         hallazgos="H1-17; H2-12; H3-05; H3-06", evidencias="E-023; E-025; E-026"),
    dict(id="PT-02", tipo="brecha", tema="Edad",
         dato="{E-302} de las {E-300} actividades publicadas son para niños y adolescentes y {E-301} para jóvenes. "
              "Las prácticas cambian con la edad: los conciertos son de 20–29 ({E-122}, {E-123}) más que de 15–19 "
              "({E-121}); los videojuegos en línea, de 15–19 ({E-164}) más que de 25–29 ({E-165}).",
         interpretacion="La oferta visible no sigue el perfil de edad de las prácticas juveniles.",
         no_permite="Que los jóvenes de 18–29 quieran actividades organizadas (brecha no es demanda).",
         hallazgos="H3-01; H2-16; H2-17", evidencias="E-302; E-300; E-301; E-122; E-123; E-121; E-164; E-165"),
    dict(id="PT-03", tipo="brecha", tema="Deporte",
         dato="{E-170} hizo deporte o ejercicio en la semana; en Lima Metropolitana, {E-171} de los hombres y {E-172} "
              "de las mujeres. Hay {E-219} organizaciones juveniles acreditadas de deporte, la oferta deportiva "
              "publicada se dirige sobre todo a 6–17 años y para 18–29 hay un solo dato de participación.",
         interpretacion="Una práctica de alcance amplio sin evidencia de convocatoria a formatos organizados para "
                        "18–29.",
         no_permite="Que la menor práctica de las mujeres sea demanda insatisfecha; que haya interés en ligas.",
         hallazgos="H2-02; H1-02; H3-03; H3-11; H3-20", evidencias="E-170; E-171; E-172; E-219"),
    dict(id="PT-04", tipo="patrón", tema="Cultura gratuita y local",
         dato="Lima Este va más que Lima Metropolitana a festivales locales ({E-130} frente a {E-131}) y bibliotecas "
              "({E-140} frente a {E-141}), casi siempre gratis ({E-132}, {E-148}), y menos a conciertos ({E-120} "
              "frente a {E-128}), casi siempre pagados ({E-124}). En el cine, {E-113} tuvo la entrada pagada por otra "
              "persona.",
         interpretacion="En Lima Este pesan las prácticas culturales gratuitas y cercanas; el dinero limita las "
                        "pagadas.",
         no_permite="Que un evento gratuito organizado por terceros convoque a jóvenes (no hay datos de asistencia "
                    "juvenil).", hallazgos="H2-16; H2-10; H2-09; H3-13",
         evidencias="E-130; E-131; E-140; E-141; E-132; E-148; E-120; E-128; E-124; E-113"),
    dict(id="PT-05", tipo="patrón", tema="Digital",
         dato="Pantallas ({E-167}) y video por internet ({E-166}) son casi universales; {E-032} de los usuarios usa "
              "internet para aprender; la mitad de los hombres juega en línea ({E-160}). La oferta tecnológica para "
              "jóvenes es mínima ({E-312} actividades) y tiene un solo dato de convocatoria (hackathon).",
         interpretacion="Lo digital es un entorno cotidiano, no un indicador de interés en actividades digitales "
                        "organizadas.", no_permite="Que la ausencia de oferta de videojuegos sea demanda.",
         hallazgos="H2-01; H2-08; H2-11; H3-10; H3-15", evidencias="E-167; E-166; E-032; E-160; E-312"),
    dict(id="PT-06", tipo="brecha", tema="Mujeres jóvenes",
         dato="Más mujeres que hombres no estudian ni trabajan ({E-044} frente a {E-045}), sobre todo por dedicarse al "
              "hogar ({E-070} de todas las mujeres jóvenes). Se sienten más inseguras de noche ({E-101} frente a "
              "{E-102}) y evitan más salir de noche ({E-104} frente a {E-105}). En cultura participan igual o más que "
              "los hombres (cine: {E-111} frente a {E-112}).",
         interpretacion="Las barreras de las mujeres jóvenes son sobre todo de tiempo, cuidado y seguridad; no de "
                        "falta de práctica cultural.",
         no_permite="Qué actividades quieren; la magnitud de su salud mental en Lima Este.",
         hallazgos="H1-07; H1-15; H1-16; H1-10; H2-08; H2-19",
         evidencias="E-044; E-045; E-070; E-101; E-102; E-104; E-105; E-111; E-112"),
    dict(id="PT-07", tipo="patrón", tema="Participación",
         dato="La participación en asociaciones es muy baja en Lima Metropolitana ({E-220}); SJL tiene {E-222} "
              "organizaciones acreditadas por 10 000 jóvenes (mediana metropolitana: {E-223}); el voluntariado llega "
              "sobre todo a estudiantes ({E-228}) y mujeres ({E-227}).",
         interpretacion="La participación organizada es un objetivo institucional con poca base de práctica medida.",
         no_permite="Interés de los jóvenes por participar.", hallazgos="H1-02; H1-03; H1-04; H1-12; H3-16",
         evidencias="E-220; E-222; E-223; E-228; E-227"),
    dict(id="PT-08", tipo="condición transversal", tema="Tiempo",
         dato="Las ventanas con 2 horas seguidas sin obligaciones son la noche de los días de semana ({E-180}), la "
              "noche del sábado ({E-183}) y la tarde del domingo ({E-184}); las mañanas de fin de semana y las tardes "
              "de semana tienen menos ({E-186}, {E-181}). {E-040} de los jóvenes estudia y trabaja; la falta de "
              "tiempo es el segundo motivo para no ir al cine ({E-116}).",
         interpretacion="La disponibilidad observada se concentra en noches y en la tarde del domingo.",
         no_permite="Horarios preferidos: es disponibilidad observada en un día, no preferencia.",
         hallazgos="H2-18; H2-06; H2-09; H1-19", evidencias="E-180; E-183; E-184; E-186; E-181; E-040; E-116"),
    dict(id="PT-09", tipo="condición transversal", tema="Seguridad",
         dato="{E-100} se siente inseguro caminando solo de noche por su barrio ({E-101} de las mujeres); {E-103} dejó "
              "o evitó salir de noche en el último año ({E-104} de las mujeres).",
         interpretacion="Las ventanas de tiempo libre (noches) coinciden con el horario que más inseguridad genera.",
         no_permite="Qué horarios o lugares evitan concretamente; inseguridad por distrito.",
         hallazgos="H1-10; H2-18", evidencias="E-100; E-101; E-103; E-104"),
    dict(id="PT-10", tipo="condición transversal", tema="Costo",
         dato="El dinero es el motivo principal de no estudiar para {E-025} de quienes tienen solo secundaria "
              "completa y de no ir a conciertos para {E-125}; la oferta publicada es casi toda gratuita ({E-304} de "
              "{E-300}) y las cuatro señales de demanda observadas son de ofertas gratuitas.",
         interpretacion="La gratuidad parece una condición de acceso, no un atributo diferencial.",
         no_permite="Disposición a pagar.", hallazgos="H1-17; H2-09; H3-04; H3-06; H3-08",
         evidencias="E-025; E-125; E-304; E-300"),
    dict(id="PT-11", tipo="condición transversal", tema="Información y visibilidad",
         dato="La falta de información es un motivo para no ir a ferias del libro ({E-144}); la oferta municipal es "
              "poco visible en internet (Chaclacayo: {E-320} en 2024–2026); {E-242} de la generación Z tenía cuenta "
              "en TikTok (Ipsos, 2021–2022).",
         interpretacion="La difusión no puede depender de las notas municipales.",
         no_permite="Qué canales usan los jóvenes de Lima Este hoy.", hallazgos="H2-09; H3-18; H2-15",
         evidencias="E-144; E-320; E-242"),
    dict(id="PT-12", tipo="condición transversal", tema="Adolescentes y protección",
         dato="Los nacimientos de madres de 15–19 bajaron de {E-208} (2019) a {E-207} (2025), con tasas sobre la "
              "mediana en El Agustino, Santa Anita y Ate; {E-205} de las víctimas atendidas por los CEM tiene 15–19.",
         interpretacion="Las necesidades registradas se concentran en adolescentes; toda actividad con menores de 18 "
                        "necesita protocolos de protección y derivación.",
         no_permite="Prevalencia (los registros dependen del acceso a servicios).", hallazgos="H1-13; H1-14",
         evidencias="E-208; E-207; E-205"),
    dict(id="PT-13", tipo="brecha", tema="Hogar y cuidado",
         dato="{E-070} de las mujeres de 15–29 no estudia ni trabaja y se dedica al hogar; {E-076} de ellas vive con "
              "niños de 0 a 5 años. {E-088} de los jóvenes cuidó a alguien del hogar en la semana. Ninguna actividad "
              "publicada se dirige a este grupo.",
         interpretacion="Es el segmento más grande que ni la oferta visible ni la primera integración cubrían.",
         no_permite="Qué actividad les sería útil: no hay datos de sus intereses ni disponibilidad.",
         hallazgos="H1-16; H1-15; H2-19", evidencias="E-070; E-076; E-088"),
]

# ---------------------------------------------------------------------------------------------------------------
# SEGMENTOS: a quién aplica cada ficha y qué tamaño tiene
SEGMENTOS = [
    dict(id="S-01", nombre="Jóvenes de 15–24 que no estudian y cuyo nivel máximo es secundaria completa",
         evidencia="E-023", fichas="F-01"),
    dict(id="S-02", nombre="Ídem, con problemas económicos como motivo principal", evidencia="E-024", fichas="F-01"),
    dict(id="S-03", nombre="Jóvenes sin trabajo que buscan o quieren trabajar", evidencia="E-049", fichas="F-02"),
    dict(id="S-04", nombre="Jóvenes que buscan trabajo (desocupados)", evidencia="E-048", fichas="F-02"),
    dict(id="S-05", nombre="Jóvenes ocupados con empleo informal (2022–2023)", evidencia="E-057", fichas="F-03"),
    dict(id="S-06", nombre="Jóvenes que trabajan por cuenta propia o como empleadores", evidencia="E-059",
         fichas="F-04"),
    dict(id="S-07", nombre="Jóvenes que hicieron deporte o ejercicio en la semana", evidencia="E-170", fichas="F-05"),
    dict(id="S-08", nombre="Jóvenes que fueron a un festival local o tradicional en el año", evidencia="E-130",
         fichas="F-06"),
    dict(id="S-09", nombre="Jóvenes que fueron a un concierto o festival musical en el año", evidencia="E-120",
         fichas="F-06"),
    dict(id="S-10", nombre="Jóvenes que fueron al cine en el año", evidencia="E-110", fichas="F-07"),
    dict(id="S-11", nombre="Jóvenes que fueron a una feria del libro en el año", evidencia="E-142", fichas="F-08"),
    dict(id="S-12", nombre="Jóvenes que fueron a una biblioteca en el año", evidencia="E-140", fichas="F-08"),
    dict(id="S-13", nombre="Jóvenes que visitaron un monumento histórico en el año", evidencia="E-150",
         fichas="F-09"),
    dict(id="S-14", nombre="Hombres jóvenes que juegan videojuegos en línea", evidencia="E-160", fichas="F-10"),
    dict(id="S-15", nombre="Mujeres de 15–29 que no estudian ni trabajan y se dedican al hogar", evidencia="E-070",
         fichas="F-15"),
    dict(id="S-16", nombre="Jóvenes que estudian y trabajan", evidencia="E-040", fichas="(condición de tiempo)"),
    dict(id="S-17", nombre="Jóvenes que no estudian ni trabajan (definición del proyecto)", evidencia="E-043",
         fichas="F-02; F-15"),
    dict(id="S-18", nombre="Jóvenes que dejaron o evitaron salir de noche por temor a la delincuencia",
         evidencia="E-103", fichas="(condición de seguridad)"),
]

# ---------------------------------------------------------------------------------------------------------------
# FICHAS
# Convocatoria: cada registro indica la comparabilidad con la actividad de la ficha (sí / parcial / no) en
# segmento, territorio, formato y costo. El código lo calcula el constructor a partir del registro de la Capa 3.
def conv(c3, segmento, territorio, formato, costo, nota=""):
    return dict(c3=c3, segmento=segmento, territorio=territorio, formato=formato, costo=costo, nota=nota)


FICHAS = [
    dict(
        id="F-01", linea="Educación y acceso a estudios superiores",
        actividad="Preparación gratuita para el ingreso a la educación superior",
        tipo="intervención segmentada", origen="P01", resultado="B: reformulada",
        segmentos="S-01; S-02",
        necesidad=[dict(tipo="brecha de acceso", evidencias="E-023; E-025; E-026",
                        texto="{E-023} de los jóvenes de 15–24 de Lima Este no estudia y su nivel máximo es secundaria "
                              "completa. Entre ellos, {E-025} menciona problemas económicos como motivo principal y "
                              "{E-026} que está trabajando.")],
        poblacion="Jóvenes de 15–24 sin estudios en curso y con secundaria completa: {E-023:personas}. Con motivo "
                  "económico: {E-024} de los jóvenes de 15–24 ({E-024:personas}).",
        interes=[dict(codigo="P0", evidencias="E-027; E-028",
                      texto="Ninguna fuente mide la intención de continuar estudios ni de prepararse. La respuesta "
                            "'terminó sus estudios o asiste a academia' ({E-027}; {E-028} a los 16–19) mezcla a quienes "
                            "ya se preparan con quienes dieron por terminados sus estudios.")],
        salto="De 'no estudia y tiene secundaria completa' a 'quiere prepararse para postular'.",
        alcance=dict(tipo="segmento identificable", evidencias="E-023; E-024"),
        oferta=dict(texto="Academias preuniversitarias municipales en Lurigancho-Chosica (gratuita), Ate y Santa Anita "
                          "(pagadas); becas municipales de preparación en El Agustino y Santa Anita; becas integrales "
                          "en SJL; ferias vocacionales en Lurigancho-Chosica y Santa Anita.",
                    c3="C3-070; C3-006; C3-123; C3-046; C3-125; C3-096; C3-080; C3-141; C3-099"),
        convocatoria=[
            conv("C3-070", "sí", "sí", "sí", "sí", "{C3-070} matriculados en la academia municipal gratuita (2024)."),
            conv("C3-046", "sí", "sí", "parcial", "sí", "{C3-046} becarios de preparación preuniversitaria (2025)."),
            conv("C3-125", "sí", "sí", "sí", "sí", "Más de {C3-125} postulantes para 10 becas: demanda por esa beca "
                                                    "concreta (C3-D9)."),
            conv("C3-123", "sí", "sí", "sí", "no", "'Aulas completas' en la academia pagada (sin cifra)."),
            conv("C3-080", "parcial", "sí", "parcial", "sí", "{C3-080} asistentes a una feria vocacional (estudiantes "
                                                              "y vecinos)."),
        ],
        barreras=[
            dict(pertinencia="directa", evidencias="E-025", c3="C3-123",
                 texto="Dinero: {E-025} de quienes no estudian con secundaria completa menciona problemas económicos; "
                       "algunas academias municipales son pagadas."),
            dict(pertinencia="directa", evidencias="E-026; E-180; E-184",
                 texto="Trabajo y tiempo: {E-026} está trabajando. La disponibilidad observada es mayor en la noche de "
                       "los días de semana ({E-180}) y la tarde del domingo ({E-184})."),
            dict(pertinencia="indirecta", evidencias="E-030",
                 texto="Desplazamiento: {E-030} de quienes estudian a los 20–24 lo hace en otro distrito (mide "
                       "movilidad existente, no una barrera)."),
        ],
        vacios=["Intención de continuar estudios y carrera de interés.",
                "Cuántos ya asisten a una academia (la ENAHO no lo separa de 'terminó sus estudios').",
                "Capacidad de pago y distancia aceptable.",
                "Resultados de las academias municipales: solo hay un dato ({C3-006} ingresantes en Ate)."],
        afirmaciones=[
            dict(texto="Un segmento identificable de jóvenes de 15–24 no estudia y solo tiene secundaria completa "
                       "({E-023}; {E-023:personas}).", evidencias="E-023"),
            dict(texto="Para un tercio de ese segmento el motivo principal es económico ({E-025}).",
                 evidencias="E-025"),
            dict(texto="Hay participación declarada con cifras en academias y becas municipales gratuitas de Lima Este "
                       "y una beca concreta tuvo más postulantes que cupos.", evidencias="", c3="C3-070; C3-046; C3-125"),
        ],
        hipotesis=["Que una preparación gratuita atraiga a jóvenes que hoy no se preparan, y no solo a quienes ya "
                   "asisten a otra academia.",
                   "Que el apoyo para postular a becas convoque por sí mismo.",
                   "Que un horario nocturno o de domingo permita participar a quienes trabajan."],
        componentes=[
            ("Preparación gratuita para el examen de admisión", "respaldado",
             "Necesidad (brecha de acceso) y convocatoria (participación con cifras y una demanda observada) "
             "documentadas; interés no medido."),
            ("Apoyo para postular a becas", "respaldado parcialmente",
             "Demanda observada por una beca concreta, que no se generaliza (C3-D9)."),
            ("Orientación vocacional", "sin evidencia suficiente",
             "Solo una feria con estudiantes y vecinos, sin segmento compatible."),
        ],
        validacion="Inscritos frente a cupos y lista de espera; proporción que no se preparaba en otra academia; "
                   "proporción que trabaja; asistencia a la 4.ª semana; postulaciones a becas e ingresos.",
        donde="Criterio operativo (I-R7): San Juan de Lurigancho no tiene academia municipal gratuita publicada y "
              "tiene la mayor población joven ({E-010}); coordinar con las academias existentes para no duplicar.",
        cambio="Segmento redefinido con un denominador de Lima Este; componentes separados; el interés pasa de "
               "'medio' a P0 (no medido); la necesidad deja de apoyarse en 'no le interesa: 2 %'.",
    ),
    dict(
        id="F-02", linea="Empleo e ingresos",
        actividad="Acompañamiento para la búsqueda de empleo (preparación y conexión con vacantes)",
        tipo="intervención segmentada", origen="P02", resultado="B: reformulada", segmentos="S-03; S-04",
        necesidad=[dict(tipo="prevalencia", evidencias="E-046; E-047; E-048",
                        texto="La tasa de desempleo juvenil en Lima Este es {E-046} ({E-047} a los 15–19); {E-048} de "
                              "todos los jóvenes busca trabajo.")],
        poblacion="Sin trabajo y buscan o quieren trabajar: {E-049} de los jóvenes ({E-049:personas}); {E-050} de las "
                  "mujeres y {E-051} de los hombres.",
        interes=[dict(codigo="P1", evidencias="E-048; E-049",
                      texto="Buscar trabajo es una práctica observada en este segmento (lo define), pero ninguna fuente "
                            "mide interés en talleres o acompañamiento.")],
        salto="De buscar trabajo a asistir a una preparación o a un acompañamiento.",
        alcance=dict(tipo="segmento identificable", evidencias="E-049"),
        oferta=dict(texto="Programas municipales de empleabilidad (Ate, SJL, Santa Anita), ferias y bolsas de empleo en "
                          "cinco distritos, Agencia Local de Empleo y Centro de Empleo del MTPE en SJL.",
                    c3="C3-003; C3-090; C3-094; C3-105; C3-126; C3-044; C3-083; C3-093; C3-102; C3-135; C3-111"),
        convocatoria=[
            conv("C3-003", "sí", "sí", "parcial", "sí", "{C3-003} jóvenes con empleo (resultado declarado)."),
            conv("C3-090", "sí", "sí", "sí", "sí", "{C3-090} aprobados en un programa de empleabilidad."),
            conv("C3-094", "sí", "sí", "parcial", "sí", "{C3-094} jóvenes contratados tras capacitación dual."),
            conv("C3-084", "sí", "parcial", "parcial", "sí", "Talleres de SENAJU con más de {C3-084} inscritos para "
                                                              "casi mil cupos (Lima y nacional; incluyen arte)."),
            conv("C3-102", "no", "sí", "parcial", "sí", "Ferias de empleo con 'cientos' o 'miles' de vecinos de todas "
                                                         "las edades."),
        ],
        barreras=[
            dict(pertinencia="indirecta", evidencias="E-180; E-100",
                 texto="Horario y seguridad: la disponibilidad se concentra en las noches ({E-180}), cuando {E-100} se "
                       "siente inseguro caminando por su barrio."),
            dict(pertinencia="directa", evidencias="E-054; E-055",
                 texto="Entre las mujeres que no estudian ni trabajan, la mayoría se dedica al hogar ({E-054}) y pocas "
                       "buscan trabajo ({E-055}): un taller de búsqueda de empleo no responde a su situación."),
        ],
        vacios=["Qué apoyo buscan (preparación, contactos, información).",
                "Si ya usan bolsas o centros de empleo.", "Tasas de inserción de los programas existentes."],
        afirmaciones=[
            dict(texto="{E-049} de los jóvenes de Lima Este no tiene trabajo y busca o quiere trabajar "
                       "({E-049:personas}).", evidencias="E-049"),
            dict(texto="Los programas municipales de empleabilidad publican cifras pequeñas y declaradas; los talleres "
                       "gratuitos de SENAJU tuvieron más inscritos que cupos a escala de Lima y el país.",
                 evidencias="", c3="C3-003; C3-090; C3-094; C3-084"),
        ],
        hipotesis=["Que quienes buscan trabajo acudan a una preparación además de las ferias y bolsas existentes.",
                   "Que la conexión con vacantes concretas aumente la asistencia."],
        componentes=[
            ("Preparación para buscar empleo (CV, entrevista, bolsas en línea)", "respaldado parcialmente",
             "Necesidad y segmento documentados; convocatoria con cifras pequeñas; interés no medido."),
            ("Conexión con vacantes", "complementario", "Ya existe como ferias, bolsas y centros de empleo."),
            ("Prioridad a mujeres que no estudian ni trabajan", "retirado",
             "La mayoría se dedica al hogar y no busca trabajo; ver F-15."),
        ],
        validacion="Inscritos frente a cupos; proporción que busca trabajo; asistencia; postulaciones y contrataciones "
                   "a tres meses.",
        donde="Criterio operativo: donde ya funcionan la Agencia Local de Empleo y el Centro de Empleo (SJL).",
        cambio="Necesidad medida en Lima Este (antes, Lima Metropolitana); segmento = sin trabajo y busca o quiere "
               "trabajar; se retira la prioridad a mujeres NINI.",
    ),
    dict(
        id="F-03", linea="Empleo e ingresos",
        actividad="Derechos laborales y formalización para jóvenes que ya trabajan",
        tipo="intervención segmentada", origen="Nueva", resultado="Nueva", segmentos="S-05",
        necesidad=[dict(tipo="prevalencia", evidencias="E-056; E-057",
                        texto="{E-056} de los jóvenes ocupados de Lima Este tiene empleo informal (2022–2023), "
                              "equivalente a {E-057} de todos los jóvenes.")],
        poblacion="Jóvenes con empleo informal: {E-057:personas}.",
        interes=[dict(codigo="P0", evidencias="", texto="Ninguna fuente mide interés en información sobre derechos "
                                                          "laborales o formalización.")],
        salto="De tener un empleo informal a querer información o apoyo para formalizarse.",
        alcance=dict(tipo="segmento identificable", evidencias="E-057"),
        oferta=dict(texto="Un encuentro sobre formalización laboral en La Molina (UNALM) y un programa de inserción "
                          "laboral en El Agustino.", c3="C3-061; C3-042"),
        convocatoria=[conv("C3-061", "sí", "sí", "sí", "sí", "Encuentro con asistentes sin número exacto.")],
        barreras=[dict(pertinencia="directa", evidencias="E-061; E-180; E-184",
                       texto="Tiempo: quienes trabajan dedican {E-061} a la semana; sus ventanas libres son la noche "
                             "({E-180}) y la tarde del domingo ({E-184}).")],
        vacios=["Qué problemas laborales enfrentan (no se midió).",
                "Informalidad de 2024–2025 (el INEI dejó de publicar la variable).",
                "Si conocerían o usarían esa información."],
        afirmaciones=[dict(texto="La informalidad afecta a {E-056} de los jóvenes ocupados de Lima Este (2022–2023).",
                           evidencias="E-056")],
        hipotesis=["Que jóvenes con empleo informal asistan a una actividad sobre derechos laborales o formalización.",
                   "Que un formato breve, de noche o en domingo, sea compatible con su jornada."],
        componentes=[("Información sobre derechos laborales y formalización", "necesidad documentada",
                      "Interés y convocatoria sin evidencia.")],
        validacion="Inscritos; proporción con empleo informal; asistencia; consultas o trámites iniciados después.",
        donde="Sin criterio de demanda por distrito.",
        cambio="Alternativa nueva: surge de la informalidad estimada para Lima Este.",
    ),
    dict(
        id="F-04", linea="Empleo e ingresos",
        actividad="Apoyo a jóvenes que ya trabajan por cuenta propia",
        tipo="intervención segmentada", origen="P09", resultado="C tal como estaba; reformulada para un segmento",
        segmentos="S-06",
        necesidad=[dict(tipo="sin evidencia", evidencias="",
                        texto="Trabajar por cuenta propia no es por sí mismo una necesidad; no tenemos datos de "
                              "ingresos ni de problemas de estos negocios.")],
        poblacion="{E-059} de los jóvenes ({E-059:personas}); {E-058} de los ocupados.",
        interes=[dict(codigo="P1", evidencias="E-058; E-231; E-240; E-241",
                      texto="Práctica observada: ya trabajan por cuenta propia ({E-058} de los ocupados); {E-231} de los "
                            "usuarios de internet lo usa para vender. La aspiración a emprender solo se midió en "
                            "2019–2020 fuera de Lima Este ({E-240}; {E-241}).")],
        salto="De trabajar por cuenta propia a querer capacitarse en gestión o ventas.",
        alcance=dict(tipo="segmento identificable", evidencias="E-059"),
        oferta=dict(texto="Ferias de jóvenes emprendedores (Santa Anita), CETPRO de La Molina, capacitación de "
                          "Jóvenes Productivos, coworking municipal en SJL.",
                    c3="C3-132; C3-064; C3-041; C3-111"),
        convocatoria=[conv("C3-132", "sí", "sí", "parcial", "sí", "Ferias con 'muchos jóvenes emprendedores', sin "
                                                                  "cifra."),
                      conv("C3-064", "no", "sí", "parcial", "no indica", "{C3-064} alumnos de 14 a 60 años.")],
        barreras=[dict(pertinencia="indirecta", evidencias="E-061",
                       texto="Tiempo: quienes trabajan dedican {E-061} a la semana.")],
        vacios=["Tipo de negocio, ingresos y problemas.", "Interés en capacitación o apoyo.",
                "Aspiración reciente a emprender en Lima Este."],
        afirmaciones=[dict(texto="{E-059} de los jóvenes de Lima Este trabaja por cuenta propia o como empleador "
                                 "({E-059:personas}).", evidencias="E-059")],
        hipotesis=["Que jóvenes con negocio propio quieran y puedan asistir a un apoyo para sus negocios."],
        componentes=[
            ("Promover el emprendimiento en general", "descartado",
             "La informalidad no demuestra necesidad de emprender y la aspiración solo se midió en 2019–2020 fuera de "
             "Lima Este."),
            ("Apoyo a quienes ya trabajan por cuenta propia", "segmento documentado",
             "Necesidad, interés y convocatoria por medir."),
            ("Ventas por internet", "sin evidencia", "Pocos usan internet para vender; no se sabe si quieren hacerlo."),
        ],
        validacion="Inscritos con negocio en marcha; asistencia; cambios declarados en el negocio.",
        donde="Sin criterio de demanda por distrito.",
        cambio="El salto 'informalidad → emprendimiento' se descarta; la ficha se limita a un segmento con práctica "
               "observada.",
    ),
    dict(
        id="F-05", linea="Deporte y actividad física",
        actividad="Deporte organizado para jóvenes de 18–29 (ligas, torneos, entrenamiento)",
        tipo="actividad de convocatoria abierta", origen="P04", resultado="B: reformulada", segmentos="S-07",
        necesidad=[dict(tipo="sin evidencia", evidencias="",
                        texto="No hay datos de actividad física insuficiente ni de salud física juvenil en nuestras "
                              "fuentes.")],
        poblacion="Jóvenes de 18–29 (la oferta deportiva publicada se dirige a 6–17); la práctica se mide para 15–29.",
        interes=[dict(codigo="P1", evidencias="E-170; E-173; E-171; E-172",
                      texto="{E-170} hizo deporte o ejercicio en la semana (2024); {E-173} a los 25–29. En Lima "
                            "Metropolitana, {E-171} de los hombres y {E-172} de las mujeres.")],
        salto="De hacer deporte o ejercicio, en cualquier forma, a inscribirse en una liga o entrenamiento organizado.",
        alcance=dict(tipo="amplia", evidencias="E-170"),
        oferta=dict(texto="Espacios deportivos nuevos o reabiertos; talleres y escuelas para 6–17; taller de tiro con "
                          "arco para jóvenes (La Molina).", c3="C3-009; C3-114; C3-120; C3-054; C3-051; C3-121; C3-053"),
        convocatoria=[conv("C3-053", "sí", "sí", "sí", "no indica", "Unos {C3-053} alumnos por horario."),
                      conv("C3-121", "no", "parcial", "sí", "sí", "Academia IPD (6–17): {C3-121} cupos agotados."),
                      conv("C3-081", "no", "sí", "parcial", "no indica", "Carrera abierta: más de {C3-081} "
                                                                         "participantes de todas las edades.")],
        barreras=[
            dict(pertinencia="directa", evidencias="E-100; E-101; E-104",
                 texto="Seguridad de noche: {E-100} se siente inseguro caminando solo de noche ({E-101} de las mujeres) "
                       "y {E-104} de las mujeres evitó salir de noche."),
            dict(pertinencia="directa", evidencias="E-180; E-184; E-186",
                 texto="Horario: hay más jóvenes disponibles en la noche de semana ({E-180}) y la tarde del domingo "
                       "({E-184}) que en la mañana del sábado ({E-186})."),
        ],
        vacios=["Si practican en ligas informales.", "Interés en un formato organizado.",
                "Deporte por sexo en Lima Este."],
        afirmaciones=[
            dict(texto="Uno de cada cuatro jóvenes de Lima Este hizo deporte o ejercicio en la semana ({E-170}).",
                 evidencias="E-170"),
            dict(texto="La oferta deportiva publicada se dirige sobre todo a 6–17 años; para 18–29 hay un solo dato "
                       "de participación.", evidencias="E-309; E-313", c3="C3-053"),
        ],
        hipotesis=["Que jóvenes de 18–29 que ya practican se inscriban en un formato organizado.",
                   "Que un horario diurno de domingo y espacios seguros permitan participar a más mujeres (su menor "
                   "práctica en Lima Metropolitana no prueba demanda insatisfecha)."],
        componentes=[
            ("Deporte organizado mixto", "práctica relacionada", "Convocatoria con un solo dato comparable."),
            ("Opción para mujeres en horario y espacio seguros", "hipótesis de diseño",
             "Se apoya en barreras medidas (inseguridad nocturna) y en la brecha de práctica de Lima Metropolitana."),
        ],
        validacion="Inscritos por sexo y edad; asistencia y retención; comparación entre horarios.",
        donde="Criterio operativo: espacios nuevos o reabiertos en SJL, Ate y Lurigancho-Chosica.",
        cambio="El interés pasa de 'alto' a P1 (práctica relacionada); la convocatoria deja de llamarse 'baja' y se "
               "describe como un solo dato comparable.",
    ),
    dict(
        id="F-06", linea="Cultura y encuentro",
        actividad="Festival o escenario local gratuito (música, danza y fiestas locales)",
        tipo="actividad de convocatoria abierta", origen="P05 + nueva (festivales locales)",
        resultado="B: reformulada", segmentos="S-08; S-09",
        necesidad=[dict(tipo="sin evidencia", evidencias="", texto="Es una práctica cultural, no una respuesta a una "
                                                                  "necesidad medida.")],
        poblacion="15–29; los conciertos son sobre todo de 20–29 ({E-122}; {E-123}) y poco de 15–19 ({E-121}).",
        interes=[
            dict(codigo="P2", evidencias="E-130; E-131; E-132",
                 texto="Festival local: {E-130} fue a un festival local o tradicional en el año (más que en Lima "
                       "Metropolitana, {E-131}); {E-132} entró gratis."),
            dict(codigo="P1", evidencias="E-120; E-124; E-136; E-137",
                 texto="Música en vivo: {E-120} fue a un concierto (casi siempre con entrada comprada: {E-124}); "
                       "{E-136} fue a danza y {E-137} a una feria artesanal."),
        ],
        salto="De asistir a fiestas locales o conciertos pagados a asistir a un festival juvenil gratuito organizado "
              "por la organización.",
        alcance=dict(tipo="amplia", evidencias="E-130; E-120"),
        oferta=dict(texto="Eventos de cultura urbana y juvenil en Lurigancho-Chosica, Santa Anita y SJL; concurso de "
                          "canto y baile en El Agustino; festival intercultural en SJL; Cajamarquilla Raymi.",
                    c3="C3-073; C3-091; C3-098; C3-127; C3-136; C3-035; C3-103; C3-076"),
        convocatoria=[conv("C3-136", "sí", "sí", "sí", "no indica", "Cultura Urbana Fest: sin cifras de asistencia."),
                      conv("C3-035", "sí", "sí", "parcial", "sí", "Concurso con participantes sin número."),
                      conv("C3-103", "no", "sí", "sí", "sí", "Festival intercultural: {C3-103} vecinos de todas las "
                                                              "edades."),
                      conv("C3-076", "no", "sí", "parcial", "no indica", "{C3-076} asistentes de todas las edades.")],
        barreras=[
            dict(pertinencia="directa", evidencias="E-125; E-126; E-127",
                 texto="Entre quienes no fueron a conciertos: dinero ({E-125}), falta de interés ({E-126}) y falta de "
                       "tiempo ({E-127})."),
            dict(pertinencia="directa", evidencias="E-133", texto="Entre quienes no fueron a festivales, la mayoría "
                                                                 "no tenía interés ({E-133})."),
            dict(pertinencia="directa", evidencias="E-100; E-103; E-183",
                 texto="Noche: la noche del sábado es una ventana libre ({E-183}), pero {E-100} se siente inseguro y "
                       "{E-103} evitó salir de noche."),
        ],
        vacios=["Géneros musicales preferidos.", "Asistencia juvenil a eventos locales (no se publica).",
                "Seguridad percibida en eventos nocturnos."],
        afirmaciones=[
            dict(texto="Uno de cada cinco jóvenes fue a un festival local en el año ({E-130}), casi siempre gratis "
                       "({E-132}).", evidencias="E-130; E-132"),
            dict(texto="Los conciertos son una práctica de 20–29 años más que de 15–19 y casi siempre pagada.",
                 evidencias="E-121; E-122; E-123; E-124"),
        ],
        hipotesis=["Que un festival gratuito organizado para jóvenes convoque a jóvenes, y no solo a familias.",
                   "Que la cultura urbana (freestyle, breaking) tenga público en Lima Este (no se midió).",
                   "Que participar como artistas u organizadores aumente la convocatoria."],
        componentes=[
            ("Festival o escenario local gratuito", "práctica de la misma actividad",
             "Festivales locales medidos en Lima Este; convocatoria juvenil sin cifras."),
            ("Programación de cultura urbana", "sin evidencia", "La encuesta no pregunta por géneros."),
            ("Jóvenes como artistas u organizadores", "sin evidencia",
             "Hay {E-225} organizaciones juveniles acreditadas de cultura y arte como posibles aliadas."),
        ],
        validacion="Asistentes y su edad (registro o conteo); artistas y colectivos inscritos; asistencia a una "
                   "segunda fecha.",
        donde="Criterio operativo: distritos con eventos previos y espacios (Lurigancho-Chosica, Santa Anita, SJL).",
        cambio="Se reorienta a festival local gratuito (práctica de la misma actividad); el segmento 15–24 se corrige "
               "(la música en vivo es de 20–29); cultura urbana y jóvenes organizadores pasan a hipótesis.",
    ),
    dict(
        id="F-07", linea="Cultura y encuentro", actividad="Proyecciones de cine gratuitas",
        tipo="actividad de convocatoria abierta", origen="P06",
        resultado="B: reformulada (se separan componentes sin evidencia)", segmentos="S-10",
        necesidad=[dict(tipo="sin evidencia", evidencias="", texto="Es una práctica cultural, no una respuesta a una "
                                                                  "necesidad medida.")],
        poblacion="15–29; más a los 15–19 ({E-117}) que a los 25–29 ({E-118}); mujeres {E-111}, hombres {E-112}.",
        interes=[dict(codigo="P1", evidencias="E-110; E-113; E-114",
                      texto="{E-110} fue al cine comercial en el año; {E-113} tuvo la entrada pagada por otra persona; "
                            "entre quienes no fueron, {E-114} menciona el dinero.")],
        salto="De ir al cine comercial a ir a una proyección gratuita organizada; ver películas no dice nada sobre "
              "conversar después ni sobre producir video.",
        alcance=dict(tipo="amplia", evidencias="E-110"),
        oferta=dict(texto="'Cine en tu Barrio' (familias, El Agustino) y cine inclusivo (SJL).", c3="C3-024; C3-097"),
        convocatoria=[conv("C3-024", "no", "sí", "sí", "sí", "Proyecciones para familias, sin cifras.")],
        barreras=[dict(pertinencia="directa", evidencias="E-114; E-115; E-116",
                       texto="Entre quienes no fueron al cine: falta de interés ({E-115}), de tiempo ({E-116}) y de "
                             "dinero ({E-114}).")],
        vacios=["Si una proyección gratuita reemplaza o no la salida al cine comercial.", "Qué películas.",
                "Convocatoria de proyecciones juveniles."],
        afirmaciones=[
            dict(texto="Ir al cine es la práctica cultural presencial más extendida ({E-110}).", evidencias="E-110"),
            dict(texto="Para algunos jóvenes el dinero es el motivo de no ir ({E-114}) y cuatro de cada diez "
                       "asistentes no pagaron su entrada ({E-113}).", evidencias="E-114; E-113"),
        ],
        hipotesis=["Que una proyección gratuita convoque a jóvenes que hoy no van al cine por dinero.",
                   "Que haya interés en conversar después de la función (cineforo).",
                   "Que haya interés en producir video."],
        componentes=[
            ("Proyección gratuita", "práctica relacionada", "Alcance amplio; convocatoria juvenil sin evidencia."),
            ("Conversación después de la función (cineforo)", "sin evidencia", "Validar por separado."),
            ("Taller de producción de video", "sin evidencia", "Ver video ({E-166}) no indica interés en producirlo."),
        ],
        validacion="Asistentes por función y su edad; asistencia a la conversación; repetición.",
        donde="Criterio operativo: espacios con pantalla o auditorio.",
        cambio="Se conserva la proyección gratuita; cineforo y taller de video pasan a componentes sin evidencia.",
    ),
    dict(
        id="F-08", linea="Cultura y encuentro", actividad="Actividades juveniles en ferias del libro y bibliotecas",
        tipo="actividad de convocatoria abierta", origen="Nueva", resultado="Nueva", segmentos="S-11; S-12",
        necesidad=[dict(tipo="sin evidencia", evidencias="", texto="Es una práctica cultural, no una respuesta a una "
                                                                  "necesidad medida.")],
        poblacion="15–29.",
        interes=[dict(codigo="P2", evidencias="E-142; E-140; E-141",
                      texto="{E-142} fue a una feria del libro y {E-140} a una biblioteca en el año (más que en Lima "
                            "Metropolitana, {E-141})."),
                 dict(codigo="P1", evidencias="E-145; E-146; E-147",
                      texto="{E-145} leyó libros digitales y {E-146} impresos; en la semana, {E-147} leyó.")],
        salto="De ir a una feria o biblioteca a participar en una actividad juvenil organizada allí (club, "
              "presentación, taller).",
        alcance=dict(tipo="amplia", evidencias="E-142; E-140"),
        oferta=dict(texto="Ferias del libro en Ate, La Molina, Lurigancho-Chosica y SJL (todo público); biblioteca "
                          "municipal de La Molina (escolares); 'Ruta Lectora' en colegios de SJL.",
                    c3="C3-013; C3-065; C3-082; C3-104; C3-055; C3-107"),
        convocatoria=[conv("C3-065", "parcial", "sí", "sí", "sí", "Ferias del libro sin cifras de asistencia."),
                      conv("C3-107", "parcial", "sí", "parcial", "sí", "{C3-107} participantes escolares (público "
                                                                      "cautivo).")],
        barreras=[dict(pertinencia="directa", evidencias="E-144; E-143; E-148",
                       texto="Información: {E-144} de quienes no fueron a ferias del libro no tuvo información oportuna. "
                             "La entrada suele ser libre ({E-143} en ferias; {E-148} en bibliotecas).")],
        vacios=["Interés en clubes de lectura o actividades en bibliotecas.", "Asistencia juvenil a ferias del libro."],
        afirmaciones=[dict(texto="Uno de cada cinco jóvenes fue a una feria del libro ({E-142}) y uno de cada siete a "
                                 "una biblioteca ({E-140}); en bibliotecas, Lima Este supera a Lima Metropolitana.",
                           evidencias="E-142; E-140; E-141")],
        hipotesis=["Que jóvenes asistan a actividades juveniles en ferias o bibliotecas.",
                   "Que una mejor difusión aumente la asistencia (la falta de información es un motivo declarado)."],
        componentes=[("Actividades juveniles en ferias del libro y bibliotecas", "práctica de la misma actividad",
                      "Convocatoria juvenil sin cifras."),
                     ("Club de lectura", "práctica relacionada", "Sin evidencia de convocatoria.")],
        validacion="Asistentes y su edad; repetición; canal por el que se enteraron.",
        donde="Criterio operativo: distritos con ferias del libro y bibliotecas (Ate, La Molina, Lurigancho-Chosica, "
              "SJL).",
        cambio="Alternativa nueva: la primera versión no consideró la lectura.",
    ),
    dict(
        id="F-09", linea="Cultura y encuentro", actividad="Visitas y rutas de patrimonio cultural",
        tipo="actividad de convocatoria abierta", origen="Nueva", resultado="Nueva", segmentos="S-13",
        necesidad=[dict(tipo="sin evidencia", evidencias="", texto="Es una práctica cultural, no una respuesta a una "
                                                                  "necesidad medida.")],
        poblacion="15–29; la oferta publicada es sobre todo escolar.",
        interes=[dict(codigo="P2", evidencias="E-150; E-151; E-152",
                      texto="{E-150} visitó un monumento histórico en el año, {E-151} un museo y {E-152} un sitio "
                            "arqueológico.")],
        salto="De visitar un sitio por cuenta propia, con la familia o el colegio a participar en una ruta organizada.",
        alcance=dict(tipo="amplia", evidencias="E-150"),
        oferta=dict(texto="Juegos en sitios arqueológicos para escolares, Cajamarquilla Raymi (todo público), grupos de "
                          "Defensores del Patrimonio.", c3="C3-019; C3-076; C3-119; C3-078"),
        convocatoria=[conv("C3-119", "sí", "parcial", "parcial", "sí", "{C3-119} participantes de Lima y Callao en el "
                                                                     "encuentro anual."),
                      conv("C3-019", "parcial", "sí", "sí", "sí", "{C3-019} participantes escolares."),
                      conv("C3-078", "no", "sí", "parcial", "sí", "Taller para niños con más inscritos que cupos.")],
        barreras=[dict(pertinencia="sin datos", evidencias="", texto="La encuesta no pregunta por barreras para "
                                                                    "visitar patrimonio.")],
        vacios=["Si las visitas fueron con el colegio, la familia o por cuenta propia.", "Interés en rutas guiadas.",
                "Convocatoria juvenil."],
        afirmaciones=[dict(texto="Uno de cada cuatro jóvenes visitó un monumento histórico en el año ({E-150}).",
                           evidencias="E-150")],
        hipotesis=["Que rutas de patrimonio organizadas convoquen a jóvenes de 18–29."],
        componentes=[("Rutas o visitas guiadas", "práctica de la misma actividad", "Convocatoria juvenil sin cifras "
                                                                                  "comparables.")],
        validacion="Inscritos y su edad; asistencia; repetición.",
        donde="Criterio operativo: distritos con sitios arqueológicos (Lurigancho-Chosica, Ate, SJL).",
        cambio="Alternativa nueva que emerge del cruce.",
    ),
    dict(
        id="F-10", linea="Cultura digital", actividad="Encuentros o torneos presenciales de videojuegos",
        tipo="actividad de convocatoria abierta", origen="P07", resultado="B: reformulada", segmentos="S-14",
        necesidad=[dict(tipo="sin evidencia", evidencias="", texto="Es una práctica de ocio, no una respuesta a una "
                                                                  "necesidad medida.")],
        poblacion="Hombres de 15–29; más frecuente a los 15–19 ({E-164}) que a los 25–29 ({E-165}).",
        interes=[dict(codigo="P1", evidencias="E-160; E-162; E-161; E-163",
                      texto="{E-160} de los hombres jugó en línea y {E-162} en el celular; entre las mujeres, {E-161} y "
                            "{E-163}.")],
        salto="De jugar en casa o en línea a asistir a un encuentro presencial.",
        alcance=dict(tipo="segmento identificable", evidencias="E-160"),
        oferta=dict(texto="No se encontró ninguna actividad publicada de videojuegos (la ausencia de oferta no es "
                          "demanda).", c3=""),
        convocatoria=[],
        barreras=[dict(pertinencia="indirecta", evidencias="E-100", texto="Sin datos específicos; si es de noche, la "
                                                                         "inseguridad ({E-100}).")],
        vacios=["Interés en un formato presencial.", "Juegos y equipamiento.", "Participación de mujeres."],
        afirmaciones=[dict(texto="La mitad de los hombres jóvenes de Lima Este juega videojuegos en línea ({E-160}).",
                           evidencias="E-160")],
        hipotesis=["Que jugadores habituales acudan a un evento presencial.",
                   "Que un formato diseñado para mujeres aumente su participación.",
                   "Que haya interés en componentes formativos (streaming, diseño)."],
        componentes=[("Encuentro o torneo presencial", "práctica relacionada", "Segmento identificable; convocatoria "
                                                                               "sin evidencia."),
                     ("Inclusión de mujeres", "hipótesis", ""),
                     ("Habilidades digitales asociadas", "sin evidencia", "")],
        validacion="Inscritos frente a cupos; asistencia; proporción de mujeres.",
        donde="Criterio operativo: un solo piloto pequeño en un espacio con conectividad.",
        cambio="Segmento con dato de Lima Este por sexo (antes, brecha de aficiones de Lima Metropolitana).",
    ),
    dict(
        id="F-11", linea="Cultura digital", actividad="Retos colaborativos de tecnología (hackathon)",
        tipo="actividad de convocatoria abierta", origen="P03", resultado="B: reformulada (parcial)", segmentos="",
        necesidad=[dict(tipo="sin evidencia", evidencias="E-230",
                        texto="Que pocos jóvenes programen ({E-230}, Lima Metropolitana) no demuestra una necesidad.")],
        poblacion="Mayores de 18 (formato probado en SJL con jóvenes y adultos).",
        interes=[dict(codigo="P0", evidencias="E-032; E-224",
                      texto="Ninguna fuente mide interés en tecnología. {E-032} de los usuarios usa internet para "
                            "aprender (práctica muy indirecta) y hay {E-224} organizaciones juveniles acreditadas de "
                            "ciencia y tecnología (autoselección).")],
        salto="De usar internet para aprender a participar en un reto tecnológico.",
        alcance=dict(tipo="desconocido", evidencias=""),
        oferta=dict(texto="Hackathon municipal y coworking en SJL.", c3="C3-100; C3-111"),
        convocatoria=[conv("C3-100", "parcial", "sí", "sí", "sí", "{C3-100} inscripciones de mayores de 18 (jóvenes y "
                                                                "adultos de varios distritos).")],
        barreras=[dict(pertinencia="sin datos", evidencias="", texto="No hay datos de acceso a computadora en Lima "
                                                                    "Este.")],
        vacios=["Interés en tecnología.", "Acceso a computadora.", "Perfil de edad de los inscritos en la hackathon."],
        afirmaciones=[dict(texto="Una hackathon municipal en SJL reunió {C3-100} inscripciones de mayores de 18.",
                           evidencias="", c3="C3-100")],
        hipotesis=["Que un reto colaborativo convoque a jóvenes de Lima Este (el único dato mezcla edades)."],
        componentes=[("Reto colaborativo o hackathon", "respaldado parcialmente",
                      "Una señal de convocatoria con segmento parcialmente compatible."),
                     ("Talleres generales de habilidades digitales", "descartado",
                      "Sin necesidad, interés ni convocatoria documentados.")],
        validacion="Inscritos por edad; equipos formados; proyectos terminados.",
        donde="Criterio operativo: SJL (experiencia previa y coworking).",
        cambio="Se descarta el componente de talleres generales; queda solo el formato con una señal de convocatoria.",
    ),
    dict(
        id="F-12", linea="Bienestar y protección",
        actividad="Bienestar y salud mental de mujeres jóvenes (espacio propio o componente con derivación)",
        tipo="intervención segmentada", origen="P08", resultado="B: reformulada", segmentos="",
        necesidad=[dict(tipo="prevalencia", evidencias="E-200; E-201; E-202",
                        texto="En Lima Metropolitana, {E-200} de las mujeres de 15–29 tuvo un episodio depresivo (2024), "
                              "frente a {E-201} de los hombres; {E-202} de las mujeres con pareja sufrió violencia de su "
                              "pareja (2025; serie variable)."),
                   dict(tipo="registro de atención", evidencias="E-203; E-204",
                        texto="En Lima Este, los CEM atendieron {E-203} casos de jóvenes en 2025; {E-204} de las "
                              "víctimas son mujeres.")],
        poblacion="Mujeres de 15–29.",
        interes=[dict(codigo="P0", evidencias="", texto="Ninguna fuente mide interés en espacios de bienestar.")],
        salto="De la prevalencia de un problema a la asistencia voluntaria a un espacio sobre ese problema.",
        alcance=dict(tipo="desconocido", evidencias=""),
        oferta=dict(texto="Charlas en colegios, campaña de salud en SJL, taller de autoestima en El Agustino, programa "
                          "para niñas y adolescentes en SJL.", c3="C3-017; C3-027; C3-087; C3-037; C3-113"),
        convocatoria=[conv("C3-017", "no", "sí", "parcial", "sí", "Charlas escolares (público cautivo)."),
                      conv("C3-087", "parcial", "sí", "parcial", "sí", "Campaña de salud con 'decenas' de "
                                                                      "beneficiarios.")],
        barreras=[dict(pertinencia="indirecta", evidencias="E-101; E-089",
                       texto="Seguridad ({E-101} se siente insegura de noche) y cuidado ({E-089} de las mujeres jóvenes "
                             "de Lima Metropolitana cuidó a alguien del hogar). El estigma no se midió.")],
        vacios=["Prevalencia en Lima Este.", "Disposición a participar.", "Estigma.",
                "Servicios de salud mental comunitaria disponibles."],
        afirmaciones=[dict(texto="La necesidad está documentada en Lima Metropolitana y en registros de atención de "
                                 "Lima Este; su magnitud en Lima Este no se conoce.", evidencias="E-200; E-203")],
        hipotesis=["Que mujeres jóvenes asistan voluntariamente a un espacio de bienestar.",
                   "Que funcione mejor como componente de otra actividad y como ruta de derivación."],
        componentes=[("Espacio de bienestar propio", "necesidad documentada (Lima Metropolitana)",
                      "Interés y convocatoria sin evidencia."),
                     ("Ruta de derivación a servicios", "condición de diseño", "Para cualquier actividad.")],
        validacion="Inscritas y asistencia; comparación entre formato propio y componente; derivaciones realizadas.",
        donde="Criterio operativo: donde haya servicios a los cuales derivar.",
        cambio="El interés pasa de 'bajo' a P0 (lo citado no era interés); el alcance en Lima Este es desconocido.",
    ),
    dict(
        id="F-13", linea="Bienestar y protección",
        actividad="Protocolo de protección y derivación en actividades con adolescentes",
        tipo="protocolo transversal", origen="P11", resultado="C como actividad; reclasificada como protocolo",
        segmentos="",
        necesidad=[dict(tipo="registro de atención", evidencias="E-207; E-208; E-209; E-210; E-205; E-206; E-211",
                        texto="En 2025 hubo {E-207} nacimientos de madres de 15–19 (en 2019, {E-208}); la tasa de El "
                              "Agustino ({E-209} por cada 1 000) supera la mediana metropolitana ({E-210}). {E-205} de "
                              "las víctimas atendidas por los CEM tiene 15–19 años y {E-206} de los casos es de violencia "
                              "sexual. En Lima Metropolitana, {E-211} de las mujeres de 15–19 estuvo alguna vez "
                              "embarazada.")],
        poblacion="Adolescentes de 15–19 que participen en cualquier actividad.",
        interes=[dict(codigo="P0", evidencias="", texto="No aplica: no es una actividad de convocatoria.")],
        salto="",
        alcance=dict(tipo="segmento identificable", evidencias="E-207"),
        oferta=dict(texto="Charlas en colegios (DEMUNA, DEVIDA).", c3="C3-027; C3-017"),
        convocatoria=[],
        barreras=[dict(pertinencia="directa", evidencias="", texto="Requiere consentimiento de madres y padres para "
                                                                  "menores de 18.")],
        vacios=["Servicios de derivación disponibles por distrito."],
        afirmaciones=[dict(texto="Las necesidades registradas se concentran en adolescentes; la maternidad adolescente "
                                 "registrada bajó a menos de la mitad desde 2019.", evidencias="E-207; E-208; E-205")],
        hipotesis=[],
        componentes=[("Educación sexual integral como actividad de convocatoria", "retirado",
                      "Sin evidencia de interés ni de convocatoria voluntaria; corresponde a colegios y salud."),
                     ("Protocolo de protección, consentimiento y derivación", "condición transversal",
                      "Para toda actividad con menores de 18.")],
        validacion="Protocolo aprobado antes de cualquier actividad con menores; derivaciones registradas.",
        donde="Todas las actividades con adolescentes.",
        cambio="Una necesidad intensa en un grupo reducido y en descenso se trata como protocolo transversal, no como "
               "actividad de convocatoria.",
    ),
    dict(
        id="F-14", linea="Participación", actividad="Voluntariado de corta duración con resultados visibles",
        tipo="actividad de convocatoria abierta", origen="P10", resultado="B: reformulada", segmentos="",
        necesidad=[dict(tipo="objetivo institucional", evidencias="E-220; E-222; E-223",
                        texto="La participación en asociaciones es muy baja en Lima Metropolitana ({E-220}) y SJL tiene "
                              "{E-222} organizaciones acreditadas por 10 000 jóvenes (mediana metropolitana: {E-223}). "
                              "Es un objetivo de la organización, no una necesidad declarada por los jóvenes.")],
        poblacion="15–29; hoy llegan sobre todo estudiantes y mujeres.",
        interes=[dict(codigo="P1", evidencias="E-175; E-226; E-227; E-228",
                      texto="{E-175} hizo voluntariado o ayudó a otros hogares en la semana (incluye ayuda a familiares). "
                            "{E-226} personas de Lima Este se inscribieron en el Programa de Voluntariado ({E-227} "
                            "mujeres; {E-228} solo estudia): es autoselección.")],
        salto="De ayudar a otros hogares o inscribirse en un programa a participar en jornadas de voluntariado.",
        alcance=dict(tipo="desconocido", evidencias=""),
        oferta=dict(texto="Minka Joven (Ate), Gran Cruzada Verde (Chosica), réplica de CADE Universitario (SJL), "
                          "Defensores del Patrimonio, pasantías del IMP.", c3="C3-011; C3-072; C3-108; C3-119; C3-020"),
        convocatoria=[conv("C3-011", "sí", "sí", "sí", "sí", "{C3-011} voluntarios jóvenes."),
                      conv("C3-072", "parcial", "sí", "sí", "sí", "{C3-072} voluntarios de edad no indicada."),
                      conv("C3-020", "sí", "sí", "parcial", "sí", "{C3-020} pasantes jóvenes.")],
        barreras=[dict(pertinencia="indirecta", evidencias="E-060; E-040",
                       texto="Tiempo: {E-060} trabajó o buscó trabajo en la semana y {E-040} estudia y trabaja.")],
        vacios=["Disposición a participar de quienes trabajan.", "Formatos preferidos."],
        afirmaciones=[dict(texto="Hay participación declarada con cifras pequeñas en voluntariado juvenil en Lima "
                                 "Este.", evidencias="", c3="C3-011; C3-020")],
        hipotesis=["Que un formato corto con resultado visible atraiga a jóvenes que trabajan y a hombres (no hay "
                   "datos)."],
        componentes=[("Jornadas cortas de voluntariado", "práctica relacionada", "Convocatoria con cifras pequeñas.")],
        validacion="Inscritos y perfil (estudia o trabaja, sexo); asistencia; repetición.",
        donde="Criterio operativo: distritos con baja densidad de organizaciones acreditadas.",
        cambio="La 'necesidad' se reclasifica como objetivo institucional; la práctica de la ENUT se lee como proxy "
               "amplio (incluye ayuda a otros hogares).",
    ),
    dict(
        id="F-15", linea="Hogar y cuidado",
        actividad="Mujeres jóvenes dedicadas al hogar: población que requiere consulta directa",
        tipo="población que requiere consulta directa", origen="Nueva", resultado="Nueva (sin actividad propuesta)",
        segmentos="S-15",
        necesidad=[dict(tipo="situación documentada", evidencias="E-070; E-071; E-054",
                        texto="{E-070} de las mujeres de 15–29 no estudia ni trabaja y se dedica al hogar; entre los "
                              "hombres, {E-071}. Es la situación principal de las mujeres que no estudian ni trabajan "
                              "({E-054}).")],
        poblacion="{E-070:personas}. {E-078} tiene 25–29 años; {E-074} está en unión (frente a {E-075} de las demás "
                  "mujeres); {E-076} vive con niños de 0 a 5 años (frente a {E-077}); {E-085} es jefa de hogar o "
                  "pareja del jefe y {E-084} es hija; {E-079} tiene secundaria completa.",
        interes=[dict(codigo="P0", evidencias="E-081; E-082; E-083; E-080",
                      texto="No sabemos qué actividades les interesan. {E-081} usó internet el mes anterior, pero solo "
                            "{E-082} lo usa para aprender (frente a {E-083} de las demás mujeres); {E-080} quería "
                            "trabajar.")],
        salto="",
        alcance=dict(tipo="segmento identificable", evidencias="E-070"),
        oferta=dict(texto="No se encontró ninguna actividad publicada dirigida a este grupo.", c3=""),
        convocatoria=[],
        barreras=[
            dict(pertinencia="directa", evidencias="E-086; E-087",
                 texto="Cuidado: en Lima Metropolitana, las mujeres jóvenes que no trabajaron ni estudiaron en la "
                       "semana dedicaron {E-086} al trabajo doméstico y de cuidado (muestra pequeña), frente a {E-087} "
                       "de las que trabajaron o estudiaron."),
            dict(pertinencia="directa", evidencias="E-101; E-104",
                 texto="Seguridad: {E-101} de las mujeres jóvenes se siente insegura de noche y {E-104} evitó salir de "
                       "noche."),
        ],
        vacios=["Qué actividades les interesan.", "En qué horarios podrían participar.",
                "Si necesitan cuidado infantil durante una actividad.", "Qué distancia pueden recorrer.",
                "Si quieren estudiar o trabajar y qué se los impide.", "Por qué canales se informan."],
        afirmaciones=[dict(texto="Es un segmento identificable ({E-070:personas}) que ni la oferta publicada ni la "
                                 "primera integración cubrían.", evidencias="E-070")],
        hipotesis=[],
        componentes=[("Actividad para este grupo", "no se propone",
                      "No hay evidencia sobre sus intereses ni disponibilidad: requiere consulta directa.")],
        validacion="Consulta directa (entrevistas o grupos focales en hogares o espacios comunitarios) antes de diseñar "
                   "cualquier actividad.",
        donde="No aplica hasta la consulta.",
        cambio="Segmento nuevo; se caracteriza y se deja explícitamente sin actividad propuesta.",
    ),
]

# ---------------------------------------------------------------------------------------------------------------
# CAMBIOS respecto de las 11 propuestas de la primera versión
CAMBIOS = [
    dict(v1="P01", v1_nombre="Preparación preuniversitaria con orientación vocacional y becas",
         resultado="B: reformulada", fichas_v2="F-01",
         cambio="Segmento con denominador de Lima Este (15–24 sin estudios con secundaria completa); componentes "
                "separados; el interés se reclasifica como no medido; se corrige la población de los motivos (15–24)."),
    dict(v1="P02", v1_nombre="Empleabilidad y primer empleo", resultado="B: reformulada", fichas_v2="F-02; F-03",
         cambio="Necesidad medida en Lima Este; segmento = sin trabajo y busca o quiere trabajar; se retira la "
                "prioridad a mujeres que no estudian ni trabajan (la mayoría se dedica al hogar); los derechos "
                "laborales pasan a una ficha propia."),
    dict(v1="P03", v1_nombre="Habilidades digitales aplicadas y retos colaborativos",
         resultado="B: reformulada (parcial)", fichas_v2="F-11",
         cambio="Se descartan los talleres generales (sin necesidad ni interés documentados); queda el reto "
                "colaborativo, con una señal de convocatoria."),
    dict(v1="P04", v1_nombre="Deporte organizado para 18–29", resultado="B: reformulada", fichas_v2="F-05",
         cambio="Interés de 'alto' a P1 (práctica relacionada); la convocatoria se describe como un solo dato "
                "comparable; el componente femenino pasa a hipótesis de diseño basada en barreras medidas."),
    dict(v1="P05", v1_nombre="Cultura urbana y música en vivo", resultado="B: reformulada", fichas_v2="F-06",
         cambio="Se reorienta a festival local gratuito (práctica de la misma actividad); se corrige la edad (la "
                "música en vivo es de 20–29); cultura urbana y jóvenes organizadores pasan a hipótesis."),
    dict(v1="P06", v1_nombre="Cine y creación audiovisual",
         resultado="B: reformulada; cineforo y taller de video sin evidencia", fichas_v2="F-07",
         cambio="Se conserva la proyección gratuita; conversación y producción de video quedan como componentes sin "
                "evidencia."),
    dict(v1="P07", v1_nombre="Videojuegos y e-sports presenciales", resultado="B: reformulada", fichas_v2="F-10",
         cambio="Segmento con dato de Lima Este por sexo y edad."),
    dict(v1="P08", v1_nombre="Bienestar para mujeres jóvenes", resultado="B: reformulada", fichas_v2="F-12",
         cambio="Interés de 'bajo' a P0 (lo citado no era interés); alcance en Lima Este desconocido."),
    dict(v1="P09", v1_nombre="Emprendimiento juvenil y ventas por internet",
         resultado="C tal como estaba; reformulada para un segmento", fichas_v2="F-04",
         cambio="Se descarta el salto 'informalidad → emprendimiento'; la ficha se limita a jóvenes que ya trabajan "
                "por cuenta propia."),
    dict(v1="P10", v1_nombre="Voluntariado de corta duración", resultado="B: reformulada", fichas_v2="F-14",
         cambio="La 'necesidad' se reclasifica como objetivo institucional; la práctica se lee como proxy amplio."),
    dict(v1="P11", v1_nombre="Educación sexual integral y prevención para adolescentes",
         resultado="C como actividad; reclasificada como protocolo", fichas_v2="F-13",
         cambio="Necesidad intensa en un grupo reducido y en descenso: protocolo transversal de protección y "
                "derivación, no actividad de convocatoria."),
    dict(v1="—", v1_nombre="(no existía)", resultado="Nuevas", fichas_v2="F-03; F-08; F-09; F-15",
         cambio="Derechos laborales, lectura y ferias del libro, rutas de patrimonio y un segmento que requiere "
                "consulta directa (mujeres dedicadas al hogar)."),
]
