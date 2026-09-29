# Metodología del cruce de las tres capas (segunda versión)

Cómo se integran la Capa 1 (contexto y necesidades), la Capa 2 (intereses, hábitos y barreras) y la Capa 3 (oferta
y convocatoria) para responder, **para cada tipo de actividad**:

- qué evidencia existe;
- a qué jóvenes aplica y qué tamaño tiene ese segmento;
- qué se sabe de sus prácticas o intereses;
- qué evidencia hay de participación en actividades similares;
- qué barreras pueden existir;
- qué falta validar.

**Fecha:** 25/09/2026.

**Reemplaza** la primera versión (niveles alto/medio/bajo y 11 propuestas). Por qué se reemplazó:
`fuentes/auditoria_integracion.md`. Qué cambió en cada propuesta: `resultados/cambios_primera_version.csv`.

**Productos**, en `resultados/`:

| Archivo | Contenido |
|---|---|
| `evidencias.csv` | 217 datos atómicos |
| `hallazgos_integrados.csv` | 62 hallazgos por capa |
| `patrones.csv` | 13 patrones, brechas y condiciones transversales |
| `segmentos.csv` | 18 segmentos con su tamaño |
| `fichas_actividad.csv` | 15 fichas por actividad y segmento |
| `fichas_cadena.csv` | La cadena de 10 pasos de cada ficha |
| `fichas_componentes.csv` | Componentes de cada ficha y su estado |
| `fichas_convocatoria.csv` | Registros de convocatoria con su comparabilidad y su código |
| `validacion_integracion.csv` | Controles de consistencia entre tablas (sección 11) |
| `informe_final.md` / `.html` | Informe de lectura |

La verificación está en `notebooks/04_integracion.ipynb`.

---

## 1. Proceso

```
Microdatos del INEI ya usados en las Capas 1 y 2          + módulos nuevos (ENAHO 02, ENAPRES seguridad)
      │
      ▼
scripts/integracion_enaho_segmentos.py     segmentos de Lima Este (ENAHO 02+03+05)   → data/processed/integracion_enaho_*.csv
scripts/integracion_seguridad_enapres.py   inseguridad y actividades evitadas         → data/processed/integracion_seguridad_*.csv
scripts/integracion_tiempo_enut.py         disponibilidad horaria y cuidado (ENUT)    → data/processed/integracion_tiempo_enut.csv
scripts/integracion_cultura_edad_enapres.py  cultura por edad y totales (ENAPRES)     → data/processed/integracion_cultura_*.csv
      │
      ▼
scripts/integracion_evidencias.py   registro atómico: cada dato se LEE de data/processed/ (nunca se escribe a mano)
scripts/integracion_contenido.py    textos de hallazgos, patrones, segmentos y fichas, con marcadores {E-###} y {C3-###}
scripts/integracion_construir.py    reemplaza los marcadores, calcula códigos, valida reglas y escribe resultados/*.csv
      │
      ▼
scripts/integracion_informe.py (informe_final.md) · scripts/integracion_pagina.py (informe_final.html)
notebooks/04_integracion.ipynb (verificaciones y tablas)
```

**Orden de ejecución**, desde la carpeta del proyecto. Los pasos `descargar` solo se necesitan la primera vez:

```
python scripts/integracion_enaho_segmentos.py descargar      # Módulo 02 de la ENAHO
python scripts/integracion_enaho_segmentos.py calcular
python scripts/integracion_seguridad_enapres.py descargar    # capítulo de seguridad de la ENAPRES
python scripts/integracion_seguridad_enapres.py calcular
python scripts/integracion_tiempo_enut.py
python scripts/integracion_cultura_edad_enapres.py
python scripts/integracion_construir.py
python scripts/integracion_informe.py
python scripts/integracion_pagina.py
```

---

## 2. Reglas del cruce

Las reglas I-R1 a I-R7 de la primera versión se mantienen; I-R8 a I-R14 se agregan.

