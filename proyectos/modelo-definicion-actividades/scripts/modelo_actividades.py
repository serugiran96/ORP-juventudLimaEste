"""Modelo de convocatoria por público: cuántos jóvenes de Lima Este podría convocar cada actividad o servicio (versión 3).

Uso (desde la carpeta del proyecto):
    python scripts/modelo_actividades.py
    # -> resultados/modelo_actividades.csv      (un resultado por tipo de actividad o servicio)
    #    resultados/modelo_publicos.csv         (el embudo de cada tipo en cada público)
    #    resultados/modelo_perfil_publicos.csv  (población, tiempo libre, seguridad, situación y distritos de cada público)
    #    resultados/modelo_criterios.csv        (los pasos del embudo, para la página)

Para cada tipo (fuentes/modelo_tipos_actividad.csv) y cada público (mujeres y hombres de 15-19, 20-24 y 25-29 años):

    jóvenes convocables = población × % que la hace o la haría × % con tiempo libre en el mejor horario

- Población: Dato Joven 2026, siete distritos de Lima Este.
- La hace o la haría:
    ya la hace  % que la hizo (ENAPRES: últimos 12 meses; ENUT: última semana; ENAHO: situación actual).
    frenados    % que no la hizo por falta de dinero, de información o de oferta (ENAPRES); que no estudia por motivo
                económico (ENAHO, hasta 24 años); que quiere trabajar pero no busca (ENAHO). Son barreras que una
                actividad gratuita, cercana y bien difundida quita.
  Si la pregunta mide una práctica relacionada y no la misma actividad (por ejemplo, ver danza frente a practicarla),
  ambos cuentan la mitad. Las medidas semanales (ENUT) no se reducen: una semana ya es una ventana más corta que un año.
- Tiempo libre: % con dos horas libres seguidas en cada bloque de la semana (ENUT 2024). En los bloques de noche se
  descuenta a quienes evitan salir de noche por inseguridad (ENAPRES). Se usa el mejor bloque de cada público.

Estimación por público: la ENAPRES de Lima Este se combina por edad y por sexo (supone que la diferencia entre mujeres y
hombres es parecida en cada edad); la ENUT de Lima Este usa el patrón por sexo y edad de Lima Metropolitana.

Las actividades y los servicios se ordenan por separado: los servicios se dirigen a jóvenes con una necesidad
específica y no se comparan con actividades abiertas a todos. Los tipos que ninguna encuesta mide no se ordenan.
El registro de oferta no cambia el número: solo indica si algo parecido ya convocó en Lima Este (la mayoría de las
actividades que convocan no está registrada). No predice asistencia ni permanencia: eso se valida en pilotos.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
PROC = RAIZ / "data" / "processed"

SEXOS = ["mujer", "hombre"]
EDADES = ["15-19", "20-24", "25-29"]
PUBLICOS = [(s, e) for s in SEXOS for e in EDADES]
BLOQUES = ["Lunes a viernes, 14:00-18:00", "Lunes a viernes, 18:00-22:00", "Sábado, 09:00-13:00", "Sábado, 14:00-18:00",
           "Sábado, 18:00-22:00", "Domingo, 09:00-13:00", "Domingo, 14:00-18:00"]
FRENOS = {"Falta de dinero": "dinero", "No tiene información oportuna": "informacion", "No hay ofertas": "oferta"}
SITUACION = ["solo_estudia", "estudia_y_trabaja", "solo_trabaja", "ni_estudia_ni_trabaja", "hogar"]
N_SIM, SEMILLA = 4000, 2026

PASOS = [
    ("poblacion", "Población", "¿Cuántos jóvenes hay en cada público?",
     "Jóvenes que viven en los siete distritos de Lima Este en 2026, por sexo y edad.",
     "Dato Joven 2026 (proyección del Minsa e INEI)", "147 841 mujeres de 25 a 29 años"),
    ("demanda", "La hace o la haría", "¿Qué parte ya la hace o la haría si se quitan las barreras que ustedes pueden quitar?",
     "Ya la hacen: % que la hizo. Frenados: % que no la hizo por falta de dinero, de información o de oferta. "
     "Ustedes quitan esas tres barreras con una actividad gratuita, cercana y bien difundida.",
     "ENAPRES 2022-2025, ENUT 2024 y ENAHO 2022-2025 (INEI)", "51,6 % de ellas va a conciertos o no va solo por esas barreras"),
    ("tiempo", "Tiempo libre", "¿Qué parte tiene tiempo libre en el mejor horario de la semana?",
     "% que tiene dos horas libres seguidas en ese horario. Si es de noche, se descuenta a quienes evitan salir por "
     "inseguridad.", "ENUT 2024 y ENAPRES 2022-2025 (INEI)", "37,1 % de ellas tiene libre el domingo de 14:00 a 18:00"),
    ("convocables", "Jóvenes convocables", "¿Cuántos jóvenes podría convocar?",
     "Población × % que la hace o la haría × % con tiempo libre. No es la asistencia esperada: es el público con interés "
     "y tiempo, y sirve para comparar.", "Cálculo del observatorio", "147 841 × 51,6 % × 37,1 % ≈ 28 300 mujeres"),
]


def lista(x):
    return [] if pd.isna(x) or x == "" else [p.strip() for p in str(x).split(";") if p.strip()]


def codigo_convocatoria(ofertas):
    """Regla automática para los tipos sin ficha (misma lógica que la integración, sin la revisión caso a caso)."""
    # Las actividades solo para niños y adolescentes no cuentan como convocatoria de jóvenes (regla de la integración).
    ofertas = ofertas[ofertas.incluye_15_29.isin(["juventud", "todo público", "no indica"])]
    if ofertas.empty:
        return "C0", "sin registros para jóvenes"
    jov = ofertas.incluye_15_29.isin(["juventud", "todo público"])
    dem = ofertas[(ofertas.evidencia == "demanda observada") & jov]
    if len(dem):
        return "C4", f"más interesados que cupos en {', '.join(dem.index)}"
    c3 = ofertas[(ofertas.evidencia == "participación declarada") & ofertas.cifra_n.notna() & (ofertas.incluye_15_29 == "juventud")]
    if len(c3):
        return "C3", f"participación declarada de jóvenes en {', '.join(c3.index)}"
    c2 = ofertas[ofertas.evidencia == "participación declarada"]
    if len(c2):
        return "C2", f"participación declarada sin cifra o de otro público en {', '.join(c2.index)}"
    return "C1", "solo anuncios de oferta"


class Datos:
    """Tablas procesadas de las encuestas, ya filtradas a Lima Este (o a Lima Metropolitana para los patrones)."""

    def __init__(self):
        le = lambda d: d[d.nivel_geografico == "lima_este"]
        self.cul_edad = le(pd.read_csv(PROC / "integracion_cultura_edad_enapres.csv"))
        c = le(pd.read_csv(PROC / "capa2_cultura_enapres.csv"))
        self.cul = c[(c.periodo == "2022-2025") & (c.grupo_edad == "15-29")]
        e = pd.read_csv(PROC / "capa2_uso_tiempo_enut.csv")
        self.enut = e[(e.nivel_geografico == "lima_este") & (e.sexo == "total") & (e.grupo_edad == "15-29")
                      & (e.familia == "participacion_semanal")].set_index("categoria")
        t = pd.read_csv(PROC / "integracion_tiempo_enut.csv")
        t = t[t.grupo == "todos"]
        self.tiempo_lm = t[t.nivel_geografico == "lima_metropolitana"]
        self.bloques_le = t[(t.nivel_geografico == "lima_este") & (t.indicador == "disponible_en_bloque")].set_index("categoria")
        s = pd.read_csv(PROC / "integracion_enaho_segmentos.csv")
        self.enaho_le = s[(s.nivel_geografico == "lima_este") & (s.periodo == "2022-2025")]
        self.seguridad = le(pd.read_csv(PROC / "integracion_seguridad_enapres.csv"))
        p = pd.read_csv(PROC / "capa1_poblacion_joven_distritos.csv")
        p = p[(p.anio == 2026) & (p.lima_este == True) & (p.nivel_geografico == "distrito")].copy()
        p["edad"] = p.grupo_edad.str.replace(" a ", "-")
        self.pob_dist = p

    # ------------------------------------------------------------ ENAPRES
    def cultura(self, familia, item, categoria="Sí", **filtro):
        df = self.cul_edad if "grupo_edad" in filtro else self.cul
        q = df[(df.familia == familia) & (df.item == item) & (df.categoria == categoria)]
        for k, v in filtro.items():
            q = q[q[k] == v]
        r = q.iloc[0]
        return float(r.valor), float(r.ee)

    def frenados_cultura(self, item, **filtro):
        """% de jóvenes que no asistió por dinero, información o falta de oferta (sobre todos los jóvenes)."""
        a, ea = self.cultura("asistencia", item, **filtro)
        mot = {k: self.cultura("motivo_no_asistencia", item, k, **filtro) for k in FRENOS}
        suma = sum(v for v, _ in mot.values())
        valor = (100 - a) * suma / 100
        ee = (((100 - a) / 100) ** 2 * sum(e ** 2 for _, e in mot.values()) + (suma / 100) ** 2 * ea ** 2) ** 0.5
        partes = {FRENOS[k]: (100 - a) * v / 100 for k, (v, _) in mot.items()}
        return valor, ee, partes

    # ------------------------------------------------------------ ENUT y seguridad (patrones de Lima Metropolitana)
    def patron_lm(self, indicador, categoria, sexo, edad):
        t = self.tiempo_lm
        g = lambda sx, ed: float(t[(t.indicador == indicador) & (t.categoria == categoria) & (t.sexo == sx)
                                   & (t.grupo_edad == ed)].valor.iloc[0])
        tot = g("total", "15-29")
        return (g(sexo, "15-29") / tot) * (g("total", edad) / tot)

    def seguridad_publico(self, indicador, sexo, edad):
        s = self.seguridad[self.seguridad.indicador == indicador]
        g = lambda sx, ed: float(s[(s.sexo == sx) & (s.grupo_edad == ed)].valor.iloc[0])
        return g("total", edad) * g(sexo, "15-29") / g("total", "15-29")

    # ------------------------------------------------------------ ENAHO
    def enaho(self, indicador, sexo, edad):
        q = self.enaho_le[(self.enaho_le.indicador == indicador) & (self.enaho_le.sexo == sexo) & (self.enaho_le.grupo_edad == edad)]
        return (float(q.valor.iloc[0]), float(q.ee.iloc[0])) if len(q) else (np.nan, np.nan)

    # ------------------------------------------------------------ tiempo libre de cada público
    def tiempo_libre(self, sexo, edad):
        evita = self.seguridad_publico("evito_salir_noche", sexo, edad)
        res = {}
        for b in BLOQUES:
            d = float(self.bloques_le.loc[b, "valor"]) * self.patron_lm("disponible_en_bloque", b, sexo, edad)
            if "18:00-22:00" in b:
                d *= 1 - evita / 100
            res[b] = min(d, 100.0)
        return res, evita


def factor(t):
    """Una práctica relacionada medida en el año cuenta la mitad; la semanal (ENUT) no se reduce."""
    return 0.5 if t.participacion_relacion == "relacionada" and t.participacion_fuente != "enut_semana" else 1.0


def demanda(D, t, sexo, edad):
    """(ya la hace, ee, frenados, ee) en % del público, con el factor de práctica relacionada aplicado."""
    f = factor(t)
    clave = t.participacion_clave.replace("; ", ", ")
    fuente = t.participacion_fuente
    if fuente in ("enapres_asistencia", "enapres_patrimonio", "enapres_bienes"):
        fam = {"enapres_asistencia": "asistencia", "enapres_patrimonio": "patrimonio", "enapres_bienes": "bienes_culturales"}[fuente]
        a, ea = D.cultura(fam, clave, grupo_edad=edad)
        r = D.cultura(fam, clave, sexo=sexo)[0] / D.cultura(fam, clave, sexo="total")[0]
        prac = (a * r * f, ea * r * f)
        if t.latente_fuente == "enapres_motivos":
            l, el, _ = D.frenados_cultura(clave, grupo_edad=edad)
            rl = D.frenados_cultura(clave, sexo=sexo)[0] / D.frenados_cultura(clave, sexo="total")[0]
            return (*prac, l * rl * f, el * rl * f)
        return (*prac, np.nan, np.nan)
    if fuente == "enut_semana":
        k = D.patron_lm("participacion_semanal", clave, sexo, edad)
        return float(D.enut.loc[clave, "valor"]) * k * f, float(D.enut.loc[clave, "ee"]) * k * f, np.nan, np.nan
    if t.latente_fuente == "enaho_preu":
        # La ENAHO pregunta el motivo para no estudiar solo hasta los 24 años; para 15-19 se usa el dato de 16-19.
        if edad == "25-29":
            return np.nan, np.nan, np.nan, np.nan
        v, e = D.enaho("base_preu_motivo_economico", sexo, "16-19" if edad == "15-19" else edad)
        return np.nan, np.nan, v, e
    if t.latente_fuente == "enaho_empleo":
        b, eb = D.enaho("busca_trabajo", sexo, edad)
        bq, ebq = D.enaho("busca_o_quiere_trabajar", sexo, edad)
        return b * f, eb * f, (bq - b) * f, (ebq ** 2 + eb ** 2) ** 0.5 * f
    if fuente == "enaho_segmento":
        # Independientes = ocupados del público × % de independientes entre los ocupados (este último solo existe para 15-29).
        ocupados = D.enaho("solo_trabaja", sexo, edad)[0] + D.enaho("estudia_y_trabaja", sexo, edad)[0]
        share, e_share = D.enaho("independiente_ocupados", sexo, "15-29")
        v = ocupados * share / 100
        return v * f, v * e_share / share * f, np.nan, np.nan
    return np.nan, np.nan, np.nan, np.nan


def total_lima_este(D, t):
    """Cifras de 15-29 años (sin el factor) para mostrar el dato original de cada tipo."""
    clave = t.participacion_clave.replace("; ", ", ")
    out = {"prac_valor": np.nan, "prac_precision": "", "fren_valor": np.nan, "fren_dinero": np.nan,
           "fren_informacion": np.nan, "fren_oferta": np.nan, "prac_fuente": "", "fren_fuente": ""}
    f = t.participacion_fuente
    if f.startswith("enapres"):
        fam = {"enapres_asistencia": "asistencia", "enapres_patrimonio": "patrimonio", "enapres_bienes": "bienes_culturales"}[f]
        q = D.cul[(D.cul.familia == fam) & (D.cul.item == clave) & (D.cul.categoria == "Sí") & (D.cul.sexo == "total")].iloc[0]
        verbo = {"asistencia": "fue", "patrimonio": "visitó", "bienes_culturales": "jugó"}[fam]
        out.update(prac_valor=q.valor, prac_precision=q.precision,
                   prac_fuente=f"ENAPRES 2022-2025 · {verbo} en los últimos 12 meses: {clave.lower()}")
        if t.latente_fuente == "enapres_motivos":
            v, _, partes = D.frenados_cultura(clave, sexo="total")
            out.update(fren_valor=v, fren_dinero=partes["dinero"], fren_informacion=partes["informacion"],
                       fren_oferta=partes["oferta"],
                       fren_fuente="ENAPRES 2022-2025 · no fue por falta de dinero, de información o de oferta")
    elif f == "enut_semana":
        out.update(prac_valor=D.enut.loc[clave, "valor"], prac_precision=D.enut.loc[clave, "precision"],
                   prac_fuente=f"ENUT 2024 · lo hizo en la última semana: {clave.lower()}")
    elif f == "enaho_segmento":
        v = D.enaho(clave, "total", "15-29")[0]
        txt = {"busca_trabajo": "busca trabajo", "independiente": "trabaja por su cuenta o es empleador"}[clave]
        out.update(prac_valor=v, prac_precision="confiable", prac_fuente=f"ENAHO 2022-2025 · {txt}")
    if t.latente_fuente == "enaho_preu":
        v = D.enaho("base_preu_motivo_economico", "total", "15-24")[0]
        out.update(fren_valor=v, fren_dinero=v, fren_fuente="ENAHO 2022-2025 · 15 a 24 años que terminaron la secundaria y no "
                                                            "estudian por motivo económico")
    if t.latente_fuente == "enaho_empleo":
        v = D.enaho("busca_o_quiere_trabajar", "total", "15-29")[0] - D.enaho("busca_trabajo", "total", "15-29")[0]
        out.update(fren_valor=v, fren_fuente="ENAHO 2022-2025 · no tiene trabajo, quiere trabajar, pero no busca")
    return out


def main():
    D = Datos()
    tipos = pd.read_csv(RAIZ / "fuentes" / "modelo_tipos_actividad.csv", dtype=str).fillna("")
    fichas = pd.read_csv(RES / "fichas_actividad.csv").set_index("id")
    oferta = pd.read_csv(RAIZ / "fuentes" / "capa3_registro_oferta.csv").set_index("id")
    pob = D.pob_dist.groupby(["sexo", "edad"]).poblacion.sum()

    # ---------------------------------------------------------------- perfil de cada público
    perfil, tiempo = [], {}
    for s, e in PUBLICOS:
        bloques, evita = D.tiempo_libre(s, e)
        mejor = max(bloques, key=bloques.get)
        tiempo[(s, e)] = (bloques[mejor], mejor)
        dist = D.pob_dist[(D.pob_dist.sexo == s) & (D.pob_dist.edad == e)].set_index("distrito").poblacion
        perfil.append({"sexo": s, "edad": e, "poblacion": int(pob[(s, e)]), "mejor_bloque": mejor, "tiempo_libre": bloques[mejor],
                       **{f"bloque_{i}": v for i, v in enumerate(bloques.values())},
                       "evita_salir_noche": evita, "inseguro_noche": D.seguridad_publico("noche_inseguro", s, e),
                       **{k: D.enaho(k, s, e)[0] for k in SITUACION},
                       **{f"distrito_{d}": v / pob[(s, e)] * 100 for d, v in dist.items()}})
    pd.DataFrame(perfil).round(3).to_csv(RES / "modelo_perfil_publicos.csv", index=False)

    # ---------------------------------------------------------------- embudo por tipo y público
    filas = []
    for t in tipos.itertuples():
        for s, e in PUBLICOS:
            pr, epr, fr, efr = demanda(D, t, s, e)
            filas.append({"id": t.id, "sexo": s, "edad": e, "poblacion": int(pob[(s, e)]), "ya": pr, "ya_ee": epr,
                          "frenados": fr, "frenados_ee": efr, "tiempo_libre": tiempo[(s, e)][0], "bloque": tiempo[(s, e)][1]})
    P = pd.DataFrame(filas)
    P["medido"] = P.ya.notna() | P.frenados.notna()
    P["demanda"] = P.ya.fillna(0) + P.frenados.fillna(0)
    P["conv_ya"] = P.poblacion * P.ya.fillna(0) / 100 * P.tiempo_libre / 100
    P["conv_frenados"] = P.poblacion * P.frenados.fillna(0) / 100 * P.tiempo_libre / 100
    P["convocables"] = P.conv_ya + P.conv_frenados
    P[P.groupby("id").medido.transform("any")].round(3).to_csv(RES / "modelo_publicos.csv", index=False)

    # ---------------------------------------------------------------- incertidumbre (errores estándar de las encuestas)
    rng = np.random.default_rng(SEMILLA)
    ya = np.clip(rng.normal(P.ya.fillna(0), P.ya_ee.fillna(0), (N_SIM, len(P))), 0, None)
    fr = np.clip(rng.normal(P.frenados.fillna(0), P.frenados_ee.fillna(0), (N_SIM, len(P))), 0, None)
    conv = P.poblacion.values * (ya + fr) / 100 * P.tiempo_libre.values / 100
    sim = pd.DataFrame({i: conv[:, (P.id == i).values].sum(axis=1) for i in tipos.id})

    # ---------------------------------------------------------------- resultado por tipo
    res = []
    for t in tipos.itertuples():
        x = P[P.id == t.id]
        medido = bool(x.medido.any())
        if t.ficha:
            codigo = fichas.loc[t.ficha, "convocatoria_codigo"]
            detalle = fichas.loc[t.ficha, "convocatoria_detalle_codigo"]
            detalle = "sin registros comparables" if pd.isna(detalle) else detalle
            ids = [i for i in lista(fichas.loc[t.ficha, "actividades_c3"]) if i in oferta.index]
        else:
            ids = [i for i in lista(t.oferta_ids) if i in oferta.index]
            codigo, detalle = codigo_convocatoria(oferta.loc[ids])
        tot = x.convocables.sum()
        principal = x.loc[x.convocables.idxmax()] if medido else None
        res.append({"id": t.id, "tipo": t.tipo, "grupo": t.grupo, "linea": t.linea, "formato_sostenido": t.formato_sostenido,
                    "ficha": t.ficha, "medido": medido, "relacion": t.participacion_relacion, "factor": factor(t),
                    "frenados_medidos": t.latente_fuente != "ninguna", **total_lima_este(D, t),
                    "convocables": tot if medido else np.nan,
                    "convocables_ya": x.conv_ya.sum() if medido else np.nan,
                    "convocables_frenados": x.conv_frenados.sum() if medido else np.nan,
                    "convocables_inf": np.percentile(sim[t.id], 5) if medido else np.nan,
                    "convocables_sup": np.percentile(sim[t.id], 95) if medido else np.nan,
                    "pct_jovenes": 100 * tot / pob.sum() if medido else np.nan,
                    "pct_mujeres": 100 * x[x.sexo == "mujer"].convocables.sum() / tot if medido and tot else np.nan,
                    "publico_principal": f"{principal.sexo} {principal.edad}" if medido else "",
                    "conv_codigo": codigo, "conv_detalle": detalle, "oferta_ids": "; ".join(ids),
                    "necesidad": t.necesidad_tipo})
    R = pd.DataFrame(res)
    # Puesto dentro de cada grupo (actividades por un lado, servicios por otro) y su rango con el margen de error.
    for g in ["actividad", "servicio"]:
        m = (R.grupo == g) & R.medido
        R.loc[m, "puesto"] = R[m].convocables.rank(ascending=False, method="min")
        rk = sim[R[m].id.tolist()].rank(axis=1, ascending=False)
        R.loc[m, "puesto_inf"] = R[m].id.map(rk.quantile(0.05).round())
        R.loc[m, "puesto_sup"] = R[m].id.map(rk.quantile(0.95).round())
    R = R.sort_values(["grupo", "puesto", "id"]).round(3)
    R.to_csv(RES / "modelo_actividades.csv", index=False)

    pd.DataFrame([dict(zip(["paso", "nombre", "pregunta", "como_se_mide", "fuente", "ejemplo"], p)) for p in PASOS]) \
        .to_csv(RES / "modelo_criterios.csv", index=False)

    pd.set_option("display.width", 220)
    print(R[["grupo", "puesto", "puesto_inf", "puesto_sup", "id", "tipo", "convocables", "convocables_inf", "convocables_sup",
             "pct_mujeres", "publico_principal", "conv_codigo"]].to_string(index=False))


if __name__ == "__main__":
    main()
