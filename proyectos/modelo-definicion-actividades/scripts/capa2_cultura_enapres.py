"""Participación cultural de jóvenes con microdatos de la ENAPRES (capítulo 800A), 2022-2025.

El capítulo 800A ("Patrimonio, servicios y bienes culturales") se aplica a una persona de 14 años
o más por hogar. Pregunta por los últimos 12 meses: visitas al patrimonio, asistencia a 11 tipos de
espectáculos y servicios culturales (con frecuencia, forma de entrada y motivo de no asistencia) y
acceso a 16 tipos de bienes culturales (libros, música, video, videojuegos, etc.).

Uso (desde la carpeta del proyecto):
    python scripts/capa2_cultura_enapres.py descargar  # -> data/raw/enapres/
    python scripts/capa2_cultura_enapres.py calcular   # -> data/processed/capa2_cultura_enapres.csv

Estimaciones:
- Jóvenes de 15-29 años y, como contraste, adultos de 30 años o más.
- Lima Metropolitana (provincia de Lima) y nacional: por año.
- Lima Metropolitana y Lima Este (7 distritos): 2022-2025 agrupados. Lima Este es un dominio no
  planificado por el INEI: es una estimación propia, que solo se publica si su CV lo permite.
- Error estándar por linealización. Conglomerado = CONGLOMERADO; como la base de 2024-2025 no trae el
  estrato, se usa departamento × área como estrato aproximado en todos los años (tiende a
  sobrestimar el error, es decir, es conservador).
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from microdatos_inei import LIMA_ESTE, clasificar_precision, descargar, razon

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "enapres"
SALIDA = RAIZ / "data" / "processed" / "capa2_cultura_enapres.csv"

CODIGOS = {2022: (785, 1734), 2023: (903, 1822), 2024: (965, 1863), 2025: (1030, 2078)}

SERVICIOS = {1: "Teatro", 2: "Danza", 3: "Circo", 4: "Espectáculo musical (conciertos, festivales)",
             5: "Cine", 6: "Exposición de fotografía, pintura o arte", 7: "Feria artesanal",
             8: "Biblioteca o sala de lectura", 9: "Feria del libro",
             10: "Festival local o tradicional (fiestas patronales, carnavales)", 11: "Otros servicios culturales"}
PATRIMONIO = {1: "Monumento histórico", 2: "Sitio arqueológico", 3: "Museo"}
BIENES = {1: "Libros impresos", 2: "Periódicos impresos", 3: "Revistas impresas", 4: "Libros digitales",
          5: "Periódicos digitales", 6: "Revistas digitales", 7: "Música por internet",
          8: "Películas o video por internet", 9: "Videojuegos en dispositivos móviles",
          10: "Videojuegos multijugador en línea", 11: "Películas o video en CD/Blu-ray", 12: "Música en CD",
          13: "Videojuegos en consola/CD", 14: "Obras de arte", 15: "Productos artesanales",
          16: "Otros productos culturales"}
MOTIVOS = {1: "Falta de tiempo", 2: "Falta de interés", 3: "Falta de dinero",
           4: "No tiene información oportuna", 5: "No hay ofertas", 6: "Otra"}
ENTRADA = {1: "Comprada", 2: "Pagada por otra persona", 3: "Entrada libre", 4: "Otra forma"}


def descargar_todo():
    for anio, (codigo, modulo) in CODIGOS.items():
        archivos = descargar(codigo, modulo, RAW / f"{anio}_cap800A", formato="CSV")
        print(f"  {anio}: {[a.name for a in archivos]}")


def _leer(anio):
    ruta = next((RAW / f"{anio}_cap800A").glob("*.csv"))
    primera = ruta.open(encoding="latin1").readline()
    sep = ";" if primera.count(";") > primera.count(",") else ","
    df = pd.read_csv(ruta, sep=sep, encoding="latin1", low_memory=False, dtype=str)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    # La base de 2023 usa punto y coma como separador y coma decimal ("239,665").
    decimal = (lambda s: s.str.replace(",", ".", regex=False)) if sep == ";" else (lambda s: s)
    num = lambda c: pd.to_numeric(decimal(df[c]), errors="coerce") if c in df else pd.Series(np.nan, index=df.index)
    out = pd.DataFrame({
        "anio": anio,
        "ubigeo": df["CCDD"].str.zfill(2) + df["CCPP"].str.zfill(2) + df["CCDI"].str.zfill(2),
        "estrato": df["CCDD"].str.zfill(2) + "_" + df["AREA"].astype(str),
        "conglomerado": f"{anio}_" + df["CONGLOMERADO"].astype(str),
        "factor": num("FACTOR"),
        "edad": num("P208_A"),
        "sexo": num("P207").map({1: "hombre", 2: "mujer"}),
    })
    for k in SERVICIOS:
        for p in ["8", "10", "12"]:
            out[f"s{p}_{k}"] = num(f"P800A_{p}_{k}")
    for k in PATRIMONIO:
        out[f"pat_{k}"] = num(f"P800A_{k}_1")
    for k in BIENES:
        out[f"b13_{k}"] = num(f"P800A_13_{k}")
    # Solo personas con factor y edad válidos (informantes del capítulo).
    return out[out["factor"].notna() & out["edad"].notna() & out["s8_1"].notna()].copy()


def _estimar(df, dominios):
    """Calcula todos los indicadores para cada dominio (nombre -> máscara booleana)."""
    filas = []
    arg = (df["factor"], df["estrato"], df["conglomerado"])
    todos = pd.Series(1.0, index=df.index)

    def agregar(dom, familia, item, categoria, num, den):
        valor, ee, n = razon(*arg, num, den, dominios[dom])
        filas.append({**claves[dom], "familia": familia, "item": item, "categoria": categoria,
                      "valor": valor, "ee": ee, "n_muestral": n})

    for dom in dominios:
        # Asistencia a servicios culturales
        for k, nombre in SERVICIOS.items():
            asistio = (df[f"s8_{k}"] == 1).astype(float)
            agregar(dom, "asistencia", nombre, "Sí", asistio, todos)
            # Forma de entrada, entre quienes asistieron
            con_entrada = df[f"s10_{k}"].notna() & (asistio == 1)
            for cod, etiqueta in ENTRADA.items():
                agregar(dom, "forma_de_entrada", nombre, etiqueta, (df[f"s10_{k}"] == cod) & con_entrada, con_entrada)
            # Motivo principal de no asistir, entre quienes no asistieron
            no = (df[f"s8_{k}"] == 2) & df[f"s12_{k}"].notna()
            for cod, etiqueta in MOTIVOS.items():
                agregar(dom, "motivo_no_asistencia", nombre, etiqueta, (df[f"s12_{k}"] == cod) & no, no)
        en_vivo = df[[f"s8_{k}" for k in [1, 2, 3, 4, 6]]].eq(1).any(axis=1)
        agregar(dom, "asistencia", "Algún espectáculo o exposición en vivo (teatro, danza, circo, música, arte)",
                "Sí", en_vivo, todos)
        agregar(dom, "asistencia", "Algún servicio cultural (cualquiera de los 11)", "Sí",
                df[[f"s8_{k}" for k in SERVICIOS]].eq(1).any(axis=1), todos)
        # Patrimonio
        for k, nombre in PATRIMONIO.items():
            agregar(dom, "patrimonio", nombre, "Sí", df[f"pat_{k}"] == 1, todos)
        # Bienes culturales
        for k, nombre in BIENES.items():
            agregar(dom, "bienes_culturales", nombre, "Sí", df[f"b13_{k}"] == 1, todos)
    return filas


def calcular():
    datos = pd.concat([_leer(a) for a in CODIGOS], ignore_index=True)
    lm = datos["ubigeo"].str.startswith("1501")
    le = datos["ubigeo"].isin(LIMA_ESTE)
    joven = datos["edad"].between(15, 29)
    adulto = datos["edad"] >= 30
    resultados = []
    global claves
    for anio in CODIGOS:
        a = datos["anio"] == anio
        dominios, claves = {}, {}
        for geo, m_geo in [("lima_metropolitana", lm), ("nacional", pd.Series(True, index=datos.index))]:
            for edad, m_edad in [("15-29", joven), ("30+", adulto)]:
                nombre = f"{geo}|{edad}|total"
                dominios[nombre] = a & m_geo & m_edad
                claves[nombre] = {"periodo": str(anio), "nivel_geografico": geo, "grupo_edad": edad, "sexo": "total"}
        # Validación: teatro, población de 14 años o más, nacional (dato publicado por el Ministerio de Cultura)
        dominios["nacional|14+|total"] = a & (datos["edad"] >= 14)
        claves["nacional|14+|total"] = {"periodo": str(anio), "nivel_geografico": "nacional", "grupo_edad": "14+",
                                        "sexo": "total"}
        resultados += _estimar(datos, dominios)
        print(f"  {anio}: listo")

    # 2022-2025 agrupados: Lima Metropolitana y Lima Este, por sexo.
    dominios, claves = {}, {}
    for geo, m_geo in [("lima_metropolitana", lm), ("lima_este", le)]:
        for sexo in ["total", "hombre", "mujer"]:
            m_sexo = pd.Series(True, index=datos.index) if sexo == "total" else datos["sexo"] == sexo
            for edad, m_edad in [("15-29", joven)] + ([("30+", adulto)] if sexo == "total" else []):
                nombre = f"{geo}|{edad}|{sexo}"
                dominios[nombre] = m_geo & m_edad & m_sexo
                claves[nombre] = {"periodo": "2022-2025", "nivel_geografico": geo, "grupo_edad": edad, "sexo": sexo}
    resultados += _estimar(datos, dominios)
    print("  2022-2025 agrupado: listo")

    res = pd.DataFrame(resultados)
    res["cv"] = 100 * res["ee"] / res["valor"]
    res.loc[res["valor"] == 0, "cv"] = np.nan
    res["precision"] = clasificar_precision(res["cv"])
    # Proporciones de 0 % no tienen CV; se publican si la muestra del denominador es suficiente.
    res.loc[(res["valor"] == 0) & (res["n_muestral"] >= 30), "precision"] = "confiable"
    res["valor_publicable"] = res["valor"].where(res["precision"] != "no_publicable")
    res["fuente"] = "ENAPRES 2022-2025, capítulo 800A (INEI), cálculo propio"
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    res.round(3).to_csv(SALIDA, index=False)

    teatro = res[(res.grupo_edad == "14+") & (res.item == "Teatro") & (res.familia == "asistencia")]
    print("\nValidación: asistencia a teatro, población de 14+ años, nacional (%):")
    print(teatro[["periodo", "valor", "cv"]].round(1).to_string(index=False))
    print(f"\n{len(res)} estimaciones -> {SALIDA.name}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paso", choices=["descargar", "calcular"])
    {"descargar": descargar_todo, "calcular": calcular}[p.parse_args().paso]()
