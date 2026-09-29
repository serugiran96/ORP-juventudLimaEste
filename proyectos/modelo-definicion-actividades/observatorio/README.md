# Observatorio de Juventudes de Lima Este

Página web de la Organización Juvenil Rita Poma. Reúne en un solo archivo HTML las tres capas del proyecto
(Contexto, Intereses y Oferta), el cruce de evidencia y el resultado: qué tipo de actividades tienen más respaldo
para convocar a los jóvenes de Lima Este.

Se genera con **Python** y se muestra con **HTML, CSS y JavaScript** (gráficos con ECharts). No necesita servidor:
se abre con doble clic y funciona sin conexión.

> **Versión local de revisión.** No se publica en internet. El HTML incorpora datos agregados de `data/`, que no se
> versionan; por eso `salida/` está en `.gitignore`.
>
> La versión anterior, hecha en R y Quarto, está en el historial de git (commit `013721b`).

## Cómo generarlo

```bash
# desde proyectos/modelo-definicion-actividades/
python scripts/web_contexto_enaho.py descargar     # solo si faltan los microdatos del Módulo 84 de la ENAHO
python scripts/web_contexto_enaho.py calcular      # educación por nivel y participación en organizaciones
python scripts/modelo_actividades.py               # modelo multicriterio (si cambian las fichas)
python observatorio/construir.py                   # -> observatorio/salida/observatorio.html
```

El resultado es `salida/observatorio.html`, de unos 1,8 MB. Incluye los datos, los estilos, el código, la librería
de gráficos y las tipografías.

Cada sección tiene su dirección:

- una pestaña: `#poblacion`, `#horarios`, `#explorar`, `#matriz`, `#resultado`…;
- una ficha: `#F-02`.

## Capas y pestañas

| Capa | Pestañas |
|---|---|
| Contexto | Población · Estudio y trabajo · Seguridad · Organizaciones · Natalidad · Datos extra (Lima Metropolitana) |
| Intereses | Su semana · Horarios · Cultura y ocio · Vida digital · Aspiraciones (Ipsos, exploratorio) |
| Oferta | Explorar · ¿Para quién? · Convocatoria · Visibilidad |
| Cruce | El modelo · La matriz · Grupos de jóvenes · Hallazgos · Evidencias |
| Actividades | Resultado (ranking con pesos ajustables) · Fichas · Protocolo y consulta |
| Acerca | Advertencias, fuentes y cómo se construyó |

## Estructura

| Archivo | Qué hace |
|---|---|
| `construir.py` | Arma el JSON de datos con `capas/` y lo incrusta, junto con el HTML, el CSS y el JavaScript, en `fuente/plantilla.html`. No estima nada. |
| `capas/comun.py` | Lectura de datos y formato de las estimaciones: IC 95 %, CV, precisión y rango de personas. |
| `capas/contexto.py`, `intereses.py`, `oferta.py`, `cruce.py` | Datos de cada capa. `cruce.py` lee el modelo, los segmentos, los patrones, los hallazgos, las evidencias y las fichas. |
| `fuente/plantilla.html` | Cabecera, navegación y pie. |
| `fuente/html/*.html` | El HTML de cada capa. |
| `fuente/js/*.js` | Lógica de cada capa: gráficos, filtros, lecturas automáticas y tablas "Ver datos". `99_app.js` maneja la navegación. |
| `fuente/estilos.css` | Diseño. |
| `vendor/` | ECharts 5.6.0 (licencia Apache 2.0) y las tipografías Onest, Unbounded y Geist (licencia SIL OFL 1.1). |

## Datos por capa

| Capa | Datos |
|---|---|
| Contexto | `capa1_poblacion_*` (Dato Joven), `web_educacion_enaho.csv`, `integracion_enaho_segmentos.csv`, `integracion_seguridad_enapres.csv`, `capa1_registros_*`, `web_participacion_enaho.csv`, `capa1_renoj_*`, `capa1_voluntariado_distritos.csv`, `capa1_resumen_lima_metropolitana.csv` |
| Intereses | `capa2_uso_tiempo_enut.csv`, `integracion_tiempo_enut.csv`, `capa2_cultura_enapres.csv`, `integracion_cultura_edad_enapres.csv`, `capa2_educacion_internet_enaho.csv`, `fuentes/capa2_estudios_ipsos.csv` |
| Oferta | `fuentes/capa3_registro_oferta.csv`, `data/raw/capa3/gobpe_listado.csv` |
| Cruce y Actividades | `resultados/modelo_*.csv`, `fichas_*.csv`, `segmentos.csv`, `patrones.csv`, `hallazgos_integrados.csv`, `evidencias.csv` |

Salvo que se indique otra carpeta, los archivos están en `data/processed/`.

## Reglas

- **Ámbito.** Las cifras de encuesta de Lima Este son de los siete distritos juntos, nunca por distrito. Los datos
  de Lima Metropolitana o del Perú urbano se rotulan así.
- **Precisión.**
  - Referencial (CV entre 15 % y 25 %): asterisco.
  - No publicable (CV mayor a 25 %): "—".
  - Las frases que comparan grupos solo afirman una diferencia si los intervalos de confianza no se superponen.
- **Cantidades.** Son rangos: % (IC 95 %) × población 2026 de Dato Joven del mismo grupo.
- **Modelo de actividades.** Ordena por respaldo en la evidencia; no predice asistencia. Criterios, reglas y pesos:
  `fuentes/metodologia_modelo_actividades.md`.
- **Colores.** Validados por contraste y daltonismo. Todo gráfico tiene su tabla equivalente ("Ver datos").