| ID | Regla |
|---|---|
| I-R1 | La ausencia de oferta no es evidencia de demanda. |
| I-R2 | La frecuencia de oferta no es evidencia de interés. |
| I-R3 | Una señal de demanda vale solo para la oferta concreta en que se observó (C3-D9). |
| I-R4 | Los resultados de actividades para niños y adolescentes no se generalizan a la juventud. |
| I-R5 | Los niveles geográficos no se mezclan: Lima Este, Lima Metropolitana, Perú urbano y nacional se citan como tales. |
| I-R6 | Una brecha entre práctica y oferta no prueba que los jóvenes quieran la actividad que falta. |
| I-R7 | Dónde pilotear es un criterio operativo, no de demanda (no hay datos de interés por distrito). |
| **I-R8** | **Toda cifra viene de una evidencia.** Los textos usan marcadores; el constructor rechaza porcentajes escritos a mano y evidencias inexistentes. |
| **I-R9** | **Ausencia de evidencia ≠ evidencia negativa.** "Sin evidencia" (C0, P0) nunca se presenta como "baja". |
| **I-R10** | **Práctica observada ≠ interés declarado ≠ interés en participar en la actividad propuesta.** El salto que queda abierto se escribe en cada ficha. |
| **I-R11** | **Los componentes se evalúan por separado.** La evidencia de un componente no respalda al resto de la actividad. |
| **I-R12** | **Una necesidad intensa en un segmento reducido es una intervención segmentada o una condición transversal**, no una propuesta de alcance general. |
| **I-R13** | **Sin puntaje, sin orden por evidencia.** Las dimensiones no se suman; las fichas se ordenan por línea temática. |
| **I-R14** | **Una cifra no publicable (CV > 25 %) no se cita.** Las referenciales llevan la marca "(referencial)" en todos los textos. |

---

## 3. Decisiones de la segunda versión

