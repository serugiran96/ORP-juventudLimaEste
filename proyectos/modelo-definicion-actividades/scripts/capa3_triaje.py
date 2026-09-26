"""Selecciona las notas candidatas para el registro de oferta de la Capa 3 y extrae fragmentos de apoyo.

No clasifica ni decide nada: solo reduce el número de notas que hay que leer y señala dónde están las edades,
los costos, las cifras y las posibles señales de demanda. La codificación final es manual y está en
fuentes/capa3_registro_oferta.csv.

Criterio de candidata: la nota menciona a jóvenes o adolescentes (o estudiantes, preuniversitarios, un rango
de edad que empieza entre 12 y 29 años) **y** algún tipo de actividad, programa, servicio o espacio. No cuentan
los nombres de oficinas o lugares que contienen "juventud" (por ejemplo, "Subgerencia de ... y Juventudes").

Uso (desde la carpeta del proyecto, después de los scripts capa3_noticias_*.py):
    python scripts/capa3_triaje.py

Salida: data/processed/capa3_notas_candidatas.csv
"""

import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CRUDOS = RAIZ / "data" / "raw" / "capa3"

JUVENTUD = re.compile(r"\bj[oó]ven(es)?\b|juventud|juvenil|adolescen|universitari|preuniversitari|escolares|"
                      r"estudiantes|secundaria|\b(1[2-9]|2\d) (a|y|hasta) \d{2} años", re.I)
# Nombres de oficinas y lugares que contienen "juventud" pero no dicen nada del público de la actividad.
NOMBRES_PROPIOS = re.compile(r"(sub)?gerencia[^.;]{0,90}?juventud(es)?|coliseo de la juventud|secretaría nacional de la "
                             r"juventud|pueblo joven", re.I)
ACTIVIDAD = re.compile(r"taller|curso|capacitaci|feria|festival|concurso|campeonato|torneo|olimpiada|beca|"
                       r"programa|voluntari|charla|escuela|academia|vacaciones útiles|orientación vocacional|"
                       r"empleo|convocatoria|inscrip|clases|certamen|encuentro|biblioteca|centro cultural|"
                       r"complejo deportivo|polideportivo|casa de la juventud|juegos|brigada|exposici|consultivo|cconna|"
                       r"municipio escolar|patrulla|danza|reforzamiento", re.I)

PATRONES = {
    "edades": r"(?:de|entre|desde|a partir de|mayores de|menores de|hasta)(?: los)? \d{1,2}(?: (?:a|y|hasta) \d{1,2})? años",
    "costo": r"gratu\w+|sin costo|costo social|S/\.?\s?\d[\d.,]*|\d+ soles",
    "cifras": r"(?:más de|alrededor de|cerca de|un total de|aproximadamente|superó los|supera los)?\s?"
              r"\b\d[\d.,]*\s(?:\w+\s){0,3}(?:participantes|inscritos|inscritas|jóvenes|asistentes|estudiantes|"
              r"vecinos|niños|adolescentes|personas|beneficiarios|beneficiados|voluntarios|alumnos|deportistas|"
              r"equipos|vacantes|cupos|visitantes|postulantes|becas|becarios|organizaciones|empresas|puestos)",
    "demanda": r"agotad\w+|lista de espera|cupos? (?:limitados|completos|llenos|agotados)|ampli\w+ (?:el|los|las)? ?"
               r"(?:vacantes|cupos|plazo)|nuevas vacantes|alta demanda|gran demanda|super\w+ (?:la|las|lo)? ?"
               r"(?:meta|expectativas|previsto)|récord",
}


def es_candidata(texto):
    limpio = NOMBRES_PROPIOS.sub(" ", texto)
    return bool(JUVENTUD.search(limpio)) and bool(ACTIVIDAD.search(limpio))


def _fragmentos(texto, patron, ancho=70, maximo=6):
    salida = []
    for m in re.finditer(patron, texto, flags=re.I):
        frag = texto[max(0, m.start() - ancho):m.end() + ancho].strip()
        if not any(frag[ancho // 2:-ancho // 2] in s for s in salida):
            salida.append(frag)
        if len(salida) == maximo:
            break
    return " || ".join(salida)


TERRITORIO = {"Lurigancho": "San Juan de Lurigancho o Lurigancho-Chosica", "Chosica": "Lurigancho-Chosica",
              "distrito de Ate": "Ate", "Ate": "Ate", "Vitarte": "Ate", "Huaycán": "Ate", "Chaclacayo": "Chaclacayo", "El Agustino": "El Agustino",
              "La Molina": "La Molina", "Santa Anita": "Santa Anita"}


def cargar():
    partes = []
    gobpe = pd.read_csv(CRUDOS / "noticias_gobpe.csv", dtype={"ubigeo": str})
    gobpe["sitio"] = "gob.pe"
    partes.append(gobpe)
    sectores = pd.read_csv(CRUDOS / "noticias_gobpe_sectores.csv")
    sectores["sitio"] = "gob.pe: " + sectores["institucion"]
    sectores["distrito"] = sectores["terminos"].map(
        lambda t: "; ".join(sorted({TERRITORIO[x] for x in t.split("; ")})))
    partes.append(sectores.assign(ubigeo=""))
    for sitio, distrito, ubigeo in [("munichosica", "Lurigancho-Chosica", "150118"),
                                    ("serpar", "Varios (SERPAR)", ""), ("senaju", "Varios (SENAJU)", "")]:
        df = pd.read_csv(CRUDOS / f"noticias_{sitio}.csv")
        partes.append(df.assign(distrito=distrito, ubigeo=ubigeo))
    cols = ["sitio", "distrito", "ubigeo", "id", "fecha", "titulo", "enlace", "terminos", "texto"]
    return pd.concat([p[cols] for p in partes], ignore_index=True)


if __name__ == "__main__":
    notas = cargar()
    notas["texto"] = notas["texto"].fillna("")
    completo = notas["titulo"] + ". " + notas["texto"]
    candidata = completo.map(es_candidata)
    # En las entidades nacionales y metropolitanas, el distrito debe aparecer en el texto (no solo en otra nota
    # enlazada o en el menú), con mayúscula inicial para no confundir "Ate" con otras palabras.
    externa = notas["sitio"].str.startswith("gob.pe: ")
    lugares = r"\b(?:" + "|".join(TERRITORIO) + r")\b"
    candidata &= ~externa | completo.str.contains(lugares)
    cand = notas[candidata].copy()
    for nombre, patron in PATRONES.items():
        cand[nombre] = (cand["titulo"] + ". " + cand["texto"]).map(lambda t, p=patron: _fragmentos(t, p))
    cand["n_caracteres"] = cand["texto"].str.len()
    salida = RAIZ / "data" / "processed" / "capa3_notas_candidatas.csv"
    cand.drop(columns="texto").sort_values(["sitio", "distrito", "fecha"]).to_csv(salida, index=False)
    print(f"{len(notas)} notas, {len(cand)} candidatas")
    print(cand.groupby("sitio").size().to_string())
