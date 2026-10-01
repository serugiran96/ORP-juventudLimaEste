# Modelo de convocatoria por público

Versión 3 · 01/10/2026.

- Script: `scripts/modelo_actividades.py`.
- Resultados:
  - `resultados/modelo_actividades.csv`: un resultado por tipo;
  - `resultados/modelo_publicos.csv`: el embudo de cada tipo en cada público;
  - `resultados/modelo_perfil_publicos.csv`: población, tiempo libre, seguridad, situación y distritos de cada público;
  - `resultados/modelo_criterios.csv`: los pasos del embudo, para la página.
- Tipos y fuentes: `fuentes/modelo_tipos_actividad.csv`.

## 1. Qué responde

A cuántos jóvenes de Lima Este podría convocar cada actividad y cada servicio, a quiénes, cuándo y dónde. Cruza las
tres capas:

- población (Dato Joven);
- quién hace cada actividad y quién no puede hacerla por barreras que la organización puede quitar (ENAPRES, ENUT,
  ENAHO);
- tiempo libre por horario (ENUT);
- inseguridad de noche (ENAPRES);
- a qué se dedica cada público (ENAHO);
- dónde vive (Dato Joven).

**Cambios frente a la versión 2 (30/09/2026).** El equipo pidió un modelo que use toda la información disponible y
no solo las preguntas de cultura. Hay cuatro cambios:

- **Se pasa de un puntaje con pesos a un embudo en personas.** En lugar de decidir cuánto pesa cada criterio, se
  multiplican datos medidos.
- **El cálculo se hace para seis públicos**: mujeres y hombres de 15-19, 20-24 y 25-29 años.
- **Actividades y servicios se ordenan por separado.**
- **El registro de oferta y la necesidad salen del número.** La mayoría de las actividades que convocan no está
  registrada; ambos quedan como señales en la ficha.

## 2. El embudo

Para cada tipo de actividad o servicio y cada público:

> **Jóvenes convocables = población × % que la hace o la haría × % con tiempo libre en su mejor horario**

| Paso | Pregunta | Dato | Fuente |
|---|---|---|---|
| 1. Población | ¿Cuántos jóvenes hay en cada público? | Jóvenes de los siete distritos en 2026, por sexo y edad | Dato Joven 2026 |
| 2. La hace o la haría | ¿Qué parte ya la hace o la haría si se quitan las barreras que la organización puede quitar? | Ya la hacen + frenados (ver abajo) | ENAPRES 2022-2025, ENUT 2024, ENAHO 2022-2025 |
| 3. Tiempo libre | ¿Qué parte tiene tiempo libre en el mejor horario? | % con dos horas libres seguidas en el bloque. En bloques de noche se descuenta a quienes evitan salir por inseguridad | ENUT 2024, ENAPRES 2022-2025 |

**Ejemplo.** Música en vivo, mujeres de 25 a 29 años:
- 147 841 mujeres;
- 51,6 % va a conciertos o no va solo por dinero, información o falta de oferta;
- 37,1 % tiene libre el domingo de 14:00 a 18:00;
- resultado: 147 841 × 51,6 % × 37,1 % ≈ 28 300.

El resultado **no es la asistencia esperada**. Es el público con interés y tiempo, y sirve para comparar.

### Paso 2 en detalle

| Tipo | Ya la hacen | Frenados |
|---|---|---|
| Música, cine, festivales, danza, teatro, circo, artes visuales, artesanía, ferias del libro, biblioteca | ENAPRES: asistió en los últimos 12 meses | ENAPRES: no asistió y su motivo principal fue falta de dinero, de información o de oferta |
| Patrimonio, videojuegos | ENAPRES: visitó o jugó en los últimos 12 meses | No medido |
| Deporte, voluntariado | ENUT: lo hizo en la última semana | No medido |
| Preparación para la educación superior | No medido | ENAHO: 16-24 años, terminó la secundaria, no estudia y su motivo es económico |
| Acompañamiento para el empleo | ENAHO: busca trabajo | ENAHO: no tiene trabajo, quiere trabajar, pero no busca |
| Emprendimiento | ENAHO: trabaja por su cuenta o es empleador | No medido |

**Reglas.**

1. **Solo cuentan las barreras que la organización puede quitar:** dinero, información y falta de oferta. No cuentan
   la falta de interés ni la falta de tiempo; el tiempo se mide en el paso 3.
