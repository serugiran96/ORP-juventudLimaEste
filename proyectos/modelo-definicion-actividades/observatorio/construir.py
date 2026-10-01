"""Construye el Observatorio de Juventudes de Lima Este: un único HTML autocontenido.

Uso (desde la carpeta del proyecto):
    python scripts/modelo_actividades.py      # (si cambian los tipos o las fichas) modelo de convocatoria -> resultados/modelo_*.csv
    python observatorio/construir.py          # -> observatorio/salida/observatorio.html

El script NO estima nada: lee los datasets finales de data/processed/, fuentes/ y resultados/, los ordena en un JSON
(capas/*.py) y lo incrusta en la página junto con el HTML de cada capa (fuente/html/), el CSS, el JavaScript
(fuente/js/), la librería de gráficos (ECharts 5.6.0) y las tipografías. El HTML resultante se abre con doble clic y
funciona sin conexión.

Reglas que aplica a toda cifra de encuesta (capas/comun.py):
- cada estimación lleva su intervalo de confianza del 95 %, su CV y su precisión;
- las no publicables (CV > 25 %) se envían sin valor (la página muestra "—");
- las cantidades de personas se calculan como % (IC 95 %) × población 2026 de Dato Joven del mismo grupo.
"""

import base64
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from capas import contexto, cruce, intereses, oferta  # noqa: E402
from capas.comun import RAIZ  # noqa: E402

SALIDA = AQUI / "salida"
FUENTE = AQUI / "fuente"
TIPOGRAFIAS = [("Onest", "onest-latin.woff2"), ("Unbounded", "unbounded-latin.woff2"), ("Geist", "geist-latin.woff2")]


def b64(ruta):
    return base64.b64encode(ruta.read_bytes()).decode()


def commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def main():
    datos = {"meta": {"generado": date.today().isoformat(), "commit": commit()},
             "contexto": contexto.construir(), "intereses": intereses.construir(), "oferta": oferta.construir(),
             "cruce": cruce.construir()}
    js_datos = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    fuentes = "".join(f"@font-face{{font-family:'{n}';font-style:normal;font-weight:400 700;font-display:swap;"
                      f"src:url(data:font/woff2;base64,{b64(AQUI / 'vendor' / 'fuentes' / f)}) format('woff2')}}\n"
                      for n, f in TIPOGRAFIAS)
    html_capas = "\n".join(p.read_text(encoding="utf-8") for p in sorted((FUENTE / "html").glob("*.html")))
    js = "\n".join(p.read_text(encoding="utf-8") for p in sorted((FUENTE / "js").glob("*.js")))
    app = "(function () {\n\"use strict\";\n" + js + "\n})();"
    piezas = {"FUENTES": fuentes, "ESTILOS": (FUENTE / "estilos.css").read_text(encoding="utf-8"), "HTML": html_capas,
              "DATOS": js_datos, "ECHARTS": (AQUI / "vendor" / "echarts.min.js").read_text(encoding="utf-8"), "APP": app}
    for nombre in ("ECHARTS", "APP"):
        assert "</script" not in piezas[nombre].lower(), f"{nombre} contiene </script>"
    plantilla = (FUENTE / "plantilla.html").read_text(encoding="utf-8")
    faltan = [n for n in piezas if f"/*{n}*/" not in plantilla]
    assert not faltan, f"Marcas faltantes en la plantilla: {faltan}"
    # Una sola pasada sobre la plantilla: el contenido insertado no se vuelve a examinar.
    html = re.sub(r"/\*(FUENTES|ESTILOS|HTML|DATOS|ECHARTS|APP)\*/", lambda m: piezas[m.group(1)], plantilla)
    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / "observatorio.html"
    destino.write_text(html, encoding="utf-8")
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
