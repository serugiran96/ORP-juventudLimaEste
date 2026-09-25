# Modelo de definición de actividades

Proyecto de análisis de datos sobre las juventudes de Lima Este.

> Estado: Capas 1, 2 y 3 con diagnóstico (notebooks 01, 02 y 03). Integración pendiente.

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
- **Población — jóvenes:** personas de **15 a 30 años**. Cuando una fuente use otro rango de edad, se registrará y se indicará al presentar sus resultados.

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
- **Recolección:** notas de prensa de las siete municipalidades y de entidades públicas (gob.pe, SERPAR, SENAJU), recolectadas respetando el `robots.txt` de cada sitio y codificadas a mano en un registro de 150 actividades (`fuentes/capa3_registro_oferta.csv`). Cada actividad se clasifica como oferta, participación declarada o demanda observada (`fuentes/metodologia_capa3.md`).

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
| 1 | Dato Joven — Observatorio Nacional de Juventud | https://observatorio-juventud.minedu.gob.pe/dato-joven/ | Procesada |
| 2 | Estudios públicos de Ipsos Perú sobre jóvenes y Generación Z | Ver `fuentes/fuentes.md` | Procesada |
| 2 | Encuestas del INEI (ENUT, ENAPRES, ENAHO) | Ver `fuentes/fuentes.md` | Procesadas |
| 3 | Notas de prensa de las municipalidades de Lima Este (gob.pe y munichosica.pe) | Ver `fuentes/fuentes.md` | Procesada |
| 3 | SERPAR, SENAJU, MTPE, IPD, Ministerio de Cultura, DEVIDA, Municipalidad de Lima | Ver `fuentes/fuentes.md` | Procesadas |

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

1. **Aplicar el alcance** (ver [Alcance](#alcance)): usar los siete distritos y el rango de 15 a 30 años como referencia en todas las capas, y registrar cuando una fuente use otro territorio u otro rango de edad.
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
- **Definiciones distintas de juventud:** el proyecto usa 15 a 30 años, pero la definición oficial en Perú (Ley N.º 27802) es de 15 a 29 años. Es probable que los indicadores oficiales, como los de Dato Joven, no incluyan a quienes tienen 30 años; en ese caso se usará el rango de 15 a 29 como aproximación y se indicará así. Además, los estudios sobre la "Generación Z" la definen por año de nacimiento. Estos datos no siempre son comparables directamente.
- **Oferta no es demanda:** la existencia de actividades en la Capa 3 no indica interés ni participación.
- **Visibilidad digital:** la Capa 3 solo recoge lo que se publica en internet. Las organizaciones o actividades sin presencia digital quedarán subrepresentadas, y no todas las municipalidades publican con el mismo detalle.
- **Datos de participación escasos:** es probable que haya pocas cifras de inscripción o asistencia, y que no sean comparables entre fuentes.
- **Fuentes cambiantes:** las páginas web pueden cambiar o desaparecer, por eso se registra la fecha de consulta.

## Estructura del proyecto

| Carpeta | Contenido |
|---|---|
| `data/raw/` | Datos tal como se obtienen de la fuente, sin modificar. |
| `data/processed/` | Datos limpios o anonimizados, listos para el análisis. Diccionario en `data/README.md`. |
| `fuentes/` | Catálogo de fuentes, exploración de Dato Joven, catálogo de tableros y metodología de la Capa 1. |
| `notebooks/` | Notebooks de exploración y análisis (Jupyter). |
| `scripts/` | Código reutilizable: recolección, limpieza y utilidades. |

## Cómo reproducir la Capa 1

Requiere Python 3 con las dependencias de `requirements.txt`. Desde esta carpeta:

```bash
python scripts/catalogo_dato_joven.py      # opcional: actualiza fuentes/catalogo_tableros_dato_joven.csv
python scripts/extraer_dato_joven.py todo  # descarga agregados de Dato Joven -> data/raw/dato_joven/
python scripts/procesar_capa1.py           # limpieza y organización -> data/processed/
python scripts/empleo_enaho.py descargar   # microdatos ENAHO 2022–2025 (~1,5 GB) -> data/raw/enaho/
python scripts/empleo_enaho.py calcular    # empleo 15–29 años, validado con Dato Joven -> data/processed/
jupyter nbconvert --to notebook --execute --inplace notebooks/01_capa1_diagnostico.ipynb
```

Las decisiones metodológicas están en `fuentes/metodologia_capa1.md`.

## Cómo reproducir la Capa 2

```bash
python scripts/capa2_uso_tiempo_enut.py descargar && python scripts/capa2_uso_tiempo_enut.py calcular
python scripts/capa2_cultura_enapres.py descargar && python scripts/capa2_cultura_enapres.py calcular
python scripts/capa2_educacion_internet_enaho.py descargar && python scripts/capa2_educacion_internet_enaho.py calcular
jupyter nbconvert --to notebook --execute --inplace notebooks/02_capa2_intereses.ipynb
```

`capa2_educacion_internet_enaho.py calcular` valida contra Dato Joven, así que requiere haber ejecutado antes
`procesar_capa1.py`. La metodología está en `fuentes/metodologia_capa2.md`.

## Cómo reproducir la Capa 3

```bash
python scripts/capa3_noticias_gobpe.py listar            # notas municipales en gob.pe (2024–2026)
python scripts/capa3_noticias_gobpe.py detalle           # texto de las notas relevantes (~30 min)
python scripts/capa3_noticias_gobpe.py sectores          # notas del MTPE, IPD, Cultura, DEVIDA y Municipalidad de Lima
python scripts/capa3_noticias_gobpe.py detalle_sectores  # su texto (~30 min)
python scripts/capa3_noticias_wp.py                      # munichosica.pe, SERPAR y SENAJU
python scripts/capa3_triaje.py                           # notas candidatas -> data/processed/
python scripts/capa3_validar_registro.py                 # revisa el registro codificado a mano
jupyter nbconvert --to notebook --execute --inplace notebooks/03_capa3_oferta.ipynb
```

El registro `fuentes/capa3_registro_oferta.csv` se codificó a mano a partir de las notas candidatas; los scripts
solo recolectan y seleccionan notas. Las notas publicadas cambian con el tiempo, así que una nueva recolección
puede dar resultados distintos. La metodología está en `fuentes/metodologia_capa3.md`.

## Datos y privacidad

- Los archivos de `data/` **no se suben al repositorio**; se guardan solo en local (ver `.gitignore`). Solo se versionan el código, los notebooks y la documentación.
- Las fuentes digitales pueden contener datos personales de jóvenes, incluidos menores de edad. Antes de analizar o compartir resultados, los datos deben anonimizarse, en línea con la Ley N.º 29733 de Protección de Datos Personales.
- Los datos originales en `data/raw/` no se modifican; cualquier transformación se guarda en `data/processed/`.
