"""Construye el catálogo de tableros de Power BI de Dato Joven.

Recorre las páginas públicas del portal, obtiene la clave de cada tablero (del iframe
de Power BI) y consulta su estructura para clasificarlo. Resultado:

    fuentes/catalogo_tableros_dato_joven.csv

Uso (desde la carpeta del proyecto):
    python scripts/catalogo_dato_joven.py
"""

import base64
import csv
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from powerbi_publico import ReportePBI

PORTAL = "https://observatorio-juventud.minedu.gob.pe"
SALIDA = Path(__file__).resolve().parent.parent / "fuentes" / "catalogo_tableros_dato_joven.csv"

MODULOS = [
    ("Dato Joven (portada)", "/dato-joven/"),
    ("Política Nacional de Juventud", "/politica-nacional-de-la-juventud/"),
    ("Datos Demográficos", "/dato-joven/datos-demograficos/"),
    ("Indicadores regionales (consolidado)", "/indicadores-regionales/"),
    ("Organizaciones juveniles (RENOJ)", "/renoj/"),
    ("Programa de Voluntariado Juvenil", "/programa-de-voluntariado-juvenil/"),
]
CATEGORIAS = ["educacion", "empleo", "habilidades-digitales", "salud", "participacion-ciudadana",
              "violencia-y-discriminacion", "victimizacion", "juventud-migrante"]

sesion = requests.Session()
sesion.headers["User-Agent"] = "ORP-juventudLimaEste (investigación sin fines de lucro)"


def pagina(ruta):
    time.sleep(1)
    url = ruta if ruta.startswith("http") else PORTAL + ruta
    resp = sesion.get(url, timeout=60)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def claves_powerbi(soup):
    """Claves únicas de los tableros de Power BI enlazados en la página (iframes o enlaces)."""
    claves = []
    for r in re.findall(r"app\.powerbi\.com/view\?r=([A-Za-z0-9=_-]+)", str(soup)):
        clave = json.loads(base64.b64decode(r + "=" * (-len(r) % 4)))["k"]
        if clave not in claves:
            claves.append(clave)
    return claves


def indicadores_de_categoria(categoria):
    """Lista (nombre, descripción, url) de los indicadores de una página de categoría."""
    soup = pagina(f"/indicador-{categoria}/")
    main = soup.find("main") or soup
    textos, salida = [], []
    for el in main.find_all(["h2", "h3", "h4", "p", "a"]):
        if el.name == "a":
            if "Ver" in el.get_text() and el.get("href", "").startswith(PORTAL):
                nombre, descripcion = (textos[-2], textos[-1]) if len(textos) >= 2 else ("", "")
                salida.append((nombre, descripcion, el["href"]))
        else:
            t = " ".join(el.get_text(" ").split())
            if t:
                textos.append(t)
    return salida


def clasificar(tablas):
    if "datosRegionales" in tablas:
        return "encuesta"
    if any(t.startswith("factPoblacion") for t in tablas) and len(tablas) < 15:
        return "poblacion"
    return "registro"


def main():
    filas = []
    for nombre, ruta in MODULOS:
        for clave in claves_powerbi(pagina(ruta)):
            filas.append({"seccion": "modulo", "categoria": "", "nombre": nombre, "descripcion": "",
                          "url_pagina": PORTAL + ruta, "clave": clave})
    vistas = set()
    for categoria in CATEGORIAS:
        for nombre, descripcion, url in indicadores_de_categoria(categoria):
            if url in vistas:
                continue
            vistas.add(url)
            try:
                claves = claves_powerbi(pagina(url))
            except requests.HTTPError as e:
                print(f"  aviso: {url} -> {e}")
                continue
            for clave in claves:
                filas.append({"seccion": "indicador", "categoria": categoria, "nombre": nombre,
                              "descripcion": descripcion, "url_pagina": url, "clave": clave})

    # Metadatos de cada tablero (una vez por clave).
    meta = {}
    for fila in filas:
        clave = fila["clave"]
        if clave not in meta:
            reporte = ReportePBI(clave, sesion)
            tablas = [t for t in reporte.esquema() if not t.startswith(("LocalDate", "DateTableTemplate"))]
            meta[clave] = {"tipo": clasificar(tablas),
                           "ultima_actualizacion": reporte.info["ultima_actualizacion"],
                           "tablas": ";".join(tablas)}
            print(f"{fila['nombre'][:60]:60} {meta[clave]['tipo']}")
        fila.update(meta[clave])
    # Los módulos de portada y consolidado reúnen varios temas.
    for fila in filas:
        if fila["nombre"] in ("Dato Joven (portada)", "Indicadores regionales (consolidado)"):
            fila["tipo"] = "consolidado"

    SALIDA.parent.mkdir(exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        campos = ["seccion", "categoria", "nombre", "descripcion", "tipo", "url_pagina", "clave",
                  "ultima_actualizacion", "tablas"]
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} tableros -> {SALIDA}")


if __name__ == "__main__":
    main()
