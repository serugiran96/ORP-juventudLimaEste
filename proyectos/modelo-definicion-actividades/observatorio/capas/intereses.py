"""Capa 2 · Intereses: uso del tiempo, horarios disponibles, cultura y ocio, vida digital y aspiraciones."""

import pandas as pd

from .comun import FUENTES, SEXOS, buscar, estimacion, leer, limpio

GEOS = {"lima_este": "le", "lima_metropolitana": "lm"}

# ENUT 2024: actividades de la semana (se omiten las que hace casi todo el mundo: dormir, comer, asearse, convivir).
ACTIVIDADES = [
    ("Usar computadora, tablet o celular (internet, redes, juegos)", "Usar celular o computadora"),
    ("Ver televisión o videos", "Ver televisión o videos"),
    ("Trabajo doméstico no remunerado", "Tareas del hogar"),
    ("Trabajo remunerado y búsqueda de trabajo", "Trabajar o buscar trabajo"),
    ("Estudio", "Estudiar"),
    ("Cuidado de otras personas del hogar", "Cuidar a otras personas"),
    ("Deporte y ejercicio físico", "Deporte o ejercicio"),
    ("Escuchar radio o audio", "Escuchar radio o audio"),
    ("Aficiones, artes y juegos", "Aficiones, artes y juegos"),
    ("Asistir a eventos culturales, de entretenimiento o deportivos", "Ir a eventos culturales o deportivos"),
    ("Leer", "Leer"),
    ("Voluntariado y ayuda a la comunidad u otros hogares", "Voluntariado o ayuda a la comunidad"),
]
HORAS = [("Trabajo remunerado y búsqueda de trabajo", "Trabajar o buscar trabajo"), ("Estudio", "Estudiar"),
         ("Trabajo doméstico no remunerado", "Tareas del hogar"), ("Cuidado de otras personas del hogar", "Cuidar a otras personas")]
SATISFACCION = [("Cantidad de tiempo libre", "Cantidad de tiempo libre"), ("Calidad del tiempo libre", "Calidad del tiempo libre"),
                ("Tiempo dedicado a pasatiempos", "Tiempo para sus pasatiempos"), ("Tiempo dedicado a sus amistades", "Tiempo con sus amistades")]
BLOQUES = [("Lunes a viernes", "14:00-18:00"), ("Lunes a viernes", "18:00-22:00"), ("Sábado", "09:00-13:00"),
           ("Sábado", "14:00-18:00"), ("Sábado", "18:00-22:00"), ("Domingo", "09:00-13:00"), ("Domingo", "14:00-18:00")]
CULTURA = [
    ("Cine", "Cine"), ("Espectáculo musical (conciertos, festivales)", "Conciertos o festivales musicales"),
    ("Feria artesanal", "Feria artesanal"), ("Festival local o tradicional (fiestas patronales, carnavales)", "Festival local o tradicional"),
    ("Feria del libro", "Feria del libro"), ("Danza", "Danza"), ("Biblioteca o sala de lectura", "Biblioteca"),
    ("Teatro", "Teatro"), ("Circo", "Circo"), ("Exposición de fotografía, pintura o arte", "Exposición de arte"),
]
MOTIVOS = [("Falta de interés", "Falta de interés"), ("Falta de tiempo", "Falta de tiempo"), ("Falta de dinero", "Falta de dinero"),
           ("No tiene información oportuna", "No se enteró a tiempo"), ("No hay ofertas", "No hay oferta cerca")]
ENTRADA = [("Entrada libre", "Gratis"), ("Comprada", "La compró"), ("Pagada por otra persona", "Se la pagaron")]
PATRIMONIO = [("Museo", "Museo"), ("Monumento histórico", "Monumento histórico"), ("Sitio arqueológico", "Sitio arqueológico")]
PROPOSITOS = [("Comunicarse (correo, chat, redes)", "Comunicarse (chat, redes)"), ("Entretenimiento", "Entretenimiento"),
              ("Obtener información", "Buscar información"), ("Banca electrónica", "Banca por internet"),
              ("Educación formal y capacitación", "Estudiar o capacitarse"), ("Comprar productos o servicios", "Comprar"),
              ("Descargar aplicaciones o software", "Descargar aplicaciones"), ("Trámites con el Estado", "Trámites con el Estado"),
              ("Vender productos o servicios", "Vender")]
