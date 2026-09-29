# Modelo multicriterio de potencial de convocatoria

Versión 1 · 29/09/2026 · `scripts/modelo_actividades.py` → `resultados/modelo_criterios.csv` y
`resultados/modelo_actividades.csv`.

## 1. Por qué un modelo

La segunda integración (`metodologia_integracion.md`) describe cada alternativa con categorías descriptivas y sin
ranking. El equipo pidió (29/09/2026) un cruce que permita **determinar qué tipo de actividades tienen más
posibilidades de convocar a los jóvenes de Lima Este** con dos condiciones:

- no puede basarse solo en dónde hay más oferta;
- tampoco solo en cuánta gente podría asistir.

El modelo cruza seis criterios con reglas fijas y pesos explícitos. Usa los mismos códigos de las fichas (necesidad,
P0–P2, C0–C4), el tamaño de los segmentos, el registro de oferta y el RENOJ. No cambia ninguna cifra ni ninguna
ficha: solo las ordena.

## 2. Los seis criterios

Cada criterio vale de 0 a 3 (`modelo_criterios.csv`).

| Criterio | Pregunta | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|
| Necesidad | ¿Responde a una necesidad documentada de los jóvenes de Lima Este? | prevalencia o brecha de acceso medida en Lima Este | registro de atención o situación documentada; prevalencia medida solo en Lima Metropolitana | objetivo institucional | sin evidencia |
| Público potencial | ¿A cuántos jóvenes de Lima Este podría llegar? | 250 mil o más | 100 a 250 mil | 30 a 100 mil | menos de 30 mil o no estimable |
| Práctica o interés | ¿Los jóvenes ya hacen algo parecido? | P2 (misma actividad) | P1 (práctica relacionada) | I1 (interés declarado fuera de Lima Este) | P0 |
| Convocatoria observada | ¿Actividades parecidas ya convocaron jóvenes? | C4 (más interesados que cupos) | C3 (participación declarada comparable) | C2 (señales débiles) | C0 o C1 |
| Espacio en la oferta | ¿La oferta actual deja espacio para una actividad nueva? | 0 o 1 actividad para jóvenes relacionada | 2 o 3, o la oferta existente se llenó (C4) | 4 a 6 | 7 o más |
| Aliados para convocar | ¿Hay organizaciones juveniles del tema que puedan ayudar a convocar? | 30 o más | 10 a 29 | 1 a 9 | ninguna |

Detalles de las reglas:

- **Público potencial:** usa el límite inferior del segmento con la población 2026 de Dato Joven (`segmentos.csv`).
  Si la ficha tiene varios segmentos, se toma el mayor.
- **Espacio en la oferta:** cuenta, entre las actividades del registro citadas por la ficha (`actividades_c3`), las
  dirigidas a jóvenes. Con C4, la oferta existente no alcanza, así que vale al menos 2.
- **Aliados:** cuenta las organizaciones acreditadas en el RENOJ en Lima Este cuya temática principal corresponde a la
  alternativa. La correspondencia está en `fuentes/modelo_aliados.csv`, que es editable y documenta cada decisión.
- **Necesidad:** una prevalencia cuenta como medida fuera de Lima Este si el texto de la ficha la sitúa primero en
  Lima Metropolitana (es el caso de F-12).

## 3. Puntaje, pesos y robustez

**Puntaje.** Es el promedio ponderado de los seis criterios, llevado a 0–100:
`100 × Σ(peso × puntaje) / (3 × Σ pesos)`.

**Pesos recomendados.**

| Criterio | Peso |
|---|---|
| Práctica o interés | 3 |
| Convocatoria observada | 3 |
| Necesidad | 2 |
| Público potencial | 2 |
| Espacio en la oferta | 1 |
| Aliados para convocar | 1 |

La práctica y la convocatoria observada pesan más porque son los indicios más directos de que una actividad puede
convocar. La necesidad y el tamaño expresan la pertinencia para Lima Este. El espacio y los aliados describen el
contexto.

**Niveles.**

| Nivel | Puntaje |
|---|---|
| Mayor potencial | 60 o más |
| Potencial medio | 45 a 60 |
| Menor respaldo hoy | menos de 45 |

**Robustez.** El resultado se recalcula con cuatro combinaciones de pesos:

