# Metodología de la Capa 2

Registro de fuentes, procesos, decisiones y limitaciones de la Capa 2 (intereses, hábitos y aspiraciones de
las juventudes). Complementa `fuentes.md` (catálogo) y `data/README.md` (diccionario de datos).

- **Fecha:** 25/09/2026.
- **Análisis:** `notebooks/02_capa2_intereses.ipynb`.

## 1. Fuentes y tipo de evidencia

| Tipo | Fuente | Años | Población | Geografía | Uso en el proyecto |
|---|---|---|---|---|---|
| Representativa (cálculo propio) | **ENUT 2024**, INEI: diario de uso del tiempo y satisfacción con el tiempo libre | 2024 | 12+ años (se usan 15–29 y 30+) | Nacional, Lima Metropolitana, Lima Este (dominio no planificado) | Qué hacen los jóvenes en su semana y cuánto tiempo le dedican |
| Representativa (cálculo propio) | **ENAPRES 2022–2025**, capítulo 800A, INEI | 2022–2025 | 14+ años (se usan 15–29 y 30+) | Nacional y Lima Metropolitana por año; Lima Metropolitana y Lima Este agrupando 2022–2025 | Participación cultural, consumo cultural y barreras |
| Representativa (cálculo propio) | **ENAHO 2022–2025**, Módulo 03, INEI | 2022–2025 | 15–29 | Nacional, Lima Metropolitana y Lima Este por año y agrupado | Usos de internet, asistencia educativa y motivos para no estudiar |
| Estudio de mercado | **Ipsos** 2019, 2020 y 2022 (infografías públicas) | 2019–2022 | 13–20 y 18–25 años | Perú urbano | Aspiraciones, diversión y consumo (dimensiones, no estimaciones actuales) |
| Señal exploratoria | Programa de Voluntariado y RENOJ (Capa 1) | Acumulado | Personas y organizaciones autoseleccionadas | Distritos de Lima Este | Solo como señal complementaria |

**Fuentes revisadas y descartadas:**
- **Reporte de Generaciones de Ipsos 2024:** es una encuesta en 29 países sobre el conocimiento de los términos
  generacionales y el tamaño ideal de la familia. No informa sobre intereses juveniles.
- **Ipsos, Generación Z (2017):** el PDF público es solo la portada de la revista *Semana Económica* y no trae
  cifras.
- **SENAJU, *Jóvenes en Agenda* (2025):** es el informe de un concurso de investigaciones hechas por jóvenes,
  no una consulta sobre sus intereses.

## 2. Proceso

```
scripts/microdatos_inei.py                → descarga de módulos y estimación (común a todas las fuentes)
scripts/capa2_uso_tiempo_enut.py          → data/processed/capa2_uso_tiempo_enut.csv
scripts/capa2_cultura_enapres.py          → data/processed/capa2_cultura_enapres.csv
scripts/capa2_educacion_internet_enaho.py → data/processed/capa2_educacion_internet_enaho*.csv
fuentes/capa2_estudios_ipsos.csv          → cifras de Ipsos transcritas a mano
notebooks/02_capa2_intereses.ipynb        → análisis y gráficos
```

Cada script tiene dos pasos: `descargar` (microdatos públicos del portal del INEI en `data/raw/`) y `calcular`.

## 3. Decisiones metodológicas

