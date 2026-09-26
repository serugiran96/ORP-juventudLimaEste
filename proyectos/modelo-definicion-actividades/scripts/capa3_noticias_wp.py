"""Recolecta noticias sobre oferta juvenil de sitios públicos con API de WordPress (Capa 3).

Sitios (todos permiten el rastreo en su robots.txt):
- munichosica.pe  — Municipalidad de Lurigancho-Chosica (Crawl-delay: 3 s)
- www.serpar.gob.pe — Servicio de Parques de Lima (clubes zonales Huiracocha, en San Juan de Lurigancho,
  y Cahuide, en Ate)
- juventud.gob.pe — Secretaría Nacional de la Juventud (SENAJU), notas que mencionan distritos de Lima Este
  (Crawl-delay: 3 s)

Las notas de prensa que las siete municipalidades publican en gob.pe se recolectan con
capa3_noticias_gobpe.py.

Uso (desde la carpeta del proyecto):
    python scripts/capa3_noticias_wp.py                # todos los sitios
    python scripts/capa3_noticias_wp.py senaju         # solo los sitios indicados

Salida: data/raw/capa3/noticias_{sitio}.csv, una fila por noticia única (fecha, título, enlace y texto
plano). Es material de revisión: cada noticia se codifica a mano en fuentes/capa3_registro_oferta.csv.
"""

import html
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "raw" / "capa3"
DESDE = "2024-01-01T00:00:00"

SITIOS = {
    "munichosica": {"base": "https://munichosica.pe", "pausa": 3,
                    "terminos": ["joven", "juventud", "adolescente", "taller", "vacaciones útiles", "deporte",
                                 "cultura", "beca", "empleo", "concurso", "festival", "voluntari", "biblioteca",
                                 "capacitación", "curso"]},
    "serpar": {"base": "https://www.serpar.gob.pe", "pausa": 2,
               "terminos": ["Huiracocha", "Wiracocha", "Cahuide"]},
    # En WordPress, varias palabras se buscan juntas (todas deben aparecer) y las comillas buscan la frase exacta.
    "senaju": {"base": "https://juventud.gob.pe", "pausa": 3,
               "terminos": ['"distrito de Ate"', '"en Ate"', "Huaycán", "Vitarte", "Chaclacayo", "El Agustino",
                            "La Molina", "Lurigancho", "Chosica", "Santa Anita", '"Lima Este"']},
}

sesion = requests.Session()
sesion.headers["User-Agent"] = "ORP-juventudLimaEste (investigación sin fines de lucro)"


def _texto(fragmento):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragmento or ""))).strip()


def recolectar(nombre, conf):
    filas = {}
    for termino in conf["terminos"]:
        pagina = 1
        while True:
            time.sleep(conf["pausa"])
            resp = sesion.get(f"{conf['base']}/wp-json/wp/v2/posts", timeout=60, params={
                "search": termino, "after": DESDE, "per_page": 50, "page": pagina,
                "_fields": "id,date,link,title,content"})
            if resp.status_code == 400:  # página fuera de rango
                break
            resp.raise_for_status()
            posts = resp.json()
            for p in posts:
                fila = filas.setdefault(p["id"], {"sitio": nombre, "id": p["id"], "fecha": p["date"][:10],
                                                  "titulo": _texto(p["title"]["rendered"]), "enlace": p["link"],
                                                  "texto": _texto(p["content"]["rendered"]), "terminos": set()})
                fila["terminos"].add(termino)
            if pagina >= int(resp.headers.get("X-WP-TotalPages", 1)):
                break
            pagina += 1
        print(f"  {nombre}: '{termino}' -> acumulado {len(filas)} noticias")
    df = pd.DataFrame(filas.values())
    df["terminos"] = df["terminos"].map(lambda s: "; ".join(sorted(s)))
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.sort_values("fecha").to_csv(SALIDA / f"noticias_{nombre}.csv", index=False)
    return df


if __name__ == "__main__":
    for nombre in sys.argv[1:] or SITIOS:
        df = recolectar(nombre, SITIOS[nombre])
        print(f"{nombre}: {len(df)} noticias desde {DESDE[:10]}")