- recomendado;
- todos pesan igual;
- necesidades primero (necesidad 3, público 2, práctica 2, convocatoria 2, espacio 1, aliados 1);
- alcance primero (público 3, práctica 2, convocatoria 2, necesidad 1, espacio 1, aliados 1).

`puesto_min` y `puesto_max` indican el rango de puestos de cada alternativa, y `nivel_estable` si su nivel cambia
entre combinaciones. En el observatorio los pesos se pueden ajustar; el resultado se actualiza al momento.

**Solidez de la evidencia.** Se informa aparte. Es el porcentaje de las evidencias citadas por la ficha que son de
Lima Este y tienen precisión suficiente:

| Solidez | Porcentaje |
|---|---|
| Alta | 85 % o más |
| Media | 60 % a 85 % |
| Baja | menos de 60 % |

## 4. Resultado (pesos recomendados)

| Puesto | Alternativa | Puntaje | Rango de puestos | Nivel | Solidez |
|---|---|---|---|---|---|
| 1 | F-02 Acompañamiento para la búsqueda de empleo | 72 | 1–2 | Mayor potencial | 100 % |
| 2 | F-01 Preparación gratuita para el ingreso a la educación superior | 67 | 1–2 | Mayor potencial | 100 % |
| 3 | F-08 Actividades juveniles en ferias del libro y bibliotecas | 58 | 2–4 | Potencial medio | 85 % |
| 3 | F-09 Visitas y rutas de patrimonio cultural | 58 | 2–4 | Potencial medio | 100 % |
| 5 | F-05 Deporte organizado para jóvenes de 18–29 | 53 | 5–6 | Potencial medio | 57 % |
| 5 | F-06 Festival o escenario local gratuito | 53 | 5–6 | Potencial medio | 86 % |
| 7 | F-14 Voluntariado de corta duración | 50 | 6–9 | Potencial medio | 67 % |
| 8 | F-07 Proyecciones de cine gratuitas | 47 | 5–8 | Potencial medio | 100 % |
| 9 | F-03 Derechos laborales y formalización | 44 | 3–9 | Menor respaldo hoy | 100 % |
| 10 | F-04 Apoyo a quienes trabajan por cuenta propia | 39 | 10–11 | Menor respaldo hoy | 75 % |
| 11 | F-10 Encuentros de videojuegos | 36 | 9–11 | Menor respaldo hoy | 100 % |
| 12 | F-12 Bienestar y salud mental de mujeres jóvenes | 31 | 10–12 | Menor respaldo hoy | 44 % |
| 13 | F-11 Retos de tecnología (hackathon) | 22 | 13 | Menor respaldo hoy | 67 % |

**Lectura.**

- **Empleo y preparación para la educación superior** encabezan el resultado en las cuatro combinaciones de pesos.
  Combinan una necesidad medida en Lima Este con convocatoria observada: más interesados que cupos.
- **Las alternativas culturales** tienen la práctica más alta, porque los jóvenes ya hacen esa misma actividad. Pero
  hay poca evidencia de que una oferta organizada convoque.
- **Derechos laborales** responde a una necesidad amplia (la informalidad), pero no tiene práctica ni convocatoria
  comparable. Por eso su puesto depende de los pesos (3 a 9).

F-13 (protocolo transversal) y F-15 (población que requiere consulta directa) no se puntúan.

## 5. Lo que el modelo no hace

- **No predice asistencia ni reemplaza la consulta a los jóvenes.** Ninguna fuente llega al código I2 (interés en
  participar en la actividad propuesta).
- **No convierte la falta de evidencia en evidencia negativa.** Un 0 significa que no hay evidencia a favor.
- **No usa las barreras para restar puntos.** El horario, la seguridad, el costo, la información y el cuidado valen
  para todas las alternativas y se tratan como condiciones de diseño. Restarlas penalizaría a las fichas con más
  barreras medidas, no a las más difíciles de convocar.
- **No convierte la ausencia de oferta en demanda.** El espacio en la oferta solo indica que una actividad nueva no
  duplicaría la existente.
- **Los umbrales y los pesos son decisiones del equipo, no resultados de los datos.** Por eso son explícitos,
  ajustables y se prueban con cuatro combinaciones.
