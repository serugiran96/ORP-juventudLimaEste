# Modelo de definición de actividades

Proyecto de análisis de datos sobre las juventudes de Lima Este.

> Estado: enfoque definido. Aún no se han recolectado ni descargado datos.

## Objetivo

Analizar la información disponible sobre las juventudes para identificar **necesidades, intereses y oportunidades** que permitan, posteriormente, diseñar actividades pertinentes en Lima Este.

## Alcance

- **Territorio — Lima Este:** para este proyecto comprende siete distritos:
  - Ate
  - Chaclacayo
  - El Agustino
  - La Molina
  - Lurigancho-Chosica (en fuentes oficiales suele figurar como "Lurigancho")
  - San Juan de Lurigancho
  - Santa Anita
- **Población — jóvenes:** personas de **15 a 35 años**. Cuando una fuente use otro rango de edad, se registrará y se indicará al presentar sus resultados.

## Preguntas de análisis

1. ¿Cuáles son las principales necesidades de las juventudes en educación, empleo, salud, seguridad, participación y otros ámbitos? ¿Qué se puede decir específicamente de Lima y Lima Este?
2. ¿Qué intereses, hábitos y aspiraciones tienen los jóvenes peruanos y la Generación Z? ¿En qué medida esos hallazgos pueden aplicarse a Lima Este?
3. ¿Qué actividades, programas, talleres, eventos y oportunidades para jóvenes existen hoy en los distritos de Lima Este? ¿Hay señales de participación en ellas?
4. Al cruzar necesidades, intereses y oferta, ¿dónde hay coincidencias y dónde hay brechas?
5. ¿Qué hipótesis de oportunidades surgen para diseñar actividades, y con qué nivel de evidencia se sostienen?

## Enfoque: tres capas de análisis

### Capa 1 — Contexto, características y necesidades

Describe la situación de las juventudes a partir de indicadores oficiales.

- **Fuente principal:** Dato Joven, del Observatorio Nacional de Juventud.
- **Temas:** demografía, educación, empleo, salud, seguridad, violencia y discriminación, participación ciudadana, competencias digitales, migración y otros indicadores disponibles.
- **Nivel territorial:** cuando exista suficiente desagregación, se priorizará la información de Lima y Lima Este. Si un indicador solo está disponible a nivel nacional o departamental, se usará como contexto y se indicará así.

### Capa 2 — Intereses, hábitos y aspiraciones

Explora qué les interesa a los jóvenes, cómo usan su tiempo y qué esperan de su futuro.