| ID | Decisión | Motivo |
|---|---|---|
| I2-D1 | **Se reemplazan los niveles alto/medio/bajo por categorías descriptivas** para cada dimensión (sección 4). Cada dimensión se lee por separado. | Los niveles mezclaban ámbito, cercanía, precisión y tipo de evidencia, no eran comparables y podían leerse como ranking (auditoría, sección 1.2). |
| I2-D2 | **Registro atómico de evidencias** con tipo de dato (dato observado o cálculo derivado), naturaleza (encuesta representativa, registro administrativo, autoselección, estudio de mercado, oferta publicada), ámbito, periodo, población, n, error, CV, precisión, validación, antigüedad y limitación. | Trazabilidad completa: cada cifra remite a una fila y a un archivo. |
| I2-D3 | **Situación de estudio y trabajo.** Asiste = matriculado y asiste. Estudia = asiste, o está de vacaciones entre ciclos. Trabaja = ocupado. Estudia y trabaja = ocupado que asiste. | Validado contra Dato Joven (Lima Metropolitana, 2022-2025, total y por sexo; 12 comparaciones por categoría). **"Estudia y trabaja" (máx. 0,08 puntos) y "solo estudia" (máx. 0,21) son equivalentes.** **"No estudia ni trabaja" (máx. 1,92) y "solo trabaja" (máx. 2,05) no lo son.** La parte que no se explica (~1 punto) es compatible con un tratamiento distinto de los desocupados ocultos y de los casos sin dato de empleo, que en Dato Joven no se pudo confirmar: sus manuales ahora exigen iniciar sesión (verificado el 25/09/2026; no se intentó eludir). Por eso la categoría se llama **"no estudia ni trabaja (definición del proyecto)"**, nunca "NINI", y **no se compara con la cifra de Dato Joven**. Lima Este y Lima Metropolitana solo se comparan con la misma definición. |
| I2-D4 | **Motivos para no estudiar: universo de 15-24 años.** | La ENAHO no hace la pregunta (p313) a mayores de 24. La primera versión los atribuía a 15-29 (error E1 de la auditoría). |
| I2-D5 | **Población compatible con la preparación preuniversitaria:** 15-24 que no estudian y cuyo nivel máximo aprobado es secundaria completa (p301a = 6). | Es un denominador real. **No mide intención de estudiar** (ninguna fuente la mide), y la categoría del INEI "terminó sus estudios o asiste a academia" no se puede separar. |
| I2-D6 | **Dos bases de población, sin combinarlas.** (a) Porcentaje (con su IC 95 %) × población 2026 de Dato Joven (REUNIS/INEI). (b) Total estimado directamente por la encuesta (± 1,96 errores estándar). | Las bases difieren. Para 15-29 en Lima Este: Dato Joven, 712 mil; expansión de la ENAHO, 848 mil (±81 mil); de la ENAPRES, 677 mil (±77 mil); de la ENUT, 558 mil (±158 mil). Los factores de expansión de las encuestas no se calibran por distrito, y la serie de Dato Joven es una proyección administrativa inestable por edad (D5). Se muestran ambas; ninguna es "la verdadera". El rango con la base de Dato Joven refleja solo el error muestral del porcentaje: la proyección 2026 no publica error y su composición por sexo es poco habitual (D5), así que las cantidades por sexo con esa base son más inciertas. Los porcentajes de 2022–2025 (o de 2024) se aplican a la población de 2026: es un orden de magnitud, no una estimación de 2026. |
| I2-D7 | **Disponibilidad horaria (ENUT 2024):** % con al menos 2 horas seguidas sin obligaciones ni sueño dentro de bloques de 4 horas. Obligaciones = trabajo o búsqueda, traslados, estudio, trabajo doméstico, cuidado y autoconsumo. | Es disponibilidad observada en un día registrado, **no preferencia**. El criterio "todo el bloque libre" se descartó: 10 minutos de una tarea bastaban para anular el bloque. Control interno: las horas de trabajo doméstico coinciden con la Capa 2 (diferencia ≤ 0,01 h). |
| I2-D8 | **Seguridad (ENAPRES, capítulo 600 / 400).** Inseguridad al caminar solo de noche por el barrio (2022-2025: P611B_1, P611B_1, P604, P405). Dejó o evitó actividades en los últimos 12 meses (2022-2024: P621A/C, P646/P648). | Réplica validada con Dato Joven: **15 de 15 comparaciones dentro de ±1 punto** (máx. 0,55). En 2025 la lista de actividades evitadas cambió y el valor salta de ~33 % a ~63 %, así que 2025 se excluye de esas preguntas. **Solo se estiman proporciones:** los factores del capítulo no expanden a totales de población coherentes (en 2024-2025 corresponden a una submuestra). |
| I2-D9 | **Módulo 02 de la ENAHO** (composición del hogar) para caracterizar a las mujeres dedicadas al hogar: unión, parentesco, niños de 0 a 5 años en el hogar. | Es la misma encuesta y el mismo periodo; permite describir el segmento sin suponer. No identifica si los niños son sus hijos. |
| I2-D10 | **Código de convocatoria calculado con una regla fija** (sección 4.3). Se basa en el tipo de evidencia del registro de la Capa 3 y en la comparabilidad declarada en segmento, territorio, formato y costo. | Reproducible: la única decisión manual es la comparabilidad, que queda escrita en `fichas_convocatoria.csv`. |
| I2-D11 | **Cultura por edad dentro de Lima Este** (ENAPRES 2022-2025), con las mismas funciones de la Capa 2. | Los segmentos de edad de la primera versión (15-24) no tenían datos; ahora se comprueban (por ejemplo, los conciertos son de 20-29 y no de 15-19). |
| I2-D12 | **Comparaciones entre Lima Este y Lima Metropolitana:** solo se describe una diferencia como distinguible si \|z\| ≥ 1,96 con la prueba aproximada de D9. | Lima Este forma parte de Lima Metropolitana, así que la prueba es aproximada. Por ejemplo, deporte: 27,6 % frente a 34,8 %, z ≈ −1,7, no distinguible. |

