"""Recolecta las notas de prensa de las siete municipalidades de Lima Este publicadas en gob.pe (Capa 3).

Respeta el robots.txt de gob.pe, que prohíbe paginar con el parámetro `sheet=`. Por eso cada búsqueda pide
hasta 100 resultados en una sola página (`filter[per_page]=100`). Si una búsqueda tiene más de 100 resultados,
el rango de fechas se divide en dos y se consulta cada mitad. Hay una pausa de 5 s entre búsquedas y de 3 s
entre notas.

Uso (desde la carpeta del proyecto):
    python scripts/capa3_noticias_gobpe.py listar              # títulos, fechas y enlaces por término de búsqueda
    python scripts/capa3_noticias_gobpe.py listar escolares    # agrega solo los términos indicados al listado
    python scripts/capa3_noticias_gobpe.py detalle             # texto de cada nota (se puede reanudar)
    python scripts/capa3_noticias_gobpe.py sectores            # notas de entidades nacionales y metropolitanas
    python scripts/capa3_noticias_gobpe.py detalle_sectores    # que mencionan los distritos, y su texto

El texto solo se descarga para las notas que la búsqueda de gob.pe devolvió con algún término sobre juventud
(TERMINOS_JUVENTUD) y para las que por su título tratan de empleo, becas o cursos gratuitos (TITULO_EMPLEO),
que suelen estar abiertos a todo público sin mencionar a los jóvenes. Las demás no se descargan.

Salidas en data/raw/capa3/:
- gobpe_listado.csv: una fila por nota única, con los términos de búsqueda que la encontraron.
- noticias_gobpe.csv: las notas con términos sobre juventud, más su texto plano. Es material de revisión: cada
  nota se codifica a mano en fuentes/capa3_registro_oferta.csv.
- gobpe_sectores_listado.csv y noticias_gobpe_sectores.csv: lo mismo para las notas de entidades nacionales y
  de la Municipalidad de Lima que mencionan un distrito de Lima Este (la búsqueda de gob.pe trata varias
  palabras como una frase exacta). De estas se descarga el texto de todas.
"""

import html
import re
import sys
import time
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "raw" / "capa3"
BASE = "https://www.gob.pe"
DESDE, HASTA = date(2024, 1, 1), date(2026, 9, 24)
PAUSA, PAUSA_NOTA = 5, 3

INSTITUCIONES = {  # UBIGEO: (distrito, identificador en gob.pe)
    "150103": ("Ate", "muniate"),
    "150107": ("Chaclacayo", "munichaclacayo"),
    "150111": ("El Agustino", "munielagustino"),
    "150114": ("La Molina", "munilamolina"),
    "150118": ("Lurigancho-Chosica", "munilurigancho"),
    "150132": ("San Juan de Lurigancho", "munisanjuandelurigancho"),
    "150137": ("Santa Anita", "munisantanita"),
}

TERMINOS_JUVENTUD = ["jóvenes", "joven", "juventud", "juvenil", "adolescentes", "estudiantes", "escolares",
                     "vacaciones útiles", "orientación vocacional", "preuniversitaria"]
TERMINOS = TERMINOS_JUVENTUD + ["talleres", "curso", "capacitación", "beca", "empleo", "emprendimiento", "concurso",
                                "festival", "campeonato", "voluntariado", "biblioteca", "cultura", "deporte"]

INSTITUCIONES_SECTORIALES = {  # identificador en gob.pe: entidad
    "mtpe": "Ministerio de Trabajo y Promoción del Empleo",
    "ipd": "Instituto Peruano del Deporte",
    "cultura": "Ministerio de Cultura",
    "devida": "DEVIDA",
    "munilima": "Municipalidad Metropolitana de Lima",
}
# "Ate" solo no sirve: en estas entidades la búsqueda lo encuentra dentro de otras palabras (más de 1 000 notas ajenas).
TERMINOS_TERRITORIO = ["Lurigancho", "Chosica", "distrito de Ate", "Vitarte", "Huaycán", "Chaclacayo", "El Agustino",
                       "La Molina", "Santa Anita"]

TITULO_EMPLEO = re.compile(r"emple|laboral|chamba|becas?\b|cursos? (virtuales )?gratu|cursos virtuales|"
                           r"capacitación gratuita", re.I)

sesion = requests.Session()
sesion.headers["User-Agent"] = "ORP-juventudLimaEste (investigación sin fines de lucro)"


def _texto(fragmento):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragmento or ""))).strip()


def _get(url, params=None, pausa=PAUSA):
    time.sleep(pausa)
    resp = sesion.get(url, params=params, timeout=60)
    resp.raise_for_status()
    return resp.text


def _buscar(slug, termino, desde, hasta):
    """Devuelve las notas de una búsqueda; divide el rango de fechas si hay más de 100 resultados."""
    pagina = _get(f"{BASE}/institucion/{slug}/noticias", {
        "filter[terms]": termino, "filter[start_date]": desde.isoformat(),
        "filter[end_date]": hasta.isoformat(), "filter[per_page]": 100})
    total = re.search(r"(\d+)\s+resultados?", _texto(pagina))
    total = int(total.group(1)) if total else 0
    resultados = pagina.split("js-feeds-search-results", 1)[-1] if total else ""
    notas = []
    for m in re.finditer(r'<a class="text-primary[^"]*"[^>]*href="(/institucion/%s/noticias/(\d+)-[^"]+)">(.*?)</a>'
                         r'.*?<time[^>]*datetime="(\d{4}-\d{2}-\d{2})' % re.escape(slug), resultados, flags=re.S):
        notas.append({"id": int(m.group(2)), "fecha": m.group(4), "titulo": _texto(m.group(3)),
                      "enlace": BASE + m.group(1)})
    if total > len(notas) and hasta > desde:
        medio = desde + (hasta - desde) // 2
        return _buscar(slug, termino, desde, medio) + _buscar(slug, termino, date.fromordinal(medio.toordinal() + 1), hasta)
    if total > len(notas):
        print(f"    aviso: {slug} '{termino}' {desde}: {total} resultados, {len(notas)} leídos")
    return notas


