"""Genera resultados/informe_final.md a partir de las tablas del cruce de las tres capas.

El texto de las secciones 1, 2 y 5–7 es fijo; los patrones y las fichas de propuestas se generan desde
resultados/patrones.csv, resultados/propuestas.csv y resultados/hallazgos_integrados.csv, para que el informe
no se aparte de las tablas. Si se editan las tablas, volver a ejecutar este script.

Uso (desde la carpeta del proyecto):
    python scripts/integracion_informe.py
"""
from pathlib import Path

import pandas as pd

PROY = Path(__file__).resolve().parent.parent
R = PROY / "resultados"
hall = pd.read_csv(R / "hallazgos_integrados.csv").set_index("id")
pat = pd.read_csv(R / "patrones.csv")
prop = pd.read_csv(R / "propuestas.csv").fillna("").set_index("id")

GRUPOS = [
    ("A. Con respaldo en las tres dimensiones", "Necesidad documentada, práctica o interés relacionados y participación declarada con cifras en actividades similares en Lima Este. Son las apuestas más sólidas, aunque su convocatoria no llega a estar demostrada.", ["P01", "P02"]),
    ("B. Práctica alta en Lima Este, convocatoria por medir", "Lo que los jóvenes ya hacen, medido con precisión en Lima Este, pero sin evidencia local de que una actividad organizada los convoque. Son las mejores candidatas para pilotos que midan la convocatoria.", ["P04", "P05", "P06"]),
    ("C. Evidencia parcial: necesidad o práctica relacionada, convocatoria débil o desconocida", "Tienen sustento en alguna dimensión, pero descansan sobre todo en hipótesis. Conviene validarlas antes de invertir.", ["P03", "P08", "P10", "P09", "P07"]),
    ("D. Componente transversal", "Necesidad documentada sin evidencia de interés: se propone integrarlo en otras actividades, no como actividad independiente.", ["P11"]),
]


def lista_hallazgos(celda):
    ids = [x.strip() for x in celda.split(";") if x.strip()]
    if not ids:
        return " sin hallazgos (ninguna fuente mide este aspecto)."
    return "".join(f"\n  - **{i}** ({hall.loc[i, 'tipo_evidencia']}; {hall.loc[i, 'geografia']}): {hall.loc[i, 'enunciado']}" for i in ids)


def ficha(pid):
    p = prop.loc[pid]
    return f"""#### {pid}. {p.propuesta}

{p.descripcion}

| | |
|---|---|
| **Para quién** | {p.segmento} |
| **Nivel de evidencia** | Necesidad: **{p.nivel_necesidad}** · Interés o práctica: **{p.nivel_interes}** · Convocatoria: **{p.nivel_convocatoria}** |
| **Por qué** | {p.sustento} |
| **Barreras relevantes** | {p.barreras} {("(" + p.hallazgos_barreras + ")") if p.hallazgos_barreras else ""} |
| **Qué sabemos de su convocatoria** | {p.convocatoria} |
| **Qué sigue siendo hipótesis** | {p.hipotesis} |
| **Cómo validarla** | {p.validacion} |
| **Dónde podría pilotearse** | {p.donde} |
| **Cautelas** | {p.cautelas} |

<details><summary>Hallazgos que la sustentan</summary>

- **Capa 1 (necesidades):**{lista_hallazgos(p.hallazgos_c1)}
- **Capa 2 (intereses y hábitos):**{lista_hallazgos(p.hallazgos_c2)}
- **Capa 3 (oferta y convocatoria):**{lista_hallazgos(p.hallazgos_c3)}

</details>
"""


resumen_prop = "\n".join(
    f"| {pid} | {prop.loc[pid, 'propuesta']} | {prop.loc[pid, 'segmento']} | {prop.loc[pid, 'nivel_necesidad']} | {prop.loc[pid, 'nivel_interes']} | {prop.loc[pid, 'nivel_convocatoria']} |"
    for _, _, ids in GRUPOS for pid in ids)

bloques_prop = "\n".join(
    f"### {titulo}\n\n{texto}\n\n" + "\n".join(ficha(pid) for pid in ids) for titulo, texto, ids in GRUPOS)

tabla_pat = "\n".join(f"| {r.id} | {r.tipo} | {r.tema} | {r.enunciado} | {r.cautela} |" for r in pat.itertuples())