2. **Si la pregunta mide algo parecido y no la misma actividad, cuenta la mitad,** tanto para quienes ya la hacen como
   para los frenados. Por ejemplo, ver danza frente a practicarla en un taller, el cine comercial frente a un
   cineclub, o buscar trabajo frente a un programa de empleo.
3. **Las medidas semanales (ENUT) no se reducen:** una semana es una ventana más corta que un año, así que ya es
   conservadora.
4. **Si nadie midió los frenados, el número es un piso:** solo cuenta a quienes ya la hacen. Pasa con deporte,
   patrimonio, videojuegos, voluntariado y emprendimiento.
5. **Lo que ninguna encuesta mide no se ordena:** tecnología, derechos laborales y bienestar. Se decide con la
   consulta a jóvenes.

### Paso 3 en detalle

- La ENUT 2024 registra en un diario qué hace cada persona cada 10 minutos, en un día de semana, un sábado y un
  domingo.
- Se calcula el % de cada público con dos horas libres seguidas en siete bloques: tardes y noches de semana, y
  mañana, tarde y noche del sábado y del domingo.
- En los bloques de noche se descuenta el % que evita salir de noche por inseguridad (ENAPRES).
- Para los seis públicos el mejor bloque es el **domingo de 14:00 a 18:00**.

| Público | Tiempo libre el domingo por la tarde |
|---|---|
| Hombres 15-19 | 61 % |
| Mujeres 15-19 | 51 % |
| Hombres 20-24 | 50 % |
| Hombres 25-29 | 44 % |
| Mujeres 20-24 | 43 % |
| Mujeres 25-29 | 37 % |

### Cómo se estima cada público

- **ENAPRES:** la muestra de Lima Este no alcanza para cada combinación de sexo y edad. Se combina la cifra por edad
  (Lima Este) con la diferencia entre mujeres y hombres (Lima Este, 15-29). Esto supone que esa diferencia es
  parecida en cada edad.
- **ENUT:** la cifra de Lima Este se combina con el patrón por sexo y edad de Lima Metropolitana, porque la muestra de
  Lima Este es de 234 jóvenes.
- **ENAHO:** cifras de Lima Este por sexo y edad, con dos excepciones:
  - trabajo independiente: ocupados del público × % de independientes entre los ocupados, que solo existe para 15-29;
  - motivo para no estudiar: se pregunta hasta los 24 años, así que la preparación para la educación superior no
    tiene dato para 25-29.
- **Distritos:** el reparto sigue la población de cada público (Dato Joven). Las encuestas no permiten saber si en
  un distrito se practica más que en otro.

### Margen de error

Se simula 4 000 veces cada estimación de encuesta con su error estándar. De ahí salen:

- el rango de jóvenes convocables (percentiles 5 y 95);
- los puestos posibles de cada tipo dentro de su grupo.

## 3. Por qué actividades y servicios van aparte

Los servicios se dirigen a jóvenes con una necesidad específica, no a todos:

- preparación para la educación superior: quienes terminaron la secundaria y no estudian por dinero;
- acompañamiento para el empleo: quienes buscan o quieren trabajar;
- emprendimiento: quienes trabajan por su cuenta.

Medidos en número total de jóvenes, siempre quedarían debajo de un concierto, abierto a los 712 mil jóvenes, aunque
llenen sus cupos sin problema. Por eso se comparan solo entre sí.

El costo no los penaliza. El modelo supone que todo es gratis: en preparación para la educación superior, los
frenados son justamente quienes no estudian por dinero.

## 4. Qué no cambia el número

| Elemento | Dónde aparece | Por qué no cambia el número |
|---|---|---|
| Registro de oferta (C0 a C4) | Señal en la ficha | La mayoría de las actividades que convocan no está registrada: la ausencia de registro no resta |
| Necesidad | Etiqueta en la ficha | No indica si vendrán. En los servicios ya está dentro del número |
| Aliados | No se usa | La organización no los necesita para empezar |
| Permanencia | Validación en el piloto | Se mide con asistencia a 3 o más sesiones y permanencia a los 3 meses |
| Interés declarado (Ipsos) | Contexto | Es del Perú urbano, no de Lima Este |
| Barreras de horario, seguridad, costo, información y cuidado | Condiciones de diseño | Valen para todas. El horario y la seguridad nocturna sí entran en el paso 3 |

## 5. Resultado (15 a 29 años)