def listar(terminos=None):
    """Sin argumentos consulta todos los TERMINOS; con argumentos, agrega esos términos al listado existente."""
    destino = SALIDA / "gobpe_listado.csv"
    filas = {}
    if terminos and destino.exists():
        previo = pd.read_csv(destino, dtype={"ubigeo": str})
        filas = {f["id"]: {**f, "terminos": set(f["terminos"].split("; "))} for f in previo.to_dict("records")}
    for ubigeo, (distrito, slug) in INSTITUCIONES.items():
        for termino in terminos or TERMINOS:
            for nota in _buscar(slug, termino, DESDE, HASTA):
                fila = filas.setdefault(nota["id"], {"distrito": distrito, "ubigeo": ubigeo, **nota, "terminos": set()})
                fila["terminos"].add(termino)
            print(f"  {distrito}: '{termino}' -> acumulado {sum(f['ubigeo'] == ubigeo for f in filas.values())}")
    df = pd.DataFrame(filas.values())
    df["terminos"] = df["terminos"].map(lambda s: "; ".join(sorted(s)))
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.sort_values(["ubigeo", "fecha"]).to_csv(destino, index=False)
    print(f"{len(df)} notas únicas")


def listar_sectores():
    filas = {}
    for slug, entidad in INSTITUCIONES_SECTORIALES.items():
        for termino in TERMINOS_TERRITORIO:
            for nota in _buscar(slug, termino, DESDE, HASTA):
                fila = filas.setdefault(nota["id"], {"institucion": entidad, **nota, "terminos": set()})
                fila["terminos"].add(termino)
            print(f"  {slug}: '{termino}' -> acumulado {sum(f['institucion'] == entidad for f in filas.values())}")
    df = pd.DataFrame(filas.values())
    df["terminos"] = df["terminos"].map(lambda s: "; ".join(sorted(s)))
    df.sort_values(["institucion", "fecha"]).to_csv(SALIDA / "gobpe_sectores_listado.csv", index=False)
    print(f"{len(df)} notas únicas")


class _Cuerpo(HTMLParser):
    """Texto del bloque `div.feed-content`, que contiene el cuerpo de la nota."""

    def __init__(self):
        super().__init__()
        self.nivel, self.partes = 0, []

    def handle_starttag(self, tag, attrs):
        if self.nivel:
            self.nivel += tag == "div"
        elif tag == "div" and "feed-content" in (dict(attrs).get("class") or ""):
            self.nivel = 1

    def handle_endtag(self, tag):
        if self.nivel and tag == "div":
            self.nivel -= 1

    def handle_data(self, data):
        if self.nivel:
            self.partes.append(data)


def detalle(sectores=False):
    if sectores:
        listado = pd.read_csv(SALIDA / "gobpe_sectores_listado.csv")
        destino, orden = SALIDA / "noticias_gobpe_sectores.csv", ["institucion", "fecha"]
    else:
        listado = pd.read_csv(SALIDA / "gobpe_listado.csv", dtype={"ubigeo": str})
        juventud = listado["terminos"].str.split("; ").map(lambda t: bool(set(t) & set(TERMINOS_JUVENTUD)))
        listado = listado[juventud | listado["titulo"].str.contains(TITULO_EMPLEO)]
        destino, orden = SALIDA / "noticias_gobpe.csv", ["ubigeo", "fecha"]
    hechas = pd.read_csv(destino) if destino.exists() else pd.DataFrame(columns=[*listado.columns, "texto"])
    hechas = hechas[hechas["id"].isin(listado["id"])]  # descarta notas de un listado anterior
    pendientes = listado[~listado["id"].isin(hechas["id"])]
    print(f"{len(pendientes)} notas por descargar ({len(hechas)} ya descargadas)")
    nuevas = []
    for i, fila in enumerate(pendientes.itertuples(index=False), 1):
        parser = _Cuerpo()
        parser.feed(_get(fila.enlace, pausa=PAUSA_NOTA))
        nuevas.append({**fila._asdict(), "texto": re.sub(r"\s+", " ", " ".join(parser.partes)).strip()})
        if i % 25 == 0 or i == len(pendientes):  # guarda el avance para poder reanudar
            hechas = pd.concat([hechas, pd.DataFrame(nuevas)], ignore_index=True)
            hechas.sort_values(orden).to_csv(destino, index=False)
            nuevas = []
            print(f"  {i}/{len(pendientes)}")


if __name__ == "__main__":
    if sys.argv[1] == "listar":
        listar(sys.argv[2:])
    elif sys.argv[1] == "sectores":
        listar_sectores()
    else:
        detalle(sectores=sys.argv[1] == "detalle_sectores")