| ID | Decisión | Motivo |
|---|---|---|
| C2-D1 | **Lima Este** (7 distritos juntos) se estima como **dominio no planificado**, nunca por distrito. Se publica si el CV ≤ 15 %; se marca como referencial entre 15 % y 25 %; no se publica si el CV > 25 %. Siempre se muestra junto al valor de Lima Metropolitana. | Decisión del equipo (25/09/2026). Las encuestas no están diseñadas para Lima Este, pero su muestra lo permite (ENAHO: ~700 jóvenes al año; ENAPRES: ~180; ENUT: ~230). La estimación por dominio no tiene sesgo, pero sí más error. |
| C2-D2 | Error estándar por **linealización de razones**, con conglomerados y estratos, e incluyendo toda la muestra (las observaciones fuera del dominio cuentan como cero). | Es la forma correcta de estimar el error en dominios no planificados. Es el mismo método validado con Dato Joven en la Capa 1. |
| C2-D3 | En la **ENAPRES y la ENUT**, el estrato se aproxima con **departamento × área**. | Las bases de 2024–2025 (ENAPRES) y la ENUT no traen el estrato de diseño. La aproximación tiende a sobrestimar el error (es conservadora). |
| C2-D4 | La **ENAPRES** se analiza por año para Lima Metropolitana y el país, y **agrupando 2022–2025** para Lima Este y Lima Metropolitana. | Con ~180 jóvenes al año, Lima Este no alcanza la precisión mínima en una sola ola. El agrupado describe el periodo, no un año concreto. |
| C2-D5 | La asistencia educativa se mide como en Dato Joven: **asiste** (`p307`), no solo matriculado (`p306`). | Con la matrícula, la réplica de la asistencia universitaria difería 2–3 puntos; con la asistencia, la diferencia es de ±1 punto. |
| C2-D6 | **ENUT:** una franja de 10 minutos cuenta para un grupo de actividades si este aparece en cualquiera de sus tres registros simultáneos (una sola vez por grupo). Horas semanales = 5 × día de semana + sábado + domingo. | Refleja el tiempo en que la persona hizo la actividad, sea principal o simultánea. La suma de todos los grupos puede superar las 168 horas semanales. |
| C2-D7 | **ENUT:** los traslados al estudio se separan de los traslados al trabajo. | El INEI incluye los traslados al estudio en el tiempo de estudio; separarlos permite replicar su cifra (validación). |
| C2-D8 | **Ipsos** se usa solo para identificar dimensiones (aspiraciones, emprendimiento, diversión, consumo). No se combina con las estimaciones del INEI ni se atribuye a Lima Este. | Población (13–20 o 18–25 años), año (2019–2022) y cobertura (Perú urbano) distintos a los del proyecto. |
| C2-D9 | Los intereses declarados del voluntariado no se usan para priorizar temas. | Entre el 81 % y el 93 % marca "sí" en cada una de las seis temáticas, así que no discriminan (Capa 1). |

## 4. Validaciones

| Fuente | Qué se comparó | Resultado |
|---|---|---|
| ENAPRES | Asistencia a teatro, población de 14+ años, nacional, 2024 | 8,6 %, igual a la cifra publicada por el Ministerio de Cultura |
| ENAHO | Uso de internet (15–29) en Lima Metropolitana y nacional, 2022–2025, frente a Dato Joven | Diferencia máxima de 0,2 puntos |
| ENAHO | Asistencia a educación universitaria (17–24), frente a Dato Joven | Diferencia máxima de 1,0 punto (Lima Metropolitana: ±0,5) |
| ENUT | Horas semanales de estudio de mujeres y hombres de 12–19 años que estudian, frente al informe del INEI (42,2 y 40,5 h) | 42,8 y 40,8 h (diferencia ≤ 0,6 h) |

## 5. Limitaciones

- **Lima Este es un dominio no planificado:** sus estimaciones tienen más error y algunas son referenciales o no
  publicables. **No hay datos por distrito.** Lima Este forma parte de Lima Metropolitana, así que las
  comparaciones entre ambas son descriptivas.
- **La ENUT es de un solo año (2024)** y su muestra de Lima Este es pequeña (~230 jóvenes).
- **Las encuestas del INEI miden prácticas, no intereses declarados.** No preguntan qué actividades les
  gustaría hacer ni en qué talleres participarían. La "falta de interés" es un motivo de no asistencia, no una
  preferencia positiva.
- **Aspiraciones y emprendimiento:** el único dato disponible es de Ipsos (2019–2020, 13–20 años, Perú urbano).
  No hay dato representativo reciente ni local.
- **Edades:** los módulos culturales y de uso del tiempo incluyen a personas desde 14 y 12 años; se filtró
  15–29. Ninguna fuente llega a 30 años de forma separada.
- **Periodo parcial:** 2026 no está disponible en ninguna encuesta.

## 6. Pendientes

- Buscar evidencia representativa y reciente sobre **aspiraciones laborales y emprendimiento** juvenil.
- Si el proyecto recoge información primaria (por ejemplo, una consulta a jóvenes de Lima Este), priorizar
  lo que las encuestas no miden: **intereses declarados** en actividades concretas, horarios disponibles y
  barreras de acceso.