**Actividades**

| Puesto | Actividad | Convocables | Rango con margen de error | Puestos posibles | Frenados | Mujeres | Público que más convoca |
|---|---|---|---|---|---|---|---|
| 1 | Música en vivo | 136 mil | 126–145 mil | 1 | 48 % | 58 % | Mujeres 25-29 |
| 2 | Cine (cineclub) | 118 mil | 114–122 mil | 2 | 11 % | 54 % | Mujeres 15-19 |
| 3 | Ferias del libro y lectura | 107 mil | 98–115 mil | 3–4 | 39 % | 51 % | Hombres 15-19 |
| 4 | Festivales y fiestas locales | 100 mil | 92–109 mil | 3–5 | 35 % | 54 % | Mujeres 25-29 |
| 5 | Deporte organizado | 93 mil | 84–102 mil | 4–6 | no medido | 28 % | Hombres 15-19 |
| 6 | Patrimonio | 83 mil | 76–90 mil | 5–7 | no medido | 54 % | Mujeres 25-29 |
| 7 | Biblioteca como espacio juvenil | 81 mil | 73–89 mil | 6–7 | 41 % | 48 % | Hombres 15-19 |
| 8 | Videojuegos presenciales | 61 mil | 57–66 mil | 8–9 | no medido | 25 % | Hombres 15-19 |
| 9 | Artesanía | 59 mil | 54–63 mil | 8–9 | 42 % | 58 % | Mujeres 25-29 |
| 10 | Danza | 51 mil | 47–55 mil | 10 | 41 % | 55 % | Mujeres 15-19 |
| 11 | Circo y artes urbanas | 42 mil | 38–46 mil | 11–12 | 58 % | 55 % | Mujeres 15-19 |
| 12 | Teatro | 41 mil | 37–45 mil | 11–13 | 56 % | 54 % | Mujeres 15-19 |
| 13 | Artes visuales | 36 mil | 32–39 mil | 12–13 | 60 % | 60 % | Mujeres 15-19 |
| 14 | Voluntariado | 30 mil | 26–34 mil | 14 | no medido | 51 % | Hombres 15-19 |

**Servicios**

| Puesto | Servicio | Convocables | Rango con margen de error | Frenados | Mujeres | Público que más convoca | Registro |
|---|---|---|---|---|---|---|---|
| 1 | Preparación para la educación superior | 24 mil | 21–28 mil | 100 % | 51 % | Mujeres 20-24 | Más interesados que cupos (C4) |
| 2 | Acompañamiento para el empleo | 19 mil | 17–22 mil | 50 % | 57 % | Hombres 15-19 | Más interesados que cupos (C4) |
| 3 | Emprendimiento | 16 mil | 15–17 mil | no medido | 41 % | Hombres 25-29 | Señales débiles (C2) |

**Sin datos para ordenar:** tecnología, derechos laborales y bienestar.

**Lectura.**

- **Por público:**
  - **mujeres de los tres grupos de edad y hombres de 25-29:** lo que más convoca es música en vivo;
  - **hombres de 15-19 y de 20-24:** deporte organizado.
- **Por sexo:** deporte y videojuegos convocan sobre todo a hombres; música, artesanía y artes visuales, a más
  mujeres.
- **Barreras:**
  - en música en vivo, casi la mitad del público son frenados, sobre todo por dinero, y más en mujeres: 28,8 % de las
    que no van a conciertos no va por dinero, frente a 12,7 % de los hombres;
  - en ferias del libro pesa más la falta de información.
- **Dónde:** San Juan de Lurigancho (44 %) y Ate (25 %) concentran el 68 % de los jóvenes de Lima Este.
- **Seguridad:** el 72 % de las mujeres jóvenes se siente insegura de noche en su barrio.

## 6. Límites

- **No predice asistencia ni permanencia.** Ninguna encuesta preguntó si participarían en la actividad propuesta.
  Se valida en pilotos:
  - inscritos frente a cupos;
  - asistencia a 3 o más sesiones;
  - permanencia a los 3 meses.
- **El cruce por sexo y edad es aproximado** (ver "Cómo se estima cada público").
- **Los tipos sin frenados medidos están subestimados:** su número es un piso.
- **La regla de la mitad para prácticas parecidas es una decisión del equipo:** explícita y aplicada igual a todos.
- **No se ven diferencias entre distritos:** el reparto sigue la población.
