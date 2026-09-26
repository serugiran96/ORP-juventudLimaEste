"""Valida fuentes/capa3_registro_oferta.csv, el registro de oferta de la Capa 3 codificado a mano.

Comprueba las listas cerradas de valores y las reglas de evidencia de fuentes/metodologia_capa3.md. Conviene
ejecutarlo después de editar el registro.

Uso (desde la carpeta del proyecto):
    python scripts/capa3_validar_registro.py
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "fuentes" / "capa3_registro_oferta.csv"

UBIGEO = {"Ate": "150103", "Chaclacayo": "150107", "El Agustino": "150111", "La Molina": "150114",
          "Lurigancho-Chosica": "150118", "San Juan de Lurigancho": "150132", "Santa Anita": "150137"}
VALORES = {
    "ambito": {"distrital", "metropolitano", "nacional"},
    "tipo_organizador": {"municipalidad distrital", "Municipalidad de Lima / SERPAR", "gobierno nacional",
                         "alianza público-privada", "sociedad civil", "privado"},
    "tipo_oferta": {"taller o curso", "programa", "evento", "feria", "concurso o competencia", "servicio",
                    "espacio o infraestructura", "convocatoria de voluntariado", "beca o premio"},
    "incluye_15_29": {"juventud", "adolescentes", "todo público", "no", "no indica"},
    "costo": {"gratuito", "pagado", "mixto", "no indica"},
    "modalidad": {"presencial", "virtual", "mixta", "no indica"},
    "evidencia": {"oferta", "participación declarada", "demanda observada"},
}
TEMAS = {"deporte", "arte y cultura", "patrimonio", "educación y preparación preuniversitaria", "orientación vocacional",
         "empleo y empleabilidad", "emprendimiento", "educación financiera", "tecnología", "idiomas",
         "salud y salud mental", "prevención (drogas y violencia)", "gestión de riesgos y primeros auxilios",
         "participación y voluntariado", "ambiente", "inclusión y discapacidad", "recreación"}
# Cifras que describen la oferta, no la participación.
CIFRAS_DE_OFERTA = ("vacantes", "aforo", "población beneficiaria estimada", "stands", "instituciones expositoras",
                    "árboles plantados")


def validar(df):
    errores = []
    for col, permitidos in VALORES.items():
        malos = set(df[col].dropna()) - permitidos
        if malos:
            errores.append(f"{col}: valores no permitidos {malos}")
    for fila in df.itertuples():
        temas = {t.strip() for t in fila.tematica.split(";")}
        if not temas <= TEMAS:
            errores.append(f"{fila.id}: temas no permitidos {temas - TEMAS}")
        distritos = [d.strip() for d in fila.distrito.split(";")]
        if not set(distritos) <= set(UBIGEO):
            errores.append(f"{fila.id}: distrito desconocido {distritos}")
        elif str(fila.ubigeo) != "; ".join(UBIGEO[d] for d in distritos):
            errores.append(f"{fila.id}: el UBIGEO no coincide con el distrito")
        if fila.evidencia != "oferta" and pd.isna(fila.cifra_texto):
            errores.append(f"{fila.id}: {fila.evidencia} sin cifra_texto")
        if fila.evidencia == "demanda observada" and pd.isna(fila.senal_demanda):
            errores.append(f"{fila.id}: demanda observada sin senal_demanda")
        if fila.evidencia == "participación declarada" and isinstance(fila.cifra_tipo, str) \
                and fila.cifra_tipo.startswith(CIFRAS_DE_OFERTA):
            errores.append(f"{fila.id}: la cifra '{fila.cifra_tipo}' describe la oferta, no la participación")
        if pd.isna(fila.fuente_url) or not str(fila.fuente_url).startswith("http"):
            errores.append(f"{fila.id}: falta el enlace de la fuente")
    if df["id"].duplicated().any():
        errores.append("hay identificadores repetidos")
    return errores


if __name__ == "__main__":
    registro = pd.read_csv(REGISTRO, dtype={"ubigeo": str})
    errores = validar(registro)
    for e in errores:
        print("ERROR:", e)
    print(f"{len(registro)} actividades; {len(errores)} errores")
    print(registro["evidencia"].value_counts().to_string())
    raise SystemExit(1 if errores else 0)