BIENES = [("Música por internet", "Música por internet"), ("Películas o video por internet", "Películas o videos por internet"),
          ("Libros impresos", "Libros impresos"), ("Libros digitales", "Libros digitales"),
          ("Videojuegos multijugador en línea", "Videojuegos en línea"), ("Videojuegos en dispositivos móviles", "Videojuegos en el celular"),
          ("Periódicos digitales", "Periódicos digitales")]


def _tiempo():
    u = leer("capa2_uso_tiempo_enut.csv")
    u = u[u.grupo_edad == "15-29"]
    part = {}
    for geo, g in GEOS.items():
        part[g] = {}
        for s in SEXOS:
            sub = u[(u.nivel_geografico == geo) & (u.sexo == s) & (u.familia == "participacion_semanal")]
            part[g][s] = [{"t": n, **(estimacion(buscar(sub, categoria=c)) or {"v": None, "p": "n"})} for c, n in ACTIVIDADES]
    horas = {}
    for geo, g in GEOS.items():
        horas[g] = {}
        for s in SEXOS:
            sub = u[(u.nivel_geografico == geo) & (u.sexo == s) & (u.familia == "horas_semanales_promedio")]
            horas[g][s] = [{"t": n, **_horas(buscar(sub, categoria=c))} for c, n in HORAS]
    sat = {}
    for geo, g in GEOS.items():
        sub = u[(u.nivel_geografico == geo) & (u.sexo == "total") & (u.familia == "satisfaccion_muy_o_totalmente_satisfecho")]
        sat[g] = [{"t": n, **(estimacion(buscar(sub, categoria=c)) or {"v": None, "p": "n"})} for c, n in SATISFACCION]
    return {"participacion": part, "horas": horas, "satisfaccion": sat}


def _horas(f):
    """Horas semanales promedio (sin IC en porcentaje: se envía el valor y su precisión)."""
    if f is None or f["precision"] == "no_publicable":
        return {"v": None, "p": "n"}
    return {"v": round(float(f["valor"]), 1), "lo": round(max(f["valor"] - 1.96 * f["ee"], 0), 1),
            "hi": round(f["valor"] + 1.96 * f["ee"], 1), "cv": round(float(f["cv"]), 1),
            "p": "c" if f["precision"] == "confiable" else "r", "n": int(f["n_muestral"])}


def _horarios():
    t = leer("integracion_tiempo_enut.csv")
    d = t[(t.indicador == "disponible_en_bloque") & (t.grupo_edad == "15-29")]
    out = {"bloques": [{"dia": a, "franja": b} for a, b in BLOQUES]}
    for geo, g in GEOS.items():
        out[g] = {}
        for s in SEXOS:
            for grupo in ["todos", "trabajó o estudió en la semana", "no trabajó ni estudió en la semana"]:
                sub = d[(d.nivel_geografico == geo) & (d.sexo == s) & (d.grupo == grupo)]
                if sub.empty:
                    continue
                out[g][f"{s}|{grupo}"] = [estimacion(buscar(sub, categoria=f"{a}, {b}")) for a, b in BLOQUES]
    libres = t[(t.indicador == "horas_no_comprometidas") & (t.grupo_edad == "15-29") & (t.grupo == "todos")]
    out["horas_libres"] = {g: {s: [{"t": c, **_horas(buscar(libres[(libres.nivel_geografico == geo) & (libres.sexo == s)], categoria=c))}
                                   for c in ["Un día de lunes a viernes", "Sábado", "Domingo"]]
                               for s in SEXOS if not libres[(libres.nivel_geografico == geo) & (libres.sexo == s)].empty}
                           for geo, g in GEOS.items()}
    return out