---

## 4. Categorías y reglas de asignación

### 4.1 Necesidad o problemática

| Tipo | Cuándo se usa |
|---|---|
| prevalencia | Encuesta representativa que mide el problema en la población (por ejemplo, desempleo, informalidad, episodio depresivo). |
| brecha de acceso | Una situación medida que limita el acceso a algo (por ejemplo, no estudia y solo tiene secundaria completa). |
| registro de atención | Casos atendidos o registrados (CEM, nacimientos). Depende del acceso a servicios: **no mide prevalencia**. |
| situación documentada | Una situación medida que no es por sí misma una necesidad declarada (por ejemplo, dedicarse al hogar). |
| objetivo institucional | Lo que la organización quiere cambiar (por ejemplo, baja participación organizada); no es una necesidad declarada ni medida en los jóvenes. |
| sin evidencia | Ninguna fuente mide una necesidad relacionada. En actividades culturales o de ocio es lo esperable. |

Cada necesidad indica su **ámbito** y, cuando se puede, **a cuántas personas afecta**.

### 4.2 Interés o práctica: distancia inferencial

| Código | Qué se observó | Regla |
|---|---|---|
| P0 | Sin evidencia | Ninguna fuente mide la práctica ni el interés. |
| P1 | Práctica relacionada | Dominio más amplio u otro formato (por ejemplo, "deporte o ejercicio" para una liga organizada; cine comercial para una proyección gratuita). |
| P2 | Práctica de la misma actividad | El indicador mide la misma actividad en el mismo formato (gratuito o pagado, organizado o no, presencial) y rango de edad (por ejemplo, festival local para un festival local). |
| I1 | Interés declarado en el tema | Solo existe en Ipsos 2019-2022, fuera de Lima Este: se cita como orientativo. |
| I2 | Interés declarado en participar en la actividad propuesta | **No existe en ninguna fuente actual.** Solo una consulta directa puede producirlo. |

El código de la ficha es el más alto entre sus registros. El **salto inferencial** que queda abierto se escribe
siempre. Los protocolos transversales llevan "no aplica".

### 4.3 Convocatoria

Regla, aplicada por `integracion_construir.py` a cada registro de la Capa 3 citado en una ficha:

1. Si la comparabilidad en **segmento o territorio es "no"**, el registro es **no comparable**. Se muestra, pero no
   define el código.
2. **Demanda observada** (más interesados que cupos) → **C4**.
3. **Participación declarada:**
   - **C3** si hay cifra y el segmento y el territorio son comparables ("sí");
   - **C2** si no hay cifra o la comparabilidad es parcial.
4. **Solo oferta** → **C1**.
5. Sin registros comparables → **C0 (sin evidencia; no es evidencia negativa)**.

El código de la ficha es el más alto entre los registros comparables. Se acompaña de un detalle:

- con qué comparabilidad se obtuvo;
- si es demanda por una oferta concreta (C3-D9);
- si la cifra fue declarada por quien organiza y sin cupos publicados.

**CB (evidencia de baja convocatoria):** cupos sin llenar, cancelaciones o asistencia menor que la inscripción.
Existe como categoría, pero **no apareció ningún caso** en los datos.

Las fichas que son protocolo o población a consultar llevan "no aplica".

### 4.4 Alcance potencial

| Tipo | Cuándo se usa |
|---|---|
| amplia | La evidencia se refiere a toda la juventud de 15-29 y la actividad no exige una condición particular. |
| segmento identificable | La actividad solo tiene sentido para una condición medible (por ejemplo, busca trabajo). Se da su tamaño en % y en personas (I2-D6). |
| desconocido | No hay denominador. Se escribe: "alcance potencial no estimable con la evidencia disponible". |
| no aplica | Protocolos transversales: se aplican a toda actividad con cierta población. |

No se fija un umbral numérico entre "amplia" y "segmento". El tamaño **no se convierte en importancia ni en
recomendación**.

### 4.5 Barreras