texto = f"""# Juventudes de Lima Este: necesidades, intereses, oferta y oportunidades de convocatoria

**Organización Rita Poma · Informe final del análisis · 25 de septiembre de 2026**

Siete distritos: Ate, Chaclacayo, El Agustino, La Molina, Lurigancho-Chosica, San Juan de Lurigancho y Santa Anita.
Jóvenes de 15 a 30 años (las fuentes llegan a 29). Periodo prioritario: 2022–2026.

## Resumen

- **En Lima Este viven unos 712 mil jóvenes de 15 a 29 años**; San Juan de Lurigancho concentra el 44 % y Ate el 25 %.
- **Estudio y empleo compiten por el tiempo y el dinero.** Entre quienes no estudian en Lima Este, el 31 % trabaja y
  el 28 % menciona problemas económicos; casi nadie deja de estudiar por falta de interés (2 %). En Lima
  Metropolitana, el desempleo juvenil es de 11,7 % y el 22 % de las mujeres jóvenes no estudia ni trabaja.
- **Lo que los jóvenes hacen** (medido en Lima Este): usan pantallas casi todos (93 %), van al cine (63 % en el
  año), a espectáculos en vivo (45 %) y a conciertos o festivales (21 %), y juegan videojuegos (46 % en el celular).
  El 28 % hace deporte cada semana, con una brecha grande por sexo (49 % de los hombres y 20 % de las mujeres en
  Lima Metropolitana).
- **La oferta publicada casi termina a los 17 años.** De 151 actividades registradas en 2024–2026, solo 44 se
  dirigen a jóvenes, y se concentran en empleo, voluntariado y preparación preuniversitaria. Para jóvenes de 18 a
  29 casi no hay deporte, cultura ni tecnología publicados.
- **La convocatoria casi nunca se puede observar.** Las pocas cifras son declaradas por quien organiza, y las
  únicas señales de demanda son por ofertas concretas y gratuitas (una beca, unos talleres), que no se generalizan.
- **Once propuestas**, ninguna con evidencia alta de convocatoria. Las más respaldadas son la **preparación
  preuniversitaria con orientación y becas** y la **empleabilidad y primer empleo**. **Deporte para 18–29, cultura
  urbana y música en vivo, y cine** tienen práctica alta medida en Lima Este y son las mejores candidatas para
  pilotos que midan la convocatoria.
- **Todas las propuestas son hipótesis de convocatoria** y deben validarse con una consulta a jóvenes y pilotos
  pequeños con indicadores definidos de antemano.

## 1. Cómo leer este informe

El análisis se hizo en tres capas y un cruce:

| Capa | Pregunta | Fuentes principales |
|---|---|---|
| **1. Contexto y necesidades** | ¿Quiénes son y qué necesitan? | Dato Joven (Observatorio Nacional de Juventud), ENAHO |
| **2. Intereses y hábitos** | ¿Qué hacen, qué consumen, qué les impide participar? | ENUT 2024, ENAPRES 2022–2025, ENAHO 2022–2025 (INEI), Ipsos |
| **3. Oferta y convocatoria** | ¿Qué se les ofrece y qué evidencia hay de que asistan? | Notas de las 7 municipalidades, SERPAR, SENAJU, MTPE, IPD, Ministerio de Cultura, DEVIDA |

**Tipos de evidencia.** No todo dato permite lo mismo:

- **Representativa de Lima Este:** estimación de los siete distritos juntos con encuestas del INEI (nunca por
  distrito).
- **Representativa de Lima Metropolitana:** describe a los 43 distritos; se cita como tal, no como Lima Este.
- **Registros administrativos distritales:** nacimientos, casos atendidos; dependen del acceso a los servicios.
- **Señales:** personas u organizaciones autoseleccionadas (voluntariado, RENOJ) y estudios de mercado antiguos (Ipsos).
- **Oferta, participación declarada y demanda observada:** lo que se publicó, las cifras que da quien organiza y
  las señales de más interesados que cupos.

**Reglas del cruce.** La ausencia de oferta no es demanda; la frecuencia de oferta no es interés; una señal de
demanda solo vale para la oferta concreta en que se observó; los resultados de actividades para niños y
adolescentes no se generalizan a la juventud.

Cada afirmación remite a un hallazgo con código (`H1-##`, `H2-##`, `H3-##`) en `resultados/hallazgos_integrados.csv`.

## 2. Lo que sabemos de las juventudes de Lima Este

### Quiénes son y qué necesitan (Capa 1)

- **Población:** ~712 mil jóvenes de 15 a 29 años (2026), un tercio de 15–19; SJL y Ate concentran el 69 % (H1-01).
- **Organización:** 182 organizaciones juveniles acreditadas; densidad baja en los distritos más poblados (SJL,
  Ate, Lurigancho-Chosica, El Agustino); ninguna de deporte ni de participación ciudadana (H1-02).
- **Empleo** (Lima Metropolitana): informalidad de 65 % (2023), desempleo de 11,7 % (2025) y 17,9 % que no estudia
  ni trabaja, 22,1 % entre las mujeres (H1-06, H1-07).
- **Salud mental** (Lima Metropolitana): episodio depresivo en 15,9 % de los jóvenes, 21,6 % de las mujeres (H1-08).
- **Seguridad** (Lima Metropolitana): un tercio dejó de hacer actividades por la delincuencia; dos de cada tres
  mujeres jóvenes se sienten inseguras de noche en su barrio (H1-10).
- **Adolescentes** (registros distritales): tasas de maternidad adolescente por encima de la mediana metropolitana
  en El Agustino, Santa Anita y Ate; el 41 % de los jóvenes atendidos por violencia en los CEM tiene 15–19 años y
  el 94 % son mujeres (H1-13, H1-14).
- **Participación:** el voluntariado llega sobre todo a mujeres estudiantes, no a quienes trabajan (H1-03, H1-04).

### Qué hacen y qué les frena (Capa 2)

- **Pantallas y consumo digital:** 93 % usa dispositivos cada semana; 93 % ve video por internet; 46 % juega en el
  celular y 35 % en línea (Lima Este; H2-01, H2-08).
- **Deporte:** 28 % cada semana en Lima Este; 49 % de los hombres y 20 % de las mujeres en Lima Metropolitana (H2-02).
- **Cultura:** cine 63 %, espectáculos en vivo 45 %, conciertos o festivales 21 %, festivales locales 20 %, ferias
  del libro 19 %, danza 18 % (Lima Este, en el año; H2-07).
- **Barreras:** falta de interés y de tiempo; el dinero pesa en cine y conciertos; "no hay oferta" casi no aparece
  como motivo (H2-09, H2-10). El tiempo es escaso: la mitad estudia y más de la mitad trabaja (H2-06).
- **Estudio:** trabajar (31 %) y los problemas económicos (28 %) son los motivos para no estudiar en Lima Este; la
  falta de interés es mínima (H2-12). Un tercio usa internet para aprender (H2-11).
- **Aspiraciones:** el deseo de emprender solo se midió en 2019–2020 (Ipsos) y no describe a Lima Este hoy (H2-13).

### Qué se ofrece y qué convoca (Capa 3)

- **151 actividades** publicadas en 2024–2026: 44 dirigidas a jóvenes, 53 a niños y adolescentes, 51 a todo
  público; casi todas gratuitas y presenciales (H3-01, H3-04).
- **Lo dirigido a jóvenes**: empleo (13), participación y voluntariado (13) y preparación preuniversitaria (11);
  muy poco en deporte (3), salud mental (3) y tecnología (2) (H3-02).
- **Participación declarada** en actividades para jóvenes: academias preuniversitarias y becas (180 alumnos en
  Chosica, 100 becarios en El Agustino), programas de empleo (62, 50 y 143 jóvenes), una hackathon con 400
  inscripciones (H3-05, H3-07, H3-10).
- **Demanda observada**, siempre por ofertas concretas y gratuitas: una beca en Santa Anita (80 postulantes para
  10 becas), los talleres juveniles de SENAJU (agotados a escala de Lima) y la Academia IPD para 6–17 años (agotada
  en Lima) (H3-06, H3-08, H3-12).
- **Visibilidad desigual:** Chaclacayo casi no publica; SJL no tiene notas de 2024; la oferta de organizaciones
  sociales casi no aparece (H3-18).

## 3. Patrones, brechas y condiciones de diseño

| ID | Tipo | Tema | Enunciado | Cautela |
|---|---|---|---|---|
{tabla_pat}

## 4. Propuestas de actividades

Cada propuesta indica **para quién** hay evidencia, **qué sabemos de su convocatoria** y **qué sigue siendo
hipótesis**. El nivel de evidencia se califica por separado en tres dimensiones (criterios en
`fuentes/metodologia_integracion.md`):

- **Necesidad:** ¿hay una necesidad documentada en ese segmento?
- **Interés o práctica:** ¿los jóvenes ya hacen algo parecido?
- **Convocatoria:** ¿hay evidencia de que una actividad así convoque jóvenes en Lima Este?

| ID | Propuesta | Segmento | Necesidad | Interés o práctica | Convocatoria |
|---|---|---|---|---|---|
{resumen_prop}

{bloques_prop}
## 5. Condiciones de diseño para todas las propuestas

Surgen de la evidencia y aplican a cualquier actividad:

- **Gratuidad o costo mínimo:** el dinero limita el estudio y la asistencia a cine y conciertos, y todas las
  señales de demanda observadas son de ofertas gratuitas (PT-09).
- **Formatos cortos y en horarios posibles:** fines de semana o bloques breves; la mitad estudia y más de la mitad
  trabaja (PT-08).
- **Cercanía y seguridad:** horarios diurnos o espacios seguros y recorridos cortos, sobre todo para mujeres (PT-10).
- **Segmentar por edad:** 15–17 (llegan por colegios), 18–24 (estudio y primer empleo) y 25–29 (empleo), con metas
  y canales distintos (PT-02, PT-12).
- **Enfoque en mujeres jóvenes:** cuentan con más necesidades documentadas y menos práctica deportiva; conviene
  medir su participación en todos los pilotos (PT-06).
- **Difusión propia:** redes sociales, colegios, institutos y organizaciones juveniles; no depender de la
  comunicación municipal (PT-11).
- **Aliarse con lo que existe:** academias municipales, centros de empleo, complejos del IPD, clubes de SERPAR,
  Casa de la Juventud de Santa Anita, organizaciones del RENOJ (H3-17), en lugar de duplicar.

## 6. Límites del análisis

- **No hay datos por distrito** sobre intereses o prácticas: las encuestas representan a Lima Este en conjunto o a
  Lima Metropolitana.
- **Ninguna fuente pregunta** a los jóvenes de Lima Este qué actividades harían.
- **La oferta registrada no es un censo:** depende de lo que cada municipalidad publica; la oferta de
  organizaciones sociales y privadas casi no aparece.
- **Las cifras de participación son declaradas**, aproximadas y no comparables entre sí.
- **Parte de la evidencia es de Lima Metropolitana** (empleo, salud mental, seguridad) y se usa como contexto, no
  como descripción de Lima Este.
- **Las encuestas llegan a 2024 o 2025**; no hay datos de 2026.

## 7. Próximos pasos

1. **Consulta breve a jóvenes de Lima Este** (colegios, institutos, redes, organizaciones del RENOJ) sobre las
   actividades propuestas: interés, horarios, distancia, costo y canal de información.
2. **Pilotos pequeños** de las propuestas de los grupos A y B, con indicadores definidos de antemano: inscritos
   frente a cupos, asistencia a la primera y cuarta sesión, perfil de quienes llegan (edad, sexo, si estudia o
   trabaja) y canal por el que se enteraron.
3. **Contacto directo con las municipalidades**, sobre todo Chaclacayo, Ate y SJL, para conocer su oferta real,
   cupos e inscritos.
4. **Decidir con los resultados** de la consulta y los pilotos qué actividades escalar.

## Trazabilidad técnica

| Archivo | Contenido |
|---|---|
| `resultados/hallazgos_integrados.csv` | 49 hallazgos de las tres capas con tipo de evidencia, población, geografía y referencia técnica |
| `resultados/patrones.csv` | 12 patrones, brechas y condiciones de diseño con sus hallazgos |
| `resultados/propuestas.csv` | 11 propuestas con hallazgos por capa, niveles, hipótesis y validación |
| `notebooks/04_integracion.ipynb` | Verificación de la trazabilidad, contexto por distrito y matriz de evidencia |
| `notebooks/01`–`03` | Análisis de cada capa |
| `fuentes/metodologia_capa1.md`, `metodologia_capa2.md`, `metodologia_capa3.md`, `metodologia_integracion.md` | Decisiones metodológicas |
| `fuentes/capa3_registro_oferta.csv` | Registro de las 151 actividades de la Capa 3 |
"""

(R / "informe_final.md").write_text(texto)
print(f"resultados/informe_final.md: {len(texto.split())} palabras")