def _cultura():
    c = leer("capa2_cultura_enapres.csv")
    c = c[(c.periodo == "2022-2025") & (c.grupo_edad == "15-29")]
    ce = leer("integracion_cultura_edad_enapres.csv")
    asis = {}
    for geo, g in GEOS.items():
        asis[g] = {}
        for s in SEXOS:
            sub = c[(c.nivel_geografico == geo) & (c.sexo == s) & (c.familia == "asistencia")]
            asis[g][s] = [{"t": n, **(estimacion(buscar(sub, item=i)) or {"v": None, "p": "n"})} for i, n in CULTURA]
        for e in ["15-19", "20-24", "25-29"]:
            sub = ce[(ce.nivel_geografico == geo) & (ce.grupo_edad == e) & (ce.familia == "asistencia")]
            asis[g][e] = [{"t": n, **(estimacion(buscar(sub, item=i)) or {"v": None, "p": "n"})} for i, n in CULTURA]
    le = c[(c.nivel_geografico == "lima_este") & (c.sexo == "total")]
    motivos = {n: [{"t": mn, **(estimacion(buscar(le[(le.familia == "motivo_no_asistencia")], item=i, categoria=m)) or {"v": None, "p": "n"})}
                   for m, mn in MOTIVOS] for i, n in CULTURA}
    entrada = {n: [{"t": en, **(estimacion(buscar(le[(le.familia == "forma_de_entrada")], item=i, categoria=m)) or {"v": None, "p": "n"})}
                   for m, en in ENTRADA] for i, n in CULTURA}
    patrimonio = {g: [{"t": n, **(estimacion(buscar(c[(c.nivel_geografico == geo) & (c.sexo == "total") & (c.familia == "patrimonio")], item=i)) or {"v": None, "p": "n"})}
                      for i, n in PATRIMONIO] for geo, g in GEOS.items()}
    resumen = {g: {k: estimacion(buscar(c[(c.nivel_geografico == geo) & (c.sexo == "total") & (c.familia == "asistencia")], item=i))
                   for k, i in [("alguno", "Algún servicio cultural (cualquiera de los 11)"),
                                ("en_vivo", "Algún espectáculo o exposición en vivo (teatro, danza, circo, música, arte)")]}
               for geo, g in GEOS.items()}
    return {"asistencia": asis, "motivos": motivos, "entrada": entrada, "patrimonio": patrimonio, "resumen": resumen}


def _digital():
    i = leer("capa2_educacion_internet_enaho.csv")
    i = i[(i.periodo == "2022-2025") & (i.grupo_edad == "15-29")]
    out = {}
    for geo, g in GEOS.items():
        out[g] = {}
        for s in SEXOS:
            sub = i[(i.nivel_geografico == geo) & (i.sexo == s)]
            out[g][s] = {"usa": estimacion(buscar(sub, familia="internet", categoria="Usó internet el mes anterior")),
                         "diario": estimacion(buscar(sub, familia="internet", categoria="Usa internet al menos una vez al día (entre usuarios)")),
                         "propositos": [{"t": n, **(estimacion(buscar(sub, familia="proposito_internet", categoria=c)) or {"v": None, "p": "n"})}
                                        for c, n in PROPOSITOS]}
    c = leer("capa2_cultura_enapres.csv")
    c = c[(c.periodo == "2022-2025") & (c.grupo_edad == "15-29") & (c.familia == "bienes_culturales") & (c.sexo == "total")]
    out["bienes"] = {g: [{"t": n, **(estimacion(buscar(c[c.nivel_geografico == geo], item=it)) or {"v": None, "p": "n"})} for it, n in BIENES]
                     for geo, g in GEOS.items()}
    return out


def _aspiraciones():
    ip = pd.read_csv(FUENTES / "capa2_estudios_ipsos.csv")
    estudios = []
    for (fid, estudio), sub in ip.groupby(["id_fuente", "estudio"], sort=False):
        f = sub.iloc[0]
        estudios.append({"id": fid, "estudio": estudio, "campo": limpio(f.trabajo_de_campo), "poblacion": limpio(f.poblacion),
                         "cobertura": limpio(f.cobertura), "muestra": limpio(str(f.muestra)), "metodo": limpio(f.metodo),
                         "temas": [{"tema": t, "items": [{"n": r.indicador, "v": limpio(r.valor_pct), "base": limpio(r.base),
                                                          "nota": limpio(r.nota)} for r in s2.itertuples()]}
                                   for t, s2 in sub.groupby("tema", sort=False)]})
    return estudios


def construir():
    return {"tiempo": _tiempo(), "horarios": _horarios(), "cultura": _cultura(), "digital": _digital(),
            "aspiraciones": _aspiraciones()}