Cada barrera lleva su **pertinencia**:

- **directa**: medida para esa actividad o situación;
- **indirecta**: medida para otra actividad;
- **sin datos**.

No se incluyen barreras que nuestras fuentes no miden. Tampoco "supuestos de diseño" sin dato.

### 4.6 Componentes

Una dimensión está **respaldada** si:

- la necesidad está documentada (cualquier tipo salvo "sin evidencia" u "objetivo institucional"); o
- el interés es P1 o más; o
- la convocatoria es C3 o C4.

Estados posibles de un componente:

- respaldado en dos o más dimensiones;
- respaldado en una dimensión;
- solo señales débiles (C2 o registros de autoselección);
- hipótesis de diseño;
- sin evidencia;
- descartado;
- condición transversal;
- complementario (ya existe).

### 4.7 Tipos de ficha

| Tipo | Significado |
|---|---|
| actividad de convocatoria abierta | Actividad dirigida a una población amplia. |
| intervención segmentada | Actividad para una condición medible. |
| protocolo transversal | Se aplica a toda actividad con cierta población; no convoca. |
| población que requiere consulta directa | Segmento caracterizado sin evidencia sobre qué actividad le sería útil. **No se inventa una actividad.** |

### 4.8 La ficha: cadena de trazabilidad

Cada ficha tiene diez pasos, en `fichas_cadena.csv`:

1. Contexto o necesidad
2. Población a la que aplica
3. Interés o práctica observada
4. Alcance potencial
5. Oferta territorial existente
6. Evidencia de participación o convocatoria
7. Barreras
8. Vacíos de información
9. Qué podemos afirmar
10. Qué solo podemos plantear como hipótesis

"Qué podemos afirmar" solo admite datos observados o cálculos derivados, con su evidencia. Las interpretaciones y
las hipótesis van en sus propios campos.

---

## 5. Validaciones

| Qué | Resultado |
|---|---|
| Situación de estudio y trabajo frente a Dato Joven (ENAHO, Lima Metropolitana, 2022-2025, total/hombre/mujer) | Estudia y trabaja: máx. 0,08 · solo estudia: 0,21 (equivalentes). No estudia ni trabaja: 1,92 · solo trabaja: 2,05 (no equivalentes; I2-D3). |
| Desempleo e informalidad (misma definición que D15 de la Capa 1) | Ya validados en la Capa 1 (32 de 32 dentro de ±1). |
| Inseguridad nocturna frente a Dato Joven (ENAPRES, 2022-2025, total/hombre/mujer) | 12 de 12 dentro de ±1 (máx. 0,55). |
| Dejó alguna actividad por temor frente a Dato Joven (2022-2024, total) | 3 de 3 dentro de ±1 (máx. 0,46). |
| Horas de trabajo doméstico (ENUT) frente a la Capa 2 | Diferencia ≤ 0,01 h. |
| Participación semanal (ENUT) y cultura (ENAPRES) frente a la Capa 2 | Mismos valores (mismas funciones). |
| Reglas del constructor | Ningún porcentaje a mano; ninguna cifra no publicable citada; todas las evidencias y actividades citadas existen; cada ficha tiene vacíos, e hipótesis si es de convocatoria; estados de componentes del vocabulario controlado. |
| Controles de consistencia (sección 11) | 10 de 10 (`resultados/validacion_integracion.csv`). |

---

## 6. Resultado

**15 fichas, ordenadas por línea temática** (no por evidencia):

