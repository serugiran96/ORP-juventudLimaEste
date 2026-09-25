"""Construye las tablas de la integración (segunda versión) y valida sus reglas.

Uso (desde la carpeta del proyecto, después de los scripts de estimación integracion_*.py):
    python scripts/integracion_construir.py

Lee:  data/processed/*.csv, fuentes/capa3_registro_oferta.csv, scripts/integracion_contenido.py
Escribe en resultados/:
    evidencias.csv            registro atómico de evidencias (una fila por dato)
    hallazgos_integrados.csv  lectura por capa, con sus evidencias
    patrones.csv              dato observado -> interpretación -> lo que no permite afirmar
    segmentos.csv             a quién aplica cada ficha y qué tamaño tiene (dos bases de población)
    fichas_actividad.csv      una fila por ficha (formato ancho)
    fichas_cadena.csv         la cadena de 10 pasos de cada ficha (formato largo)
    fichas_componentes.csv    componentes respaldados, hipotéticos o descartados
    fichas_convocatoria.csv   registros de convocatoria con su comparabilidad y su código
    cambios_primera_version.csv
Si una regla no se cumple, el script se detiene con un error que dice cuál y dónde.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

import integracion_contenido as C
import integracion_evidencias as IE

RAIZ = Path(__file__).resolve().parent.parent
R = RAIZ / "resultados"
ORDEN_INTERES = ["P0", "P1", "P2", "I1", "I2"]
ORDEN_CONV = ["C0", "C1", "C2", "C3", "C4"]
PASOS = ["Contexto o necesidad", "Población a la que aplica", "Interés o práctica observada", "Alcance potencial",
         "Oferta territorial existente", "Evidencia de participación o convocatoria", "Barreras", "Vacíos de información",
         "Qué podemos afirmar", "Qué solo podemos plantear como hipótesis"]


# --- Formato ----------------------------------------------------------------------------------------------------
def num(x, d=0):
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


def miles(x):
    return f"{num(round(x / 1000))} mil"


class Render:
    def __init__(self, ev, c3):
        self.ev = ev.set_index("id")
        self.c3 = c3.set_index("id")
        self.usadas_e, self.usadas_c3 = set(), set()

    def valor(self, eid):
        e = self.ev.loc[eid]
        if e.precision == "no_publicable":
            raise ValueError(f"{eid} no es publicable (CV > 25 %) y se cita en un texto")
        u = e.unidad
        if u == "%":
            # Ipsos publica enteros: no se agregan decimales que la fuente no tiene.
            s = f"{num(e.valor, 0 if e.precision == 'sin error publicado' else 1)} %"
        elif u == "horas":
            s = f"{num(e.valor, 1)} horas"
        elif u == "personas":
            s = miles(e.valor) if e.valor >= 10000 else num(e.valor)
            if pd.notna(e.ee):
                s += f" (±{miles(1.96 * e.ee)})"
        elif u in ("por 1 000", "por 10 000"):
            s = num(e.valor, 1)
        elif u == "notas":
            s = f"{num(e.valor)} nota{'s' if e.valor != 1 else ''}"
        else:
            s = num(e.valor)
        if e.precision == "referencial":
            s += " (referencial)"
        return s

    def personas(self, eid):
        e = self.ev.loc[eid]
        partes = []
        if pd.notna(e.personas_dj_inf):
            partes.append(f"≈ {num(round(e.personas_dj_inf / 1000))}–{miles(e.personas_dj_sup)} según la población "
                          f"2026 de Dato Joven")
        if pd.notna(e.personas_encuesta):
            lo, hi = e.personas_encuesta - 1.96 * e.personas_encuesta_ee, e.personas_encuesta + 1.96 * e.personas_encuesta_ee
            partes.append(f"{num(round(lo / 1000))}–{miles(hi)} según la expansión de la encuesta")
        if not partes:
            raise ValueError(f"{eid} no tiene cantidad estimada")
        return "; ".join(partes)

    def cifra_c3(self, cid):
        f = self.c3.loc[cid]
        if pd.isna(f.cifra_n):
            raise ValueError(f"{cid} no tiene cifra declarada")
        return num(f.cifra_n)

    def texto(self, t, donde=""):
        if not t:
            return ""
        if re.search(r"\d+(?:[.,]\d+)?\s?%", re.sub(r"\{[^}]+\}", "", t)):
            raise ValueError(f"Porcentaje escrito a mano en {donde}: {t[:80]}")

        def rep(m):
            eid, modo = m.group(1), m.group(2)
            if eid.startswith("C3-"):
                self.usadas_c3.add(eid)
                return self.cifra_c3(eid)
            if eid not in self.ev.index:
                raise ValueError(f"{donde}: evidencia inexistente {eid}")
            self.usadas_e.add(eid)
            if modo == "personas":
                return self.personas(eid)
            if modo == "n":
                return num(self.ev.loc[eid].n_muestral)
            return self.valor(eid)
        return re.sub(r"\{((?:E|C3)-\d{3})(?::(\w+))?\}", rep, t)


def ids(celda):
    return [x.strip() for x in str(celda or "").split(";") if x.strip()]


def placeholders(t):
    return set(re.findall(r"\{(E-\d{3})", t or "")), set(re.findall(r"\{(C3-\d{3})\}", t or ""))


# --- Reglas -----------------------------------------------------------------------------------------------------
def codigo_convocatoria(reg, c3):
    """Regla reproducible: el código depende del tipo de evidencia de la Capa 3 y de la comparabilidad."""
    f = c3.loc[reg["c3"]]
    comparable = reg["segmento"] != "no" and reg["territorio"] != "no"
    if not comparable:
        return "no comparable", False
    if f.evidencia == "demanda observada":
        return "C4", True
    if f.evidencia == "participación declarada":
        if pd.notna(f.cifra_n) and reg["segmento"] == "sí" and reg["territorio"] == "sí":
            return "C3", True
        return "C2", True
    return "C1", True


def construir():
    ev = IE.construir()
    c3 = pd.read_csv(RAIZ / "fuentes" / "capa3_registro_oferta.csv")
    rd = Render(ev, c3)
    c3i = c3.set_index("id")

    def check_c3(lista, donde):
        for x in lista:
            if x not in c3i.index:
                raise ValueError(f"{donde}: actividad inexistente {x}")

    # Hallazgos
    filas_h = []
    for h in C.HALLAZGOS:
        texto = rd.texto(h["enunciado"], h["id"])
        e_ids = ids(h.get("evidencias")) or []
        pe, pc = placeholders(h["enunciado"])
        if not pe <= set(e_ids):
            raise ValueError(f"{h['id']}: el texto cita {sorted(pe - set(e_ids))} sin declararlas en 'evidencias'")
        c3_ids = sorted(set(ids(h.get("c3"))) | pc)
        check_c3(c3_ids, h["id"])
        sub = ev[ev.id.isin(e_ids)]
        precisiones = set(sub.precision)
        precision = ("incluye valores referenciales" if "referencial" in precisiones else
                     "confiable" if precisiones & {"confiable"} else ", ".join(sorted(precisiones)) or
                     "cifras declaradas por quien organiza")
        filas_h.append({
            "id": h["id"], "capa": h["capa"], "dimension": h["dimension"], "enunciado": texto,
            "tipo_evidencia": "; ".join(sorted(set(sub.naturaleza))) or "oferta y convocatoria publicadas (Capa 3)",
            "geografia": "; ".join(sorted(set(sub.ambito))) or "7 distritos (lo publicado)",
            "periodo": "; ".join(sorted(set(sub.periodo.astype(str)))) or "2024-2026",
            "precision": precision, "no_permite": h["no_permite"], "evidencias": "; ".join(e_ids),
            "actividades_c3": "; ".join(c3_ids), "estado_v2": h["estado"], "cambio_v2": h.get("cambio", "")})
    hall = pd.DataFrame(filas_h)

    # Patrones
    filas_p = []
    for p in C.PATRONES:
        pe, _ = placeholders(p["dato"])
        if not pe <= set(ids(p["evidencias"])):
            raise ValueError(f"{p['id']}: evidencias no declaradas {sorted(pe - set(ids(p['evidencias'])))}")
        for hid in ids(p["hallazgos"]):
            if hid not in set(hall.id):
                raise ValueError(f"{p['id']}: hallazgo inexistente {hid}")
        filas_p.append({"id": p["id"], "tipo": p["tipo"], "tema": p["tema"],
                        "dato_observado": rd.texto(p["dato"], p["id"]),
                        "interpretacion": rd.texto(p["interpretacion"], p["id"]),
                        "no_permite_afirmar": rd.texto(p["no_permite"], p["id"]), "hallazgos": p["hallazgos"],
                        "evidencias": p["evidencias"]})
    pat = pd.DataFrame(filas_p)

    # Segmentos
    evi = ev.set_index("id")
    filas_s = []
    for s in C.SEGMENTOS:
        e = evi.loc[s["evidencia"]]
        filas_s.append({
            "id": s["id"], "segmento": s["nombre"], "evidencia": s["evidencia"], "indicador": e.indicador,
            "poblacion_de_referencia": e.poblacion, "ambito": e.ambito, "periodo": e.periodo,
            "porcentaje": round(e.valor, 1), "ic95_inf": round(e.ic95_inf, 1), "ic95_sup": round(e.ic95_sup, 1),
            "precision": e.precision, "n_muestral": e.n_muestral,
            "personas_base_dato_joven_inf": round(e.personas_dj_inf, -3) if pd.notna(e.personas_dj_inf) else np.nan,
            "personas_base_dato_joven_sup": round(e.personas_dj_sup, -3) if pd.notna(e.personas_dj_sup) else np.nan,
            "personas_encuesta": round(e.personas_encuesta, -3) if pd.notna(e.personas_encuesta) else np.nan,
            "personas_encuesta_ic95": round(1.96 * e.personas_encuesta_ee, -3) if pd.notna(
                e.personas_encuesta_ee) else np.nan,
            "texto": f"{rd.valor(s['evidencia'])} de {e.poblacion} ({rd.personas(s['evidencia'])})",
            "fichas": s["fichas"], "fuente": e.fuente})
    seg = pd.DataFrame(filas_s)

    # Fichas
    filas_f, cadena, comp, convs = [], [], [], []
    for f in C.FICHAS:
        fid = f["id"]
        todas_e, todas_c3 = set(), set(ids(f["oferta"]["c3"]))
        nec = []
        for n in f["necesidad"]:
            pe, pc = placeholders(n["texto"])
            if not pe <= set(ids(n["evidencias"])):
                raise ValueError(f"{fid} necesidad: evidencias no declaradas {sorted(pe - set(ids(n['evidencias'])))}")
            todas_e |= set(ids(n["evidencias"]))
            nec.append((n["tipo"], rd.texto(n["texto"], fid)))
        intereses = []
        for i in f["interes"]:
            if i["codigo"] not in ORDEN_INTERES:
                raise ValueError(f"{fid}: código de interés inválido {i['codigo']}")
            pe, _ = placeholders(i["texto"])
            if not pe <= set(ids(i["evidencias"])):
                raise ValueError(f"{fid} interés: evidencias no declaradas")
            if i["codigo"] != "P0" and not ids(i["evidencias"]):
                raise ValueError(f"{fid}: un interés {i['codigo']} necesita al menos una evidencia")
            todas_e |= set(ids(i["evidencias"]))
            intereses.append((i["codigo"], rd.texto(i["texto"], fid)))
        cod_interes = max((c for c, _ in intereses), key=ORDEN_INTERES.index)

        # Convocatoria
        regs = []
        for reg in f["convocatoria"]:
            check_c3([reg["c3"]], fid)
            codigo, comparable = codigo_convocatoria(reg, c3i)
            a = c3i.loc[reg["c3"]]
            nota = rd.texto(reg["nota"], fid)
            regs.append((codigo, comparable, reg, nota))
            todas_c3.add(reg["c3"])
            convs.append({"ficha": fid, "actividad_c3": reg["c3"], "nombre": a.nombre, "distrito": a.distrito,
                          "publico": a.incluye_15_29, "evidencia_c3": a.evidencia, "cifra_declarada": a.cifra_n,
                          "cifra_tipo": a.cifra_tipo, "comparable_segmento": reg["segmento"],
                          "comparable_territorio": reg["territorio"], "comparable_formato": reg["formato"],
                          "comparable_costo": reg["costo"], "codigo": codigo, "nota": nota})
        detalle_conv = ""
        if f["tipo"] in ("protocolo transversal", "población que requiere consulta directa"):
            cod_conv = "no aplica"
        else:
            cods = [c for c, ok, _, _ in regs if ok]
            cod_conv = max(cods, key=ORDEN_CONV.index) if cods else "C0"
            # Detalle del registro que define el código: con qué comparabilidad y qué tipo de señal es.
            mejores = [r for c, ok, r, _ in regs if ok and c == cod_conv]
            if mejores:
                dims = {"segmento": "segmento", "territorio": "territorio", "formato": "formato", "costo": "costo"}
                r0 = min(mejores, key=lambda r: sum(r[k] != "sí" for k in dims))
                parciales = [v for k, v in dims.items() if r0[k] != "sí"]
                detalle_conv = (f"{cod_conv} por {r0['c3']}: comparable en "
                                + ("todas las dimensiones" if not parciales else
                                   "parte; no plenamente en " + ", ".join(parciales)))
                if cod_conv == "C4":
                    detalle_conv += ". Es demanda por esa oferta concreta, no interés general (C3-D9)"
                elif cod_conv == "C3":
                    detalle_conv += ". Cifra declarada por quien organiza, sin cupos publicados"
        texto_conv = " ".join(f"[{c}] {n}" for c, _, _, n in regs) or (
            "No se encontró ninguna actividad comparable con datos (sin evidencia, no evidencia negativa)."
            if cod_conv == "C0" else "No aplica.")

        # Alcance
        al = f["alcance"]
        if al["tipo"] == "desconocido":
            texto_alc = "Alcance potencial no estimable con la evidencia disponible."
        else:
            partes = []
            for eid in ids(al["evidencias"]):
                e = evi.loc[eid]
                p = (f"{e.indicador}: {rd.valor(eid)} de {e.poblacion}" if e.unidad == "%" else
                     f"{e.indicador}: {rd.valor(eid)} ({e.periodo})")
                if pd.notna(e.personas_dj_inf) or pd.notna(e.personas_encuesta):
                    p += f" ({rd.personas(eid)})"
                rd.usadas_e.add(eid)
                partes.append(p)
            texto_alc = ". ".join(partes) + "."
            todas_e |= set(ids(al["evidencias"]))

        barreras = []
        for b in f["barreras"]:
            pe, _ = placeholders(b["texto"])
            if not pe <= set(ids(b["evidencias"])):
                raise ValueError(f"{fid} barrera: evidencias no declaradas {sorted(pe - set(ids(b['evidencias'])))}")
            todas_e |= set(ids(b["evidencias"]))
            barreras.append(f"[{b['pertinencia']}] {rd.texto(b['texto'], fid)}")
        afirm = []
        for a_ in f["afirmaciones"]:
            pe, pc = placeholders(a_["texto"])
            declaradas = set(ids(a_.get("evidencias")))
            if not pe <= declaradas:
                raise ValueError(f"{fid} afirmación: evidencias no declaradas {sorted(pe - declaradas)}")
            if not declaradas and not ids(a_.get("c3")) and not pc:
                raise ValueError(f"{fid}: una afirmación sin evidencia")
            for eid in declaradas:
                if evi.loc[eid].tipo_dato not in ("dato observado", "cálculo derivado"):
                    raise ValueError(f"{fid}: una afirmación cita algo que no es un dato")
            todas_e |= declaradas
            todas_c3 |= set(ids(a_.get("c3"))) | pc
            afirm.append(rd.texto(a_["texto"], fid))
        if f["tipo"] not in ("protocolo transversal", "población que requiere consulta directa") and not f["hipotesis"]:
            raise ValueError(f"{fid}: una actividad de convocatoria necesita hipótesis explícitas")
        if not f["vacios"]:
            raise ValueError(f"{fid}: faltan vacíos de información")
        vacios = [rd.texto(v, fid) for v in f["vacios"]]
        hipot = [rd.texto(h, fid) for h in f["hipotesis"]]
        poblacion = rd.texto(f["poblacion"], fid)
        todas_e |= placeholders(f["poblacion"])[0]
        oferta = rd.texto(f["oferta"]["texto"], fid)
        check_c3(sorted(todas_c3), fid)

        pasos = [
            (" · ".join(t for t, _ in nec), " ".join(x for _, x in nec)),
            ("", poblacion),
            (cod_interes, " ".join(f"[{c}] {x}" for c, x in intereses) + (f" Salto inferencial: {f['salto']}"
                                                                           if f["salto"] else "")),
            (al["tipo"], texto_alc),
            ("", oferta),
            (cod_conv, (detalle_conv + ". " if detalle_conv else "") + texto_conv),
            ("", " ".join(barreras) or "No hay datos de barreras específicas."),
            ("", " ".join(f"• {v}" for v in vacios)),
            ("", " ".join(f"• {a}" for a in afirm)),
            ("", " ".join(f"• {h}" for h in hipot) or "No aplica."),
        ]
        for k, (paso, (codigo, texto)) in enumerate(zip(PASOS, pasos), start=1):
            cadena.append({"ficha": fid, "orden": k, "paso": paso, "codigo": codigo, "texto": texto})
        for nombre, estado, nota in f["componentes"]:
            comp.append({"ficha": fid, "componente": nombre, "estado": estado, "nota": rd.texto(nota, fid)})
        filas_f.append({
            "id": fid, "linea": f["linea"], "actividad": f["actividad"], "tipo_ficha": f["tipo"],
            "origen_v1": f["origen"], "resultado_auditoria": f["resultado"], "segmentos": f["segmentos"],
            "necesidad_tipo": "; ".join(t for t, _ in nec), "necesidad": pasos[0][1], "poblacion": poblacion,
            "interes_codigo": cod_interes, "interes": pasos[2][1], "salto_inferencial": f["salto"],
            "alcance_tipo": al["tipo"], "alcance": texto_alc, "oferta": oferta, "convocatoria_codigo": cod_conv,
            "convocatoria_detalle_codigo": detalle_conv,
            "convocatoria": texto_conv, "barreras": pasos[6][1], "vacios": pasos[7][1], "afirmaciones": pasos[8][1],
            "hipotesis": pasos[9][1], "validacion_piloto": f["validacion"], "donde": rd.texto(f["donde"], fid),
            "cambio_v1": f["cambio"], "evidencias": "; ".join(sorted(todas_e)),
            "actividades_c3": "; ".join(sorted(todas_c3))})
    fichas = pd.DataFrame(filas_f)
    if list(fichas.id) != sorted(fichas.id):
        raise ValueError("Las fichas deben conservar su orden por línea temática e ID, no por evidencia")

    cambios = pd.DataFrame(C.CAMBIOS)

    # Evidencias: marcar cuáles se citan
    ev["citada_en"] = ev.id.map(lambda i: "sí" if i in rd.usadas_e else "")
    return dict(evidencias=ev, hallazgos_integrados=hall, patrones=pat, segmentos=seg, fichas_actividad=fichas,
                fichas_cadena=pd.DataFrame(cadena), fichas_componentes=pd.DataFrame(comp),
                fichas_convocatoria=pd.DataFrame(convs), cambios_primera_version=cambios)


def main():
    tablas = construir()
    for nombre, df in tablas.items():
        df.to_csv(R / f"{nombre}.csv", index=False)
        print(f"  {nombre}.csv: {len(df)} filas")
    viejo = R / "propuestas.csv"
    if viejo.exists():
        viejo.unlink()
        print("  propuestas.csv: reemplazado por fichas_actividad.csv (ver cambios_primera_version.csv)")
    f = tablas["fichas_actividad"]
    print("\nFichas:")
    print(f[["id", "actividad", "tipo_ficha", "necesidad_tipo", "interes_codigo", "alcance_tipo",
             "convocatoria_codigo"]].to_string(index=False))


if __name__ == "__main__":
    main()