- **Fuentes:** investigaciones públicas de Ipsos y otras fuentes confiables sobre jóvenes peruanos y la Generación Z.
- **Temas:** entretenimiento, cultura, deporte, tecnología, uso digital, educación y capacitación, empleo, emprendimiento, consumo, aspiraciones y uso del tiempo.
- **Registro obligatorio por fuente:** fecha, población estudiada y cobertura geográfica (ver [Registro de fuentes](#registro-de-fuentes)). Así se evita interpretar datos nacionales o antiguos como si representaran directamente a los jóvenes actuales de Lima Este.

### Capa 3 — Evidencia territorial de Lima Este

Identifica la oferta existente de actividades y oportunidades para jóvenes en el territorio.

- **Fuentes:** información pública de municipalidades distritales de Lima Este y de otras organizaciones públicas.
- **Contenido:** actividades, programas, talleres, eventos y oportunidades dirigidas a jóvenes.
- **Oferta no es demanda:** que exista una actividad no significa que sea de interés de los jóvenes. Cuando haya datos de inscripciones, participación o asistencia, se registrarán como una señal adicional de interés.
- **Recolección:** más adelante se evaluará qué información puede obtenerse mediante scraping y cuál requiere recolección manual.

### Integración de las capas

Las tres capas se cruzarán para identificar coincidencias, brechas e hipótesis de oportunidades:

**necesidades detectadas (Capa 1) + intereses y aspiraciones (Capa 2) + oferta territorial existente (Capa 3)**

Guía orientativa para leer el cruce:

| Necesidad | Interés | Oferta en Lima Este | Lectura posible |
|---|---|---|---|
| Sí | Sí | No | Brecha: posible oportunidad prioritaria |
| Sí | Sí | Sí | Coincidencia: revisar alcance, acceso y participación de la oferta |
| Sí | No | — | Necesidad sin interés declarado: requiere un enfoque que la haga atractiva |
| No | Sí | No | Interés no atendido: posible actividad de convocatoria o vínculo |

Los resultados de la integración son **hipótesis** para orientar el diseño de actividades, no conclusiones sobre toda la juventud de Lima Este.

## Fuentes iniciales

| Capa | Fuente | Enlace | Estado |
|---|---|---|---|
| 1 | Dato Joven — Observatorio Nacional de Juventud | https://observatorio-juventud.minedu.gob.pe/dato-joven/ | Por revisar |
| 2 | Estudios públicos de Ipsos Perú sobre jóvenes y Generación Z | Por identificar | Por revisar |
| 2 | Otras investigaciones confiables sobre jóvenes peruanos | Por identificar | Por identificar |
| 3 | Portales y canales oficiales de municipalidades de Lima Este | Por identificar | Por identificar |
| 3 | Otras organizaciones públicas con oferta para jóvenes | Por identificar | Por identificar |

### Registro de fuentes

Cada fuente usada debe documentarse con, al menos:

- Nombre, institución autora y enlace.
- Capa a la que aporta.
- Fecha de publicación y, si se conoce, fecha de recolección de los datos.
- Fecha de consulta.
- Población estudiada (rango de edad y características).
- Cobertura geográfica (nacional, Lima Metropolitana, distrital, etc.).
- Tipo de fuente y metodología (encuesta, registro administrativo, publicación institucional, etc.) y tamaño de muestra, si aplica.

## Metodología general

1. **Aplicar el alcance** (ver [Alcance](#alcance)): usar los siete distritos y el rango de 15 a 35 años como referencia en todas las capas, y registrar cuando una fuente use otro territorio u otro rango de edad.
2. **Inventariar las fuentes** de cada capa y completar su registro.
3. **Recolectar la información** de cada capa. Por ahora, sin scraping; más adelante se evaluará dónde es viable y adecuado.
4. **Limpiar y estandarizar** los datos: categorías temáticas comunes entre capas, distritos, fechas y rangos de edad.
5. **Analizar cada capa** de forma descriptiva, indicando siempre el nivel territorial y la fecha de cada dato.
6. **Integrar las capas** para identificar coincidencias, brechas e hipótesis de oportunidades.
7. **Documentar el alcance de cada hallazgo:** a qué población y territorio representa, y con qué nivel de evidencia se sostiene.

## Limitaciones

- **Desagregación territorial:** es posible que muchos indicadores solo estén disponibles a nivel nacional o departamental, y no por distrito ni para Lima Este.
- **Representatividad:** no se debe afirmar que los datos representan a toda la juventud de Lima Este cuando la fuente no lo permita.
- **Fechas distintas:** las fuentes pueden haberse levantado en años diferentes. Los datos antiguos no necesariamente reflejan la situación actual.
- **Definiciones distintas de juventud:** el proyecto usa 15 a 35 años, pero la definición oficial en Perú (Ley N.º 27802) es de 15 a 29 años. Es probable que los indicadores oficiales, como los de Dato Joven, no cubran el tramo de 30 a 35 años. Además, los estudios sobre la "Generación Z" la definen por año de nacimiento. Estos datos no siempre son comparables directamente.
- **Oferta no es demanda:** la existencia de actividades en la Capa 3 no indica interés ni participación.
- **Visibilidad digital:** la Capa 3 solo recoge lo que se publica en internet. Las organizaciones o actividades sin presencia digital quedarán subrepresentadas, y no todas las municipalidades publican con el mismo detalle.
- **Datos de participación escasos:** es probable que haya pocas cifras de inscripción o asistencia, y que no sean comparables entre fuentes.
- **Fuentes cambiantes:** las páginas web pueden cambiar o desaparecer, por eso se registra la fecha de consulta.

## Estructura del proyecto

| Carpeta | Contenido |
|---|---|
| `data/raw/` | Datos tal como se obtienen de la fuente, sin modificar. |
| `data/processed/` | Datos limpios o anonimizados, listos para el análisis. |
| `notebooks/` | Notebooks de exploración y análisis (Jupyter). |
| `scripts/` | Código reutilizable: recolección, limpieza y utilidades. |

## Datos y privacidad

- Los archivos de `data/` **no se suben al repositorio**; se guardan solo en local (ver `.gitignore`). Solo se versionan el código, los notebooks y la documentación.
- Las fuentes digitales pueden contener datos personales de jóvenes, incluidos menores de edad. Antes de analizar o compartir resultados, los datos deben anonimizarse, en línea con la Ley N.º 29733 de Protección de Datos Personales.
- Los datos originales en `data/raw/` no se modifican; cualquier transformación se guarda en `data/processed/`.