| Ficha | Actividad | Tipo | Necesidad | Interés | Alcance | Convocatoria |
|---|---|---|---|---|---|---|
| F-01 | Preparación gratuita para el ingreso a la educación superior | intervención segmentada | brecha de acceso | P0 | segmento identificable | C4 — C3-125 |
| F-02 | Acompañamiento para la búsqueda de empleo (preparación y conexión con vacantes) | intervención segmentada | prevalencia | P1 | segmento identificable | C4 — C3-084 |
| F-03 | Derechos laborales y formalización para jóvenes que ya trabajan | intervención segmentada | prevalencia | P0 | segmento identificable | C2 — C3-061 |
| F-04 | Apoyo a jóvenes que ya trabajan por cuenta propia | intervención segmentada | sin evidencia | P1 | segmento identificable | C2 — C3-132 |
| F-05 | Deporte organizado para jóvenes de 18–29 (ligas, torneos, entrenamiento) | actividad de convocatoria abierta | sin evidencia | P1 | amplia | C3 — C3-053 |
| F-06 | Festival o escenario local gratuito (música, danza y fiestas locales) | actividad de convocatoria abierta | sin evidencia | P2 | amplia | C2 — C3-035 |
| F-07 | Proyecciones de cine gratuitas | actividad de convocatoria abierta | sin evidencia | P1 | amplia | C0 |
| F-08 | Actividades juveniles en ferias del libro y bibliotecas | actividad de convocatoria abierta | sin evidencia | P2 | amplia | C2 — C3-107 |
| F-09 | Visitas y rutas de patrimonio cultural | actividad de convocatoria abierta | sin evidencia | P2 | amplia | C2 — C3-019 |
| F-10 | Encuentros o torneos presenciales de videojuegos | actividad de convocatoria abierta | sin evidencia | P1 | segmento identificable | C0 |
| F-11 | Retos colaborativos de tecnología (hackathon) | actividad de convocatoria abierta | sin evidencia | P0 | desconocido | C2 — C3-100 |
| F-12 | Bienestar y salud mental de mujeres jóvenes (espacio propio o componente con derivación) | intervención segmentada | prevalencia; registro de atención | P0 | desconocido | C2 — C3-087 |
| F-13 | Protocolo de protección y derivación en actividades con adolescentes | protocolo transversal | registro de atención | no aplica | no aplica | no aplica |
| F-14 | Voluntariado de corta duración con resultados visibles | actividad de convocatoria abierta | objetivo institucional | P1 | desconocido | C3 — C3-011 |
| F-15 | Mujeres jóvenes dedicadas al hogar: población que requiere consulta directa | población que requiere consulta directa | situación documentada | P0 | segmento identificable | no aplica |

**Cómo leer la tabla.** La tabla se genera desde `fichas_actividad.csv`; en la columna Convocatoria se indica la
actividad del registro de la Capa 3 que define el código. Las columnas no se suman ni se comparan entre filas. Una ficha con P2 y C2 no es "mejor" ni
"peor" que una con P0 y C4: responden a preguntas distintas.

---

## 7. Cambios respecto de la primera versión

El detalle está en `resultados/cambios_primera_version.csv` y en `resultados/hallazgos_integrados.csv` (columnas
`estado_v2` y `cambio_v2`).

- **11 propuestas → 15 fichas.**
  - 9 propuestas se reformulan.
  - P09 se descarta tal como estaba (se reformula para quienes ya trabajan por cuenta propia).
  - P11 se reclasifica como protocolo.
  - 4 fichas son nuevas: derechos laborales, lectura, patrimonio y mujeres dedicadas al hogar.
- **Componentes descartados como conclusión:**
  - talleres generales de habilidades digitales;
  - promover el emprendimiento en general;
  - educación sexual integral como actividad de convocatoria;
  - la prioridad a mujeres que no estudian ni trabajan en empleabilidad.
- **Componentes que pasan a "sin evidencia":** cineforo, taller de video, cultura urbana, jóvenes organizadores,
  orientación vocacional y ventas por internet.
- **Hallazgos (62):**
  - 10 corregidos;
  - 5 reemplazados por datos de Lima Este;
  - 4 ampliados;
  - 14 nuevos;
  - 29 sin cambios de contenido (las cifras ahora se leen de los datos);
  - H3-12 se integra en H3-11.
- **Informe:** se elimina el orden implícito ("las más respaldadas", "las mejores candidatas").

---

## 8. Qué no permite afirmar este cruce

