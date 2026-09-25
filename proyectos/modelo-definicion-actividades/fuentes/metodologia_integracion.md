# Metodología del cruce de las tres capas

Cómo se integraron la Capa 1 (contexto y necesidades), la Capa 2 (intereses, hábitos y aspiraciones) y la
Capa 3 (oferta y convocatoria) para identificar patrones, brechas y propuestas de actividades con trazabilidad.

- **Fecha:** 25/09/2026.
- **Productos:** `resultados/informe_final.md` (lectura principal), `resultados/hallazgos_integrados.csv`,
  `resultados/patrones.csv`, `resultados/propuestas.csv` y `notebooks/04_integracion.ipynb`.

## 1. Proceso

```
Capas 1, 2 y 3 (notebooks 01–03, registro de oferta)
      │
      ▼
resultados/hallazgos_integrados.csv   49 hallazgos con ID, tipo de evidencia, población, geografía y referencia
      │
      ▼
resultados/patrones.csv               12 patrones, brechas y condiciones de diseño que cruzan capas
      │
      ▼
resultados/propuestas.csv             11 propuestas, cada una con los hallazgos que la sustentan por capa
      │
      ▼
notebooks/04_integracion.ipynb        verifica la trazabilidad y resume el contexto por distrito
```

Cada hallazgo remite a una sección de un notebook, a un archivo procesado o a las actividades del registro de la
Capa 3 (`C3-###`). Cada patrón y cada propuesta remite a hallazgos (`H1-##`, `H2-##`, `H3-##`). El notebook 04
comprueba que todas las referencias existan.

## 2. Reglas

| ID | Regla | Motivo |
|---|---|---|
| I-R1 | **La ausencia de oferta no es evidencia de demanda.** Que no se haya encontrado una actividad solo dice que no se publicó. | La Capa 3 depende de lo que cada municipalidad publica (sesgo de visibilidad). |
| I-R2 | **La frecuencia de oferta no es evidencia de interés.** Que se ofrezcan muchas actividades de un tema refleja las decisiones de quien organiza. | Ídem. |
| I-R3 | **Las señales de demanda se refieren solo a la oferta concreta** en que se observaron (una beca, unos talleres gratuitos) y no se generalizan a un tema. | Decisión del equipo (C3-D9). |
| I-R4 | **Los resultados de actividades para niños y adolescentes no se generalizan a la juventud.** Se citan siempre con su población (por ejemplo, 6–17 años). | Decisión del equipo; solo una parte coincide con 15–29. |
| I-R5 | **Los niveles geográficos no se mezclan.** Un dato de Lima Metropolitana se cita como tal; "Lima Este" solo cuando la estimación es del dominio de los siete distritos o suma de datos distritales. | Metodología de las Capas 1 y 2. |
| I-R6 | **Una brecha es una distancia entre necesidad o práctica documentada y oferta visible.** No prueba que los jóvenes quieran la actividad que falta. | Evita convertir I-R1 en una conclusión encubierta. |
| I-R7 | Los criterios para sugerir **dónde pilotear** son operativos (tamaño de la población, espacios y aliados existentes, registros de necesidad), no de demanda. | No hay datos de interés por distrito. |

## 3. Niveles de evidencia de cada propuesta

Cada propuesta se califica en tres dimensiones por separado. No se combinan en un puntaje: una propuesta puede
tener mucha práctica documentada y ninguna evidencia de convocatoria.

| Nivel | Necesidad (sobre todo Capa 1) | Interés o práctica (sobre todo Capa 2) | Convocatoria (Capa 3) |
|---|---|---|---|
| **Alto** | Evidencia representativa y confiable de Lima Este, o registro distrital, que muestra la necesidad en el segmento. | La misma práctica o actividad, medida en Lima Este con precisión confiable. | Demanda observada en Lima Este para una actividad similar y el mismo segmento. |
| **Medio** | Evidencia representativa de Lima Metropolitana, no desagregable a Lima Este. | Práctica relacionada (no la misma actividad), o medida solo en Lima Metropolitana, o referencial en Lima Este. | Participación declarada con cifras en actividades similares para el mismo segmento en Lima Este, o demanda observada en una oferta similar a escala de Lima. |
| **Bajo** | Solo señales: autoselección o estudios de mercado antiguos; o contexto indirecto. | Solo estudios de mercado antiguos o registros de autoselección. | Participación sin cifras, cifras de otro segmento o de todas las edades, o un solo dato. |
| **Sin evidencia** | No hay datos. | No hay datos. | No se encontró ninguna actividad similar con datos. |

La **convocatoria** es lo que más importa para decidir, y es la dimensión más débil en casi todas las propuestas:
ninguna propuesta llega a "alto", porque la única demanda observada local para jóvenes es de una beca concreta
(I-R3).

## 4. Qué no permite afirmar este cruce

- **Preferencias por distrito:** las encuestas no tienen muestra por distrito y la oferta publicada es desigual.
- **Interés en actividades concretas:** ninguna fuente pregunta a los jóvenes de Lima Este qué actividades harían.
- **Tamaño de la convocatoria esperable:** las cifras de participación son declaradas y no comparables.
- **Situación de 2026:** las encuestas llegan a 2024 o 2025.

## 5. Cómo validar

Las propuestas son **hipótesis de convocatoria**. Antes de escalarlas, se sugiere:

1. **Consulta breve a jóvenes de Lima Este** (colegios, institutos, redes sociales, organizaciones del RENOJ):
   qué actividades harían, en qué horario, a qué distancia, con qué costo, y por qué canal se enteran.
2. **Pilotos pequeños con indicadores definidos de antemano:**

| Indicador | Qué mide | Umbral orientativo (a definir por el equipo) |
|---|---|---|
| Inscritos / cupos y lista de espera | Demanda por la actividad | Cupos llenos en menos de dos semanas |
| Asistencia a la 1.ª sesión / inscritos | Convocatoria real | 60 % o más |
| Asistencia a la 4.ª sesión / 1.ª sesión | Retención | 50 % o más |
| Perfil (edad, sexo, estudia/trabaja) | Si llega al segmento buscado | Según el segmento de cada propuesta |
| Canal por el que se enteró | Qué difusión funciona | — |

Los umbrales son una sugerencia para discutir; no provienen de los datos.