- **Interés en participar en cualquier actividad concreta (I2):** ninguna fuente lo pregunta a los jóvenes de Lima
  Este.
- **Preferencias por distrito:** las encuestas no tienen representatividad distrital y la oferta publicada es
  desigual.
- **Horarios preferidos, distancia aceptable, disposición a pagar:** solo hay disponibilidad observada (ENUT) y
  desplazamiento de quienes estudian.
- **Intención de continuar estudios,** ni cuántos ya se preparan en academias.
- **Salud mental e inseguridad por distrito;** salud mental en Lima Este.
- **Convocatoria real de la oferta existente:** las cifras son declaradas y casi nunca informan cupos.
- **Situación de 2026:** las encuestas llegan a 2024 o 2025.

---

## 9. Cómo validar

El equipo decidió (25/09/2026) que la consulta directa y los pilotos son una **fase posterior**. Hasta
entonces, las fichas se presentan como **alternativas derivadas de evidencia secundaria**, y cada una indica qué
parte de la participación concreta queda por validar con jóvenes.

1. **Consulta directa a jóvenes de Lima Este.** Es la única vía para llegar a I2. Debe incluir a las mujeres
   dedicadas al hogar (F-15), en sus hogares o espacios comunitarios. Preguntas:
   - qué actividades y formatos harían;
   - horarios y distancia;
   - cuidado infantil;
   - costo;
   - canales de información;
   - intención de estudiar;
   - seguridad para salir de noche.
2. **Registros administrativos de convocatoria** (Ley 27806: municipalidades, SENAJU, IPD). Permitirían pasar de
   cifras declaradas a cifras verificadas, con cupos, o detectar baja convocatoria (CB). Se pedirían:
   - inscritos, asistentes y cupos por edad y sexo;
   - listas de espera.
3. **Pilotos pequeños con indicadores definidos antes.** Cada ficha indica los suyos. Los umbrales los define el
   equipo; no provienen de los datos.

---

## 10. Limitaciones y pendientes

- **Lima Este sigue siendo un dominio no planificado.** Varias estimaciones por edad o sexo son referenciales. Las de
  la ENUT (~230 jóvenes) son las más imprecisas.
- **Muestra pequeña en E-086.** Las horas de trabajo doméstico de las mujeres que no trabajaron ni estudiaron (Lima
  Metropolitana) tienen CV aceptable, pero una muestra de 43 personas.
- **"No estudia ni trabaja" usa la definición del proyecto.** Si Dato Joven publica su manual de forma abierta, se
  puede reintentar la equivalencia (I2-D3).
- **Informalidad solo hasta 2023** (D16).
- **Fuentes posibles aún no exploradas:**
  - ENDES para salud mental en Lima Este (muestra por verificar);
  - MINEDU (ESCALE) para la cohorte de 5.º de secundaria por distrito;
  - PRONABEC para postulantes a becas (sin eludir bloqueos de acceso).

---

## 11. Validación final de consistencia (25/09/2026)

Revisión pedida por el equipo antes de construir el observatorio, sin rediseñar el modelo. Los controles
automáticos están en `integracion_construir.validar()` y se guardan en `resultados/validacion_integracion.csv`
(10 de 10 correctos). La revisión manual encontró y corrigió:

- **Cuantificadores exagerados:** "casi siempre pagados" para conciertos (58,6 % compró su entrada; se reescribió como
  "la mayoría"), y "casi todos entraron gratis" incluía ferias del libro (76,9 %).
- **Universos implícitos:** cuatro frases no decían de qué grupo era el porcentaje (F-01, F-06, F-15, PT-10).
- **Interpretaciones con tono causal:** PT-01, PT-04, PT-06 y PT-09. Ahora describen coincidencias o motivos
  declarados, no causas.
- **Contradicción entre PT-03 y F-05:** PT-03 decía "sin evidencia de convocatoria"; F-05 tiene un dato comparable (C3).
- **C0 en F-07:** al tener registros no comparables, no aclaraba que la ausencia de evidencia no es evidencia negativa.
- **Evidencia pertinente no usada:**
  - por sexo: preuniversitaria, informalidad, trabajo independiente, festivales y ferias del libro;
  - por edad: 16–19 en la preuniversitaria; festivales, ferias del libro y patrimonio;
  - disponibilidad nocturna de las mujeres (Lima Metropolitana) en F-05, F-12 y F-15;
  - inseguridad nocturna en fichas con probables sesiones nocturnas.

  Se agregaron 14 evidencias.
- **F-13 (protocolo):** el interés y el alcance pasan a "no aplica" (antes, P0 y un conteo de nacimientos).
- **Alcance:** ahora indica ámbito y periodo de cada dato.
- **Paráfrasis imprecisa de la ENUT:** "noches libres" se reemplazó por la definición del indicador (2 horas libres
  seguidas entre 18:00 y 22:00 en el día de semana registrado).

**Distinción entre pertinencia amplia y segmentada.**

- El campo `alcance_tipo` indica dónde se apoya la evidencia:
  - **amplia:** F-05 a F-09, con evidencia sobre toda la juventud de 15–29;
  - **segmento identificable:** F-01 a F-04, F-10 y F-15;
  - **desconocido:** F-11, F-12 y F-14;
  - **no aplica:** F-13.
- El campo `tipo_ficha` describe el diseño de la actividad.
- F-10 es una actividad de convocatoria abierta cuya evidencia de práctica se concentra en hombres. No es una
  contradicción: el observatorio debe mostrar ambos campos.

**Limitaciones que el observatorio debe mostrar obligatoriamente:**

1. **Las fichas son alternativas derivadas de evidencia secundaria.** Ninguna tiene interés declarado en participar
   (I2); la participación concreta se validará con jóvenes en una fase posterior.
2. **"Sin evidencia" (P0, C0) no es evidencia negativa**, y la oferta publicada no es demanda.
3. **Práctica relacionada no es intención de participar;** cada ficha muestra su salto inferencial.
4. **Ámbito de cada dato:**
   - Lima Este es un dominio no planificado: se estima para los siete distritos juntos, nunca por distrito;
   - varios datos son de Lima Metropolitana (salud mental, violencia de pareja, deporte por sexo, disponibilidad por
     sexo) y no describen a Lima Este;
   - Ipsos es de 2019–2022 y Perú urbano.
5. **Periodo:** las encuestas son de 2022–2025 (ENUT: 2024; informalidad: 2022–2023); nada describe 2026.
6. **Las cantidades son órdenes de magnitud con dos bases que no se combinan.** Con la base de Dato Joven, solo
   reflejan el error del porcentaje; por sexo son más inciertas.
7. **"No estudia ni trabaja" es una definición del proyecto,** no la cifra "NINI" de Dato Joven.
8. **La convocatoria son cifras declaradas por quien organiza,** casi nunca con cupos; las señales de demanda valen
   solo para su oferta concreta.
9. **Los registros administrativos (CEM, nacimientos) miden atenciones, no prevalencia.**
10. **La disponibilidad horaria es observada en un día registrado, no una preferencia;** la inseguridad nocturna es
    una condición que coincide con esas franjas, no una causa medida de no participar.
11. **Precisión:** las cifras referenciales van marcadas; las no publicables no se muestran.
12. **"Dónde pilotear" es un criterio operativo,** no una señal de demanda por distrito.


---

## 12. Modelo de priorización (29/09/2026)

El equipo pidió pasar de la descripción sin ranking a un cruce que determine qué tipo de actividades tienen más
posibilidades de convocar, sin basarse solo en la oferta ni solo en el tamaño del público. Las fichas y sus
categorías no cambian: el modelo multicriterio las ordena con seis criterios de reglas fijas, pesos explícitos y
una prueba de robustez con cuatro combinaciones de pesos. La solidez de la evidencia se informa aparte. El detalle
está en `metodologia_modelo_actividades.md`.
