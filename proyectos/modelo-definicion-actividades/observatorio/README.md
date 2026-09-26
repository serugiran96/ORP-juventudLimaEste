# Observatorio de Juventudes de Lima Este

Página web estática de la Organización Juvenil Rita Poma. Reúne en un solo archivo HTML las tres capas del
proyecto (contexto, intereses, oferta), el cruce de evidencia y las fichas de alternativas de actividades.
Se genera con R y Quarto. No necesita servidor ni Shiny: todos los filtros funcionan en el navegador.

> **Versión local de revisión.** No se publica en internet. El HTML incorpora datos agregados de `data/`, que
> no se versionan; por eso `salida/` está en `.gitignore`.

## Cómo generarlo

Requisitos:

- R 4.3 o posterior (probado con R 4.6.1).
- Quarto 1.4 o posterior (probado con 1.10.18, el que trae RStudio).
- Los datos procesados de las capas y de la integración. Los genera el proyecto (ver el `README.md` principal);
  el observatorio solo los lee.

```bash
cd observatorio
Rscript instalar_paquetes.R     # solo la primera vez
quarto render                   # o, con el Quarto de RStudio en macOS:
# /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
```

El resultado es `salida/observatorio.html` (unos 6 MB). Incluye todo: estilos, código y gráficos.

## Cómo abrirlo

Abre `salida/observatorio.html` con doble clic, o arrástralo a un navegador (Chrome, Firefox, Safari o Edge).
Funciona sin conexión; con internet usa las tipografías de Google Fonts, y sin conexión usa las del sistema.

Cada sección tiene su dirección: `observatorio.html#oferta`, `#actividades`, `#F-05` (una ficha) o `#H2-12`
(un hallazgo).

## Estructura

| Archivo | Qué hace |
|---|---|
| `observatorio.qmd` | Página principal: cabecera, navegación, las seis secciones y el pie. |
| `paginas/_inicio.qmd` … `_actividades.qmd` | Una sección cada uno. |
| `R/paquetes.R` | Carga los paquetes. |
| `R/datos.R` | Lee los datasets y define `ev()`, que cita las cifras desde `resultados/evidencias.csv`. |
| `R/estilo.R` | Paleta, tema de los gráficos y gráficos de puntos con intervalo. |
| `R/componentes.R` | Piezas de página: indicadores, bloques de lectura, pestañas, filtros de chips y referencias. |
| `R/fichas.R` | Fichas de actividades: recorrido de ocho pasos, tamaño con dos bases y componentes. |
| `estilos/observatorio.css` | Diseño. |
| `js/observatorio.js` | Navegación por secciones y pestañas, filtros de chips, explorador de fichas y contadores de la oferta. |
| `instalar_paquetes.R` | Instala los paquetes de R que faltan. |

## Datos por sección

| Sección | Datasets |
|---|---|
| Inicio | `data/processed/capa1_poblacion_joven_distritos.csv` (Dato Joven 2026) y `resultados/evidencias.csv`, `hallazgos_integrados.csv`, `fichas_actividad.csv`. |
| Contexto | Población: `capa1_poblacion_joven_distritos.csv`. Estudio y trabajo: `integracion_enaho_segmentos.csv`. Seguridad: `integracion_seguridad_enapres.csv`. Organización: `capa1_renoj_resumen_distritos.csv`, `capa1_voluntariado_resumen_distritos.csv`. Registros: `capa1_registros_resumen.csv`, `capa1_registros_distrito_anio.csv`. Lima Metropolitana: `resultados/evidencias.csv`. |
| Intereses | Uso del tiempo: `capa2_uso_tiempo_enut.csv`. Horarios: `integracion_tiempo_enut.csv`. Cultura: `capa2_cultura_enapres.csv`, `integracion_cultura_edad_enapres.csv`. Vida digital: `capa2_educacion_internet_enaho.csv`, `capa2_cultura_enapres.csv`. Aspiraciones: `fuentes/capa2_estudios_ipsos.csv`. |
| Oferta | `fuentes/capa3_registro_oferta.csv` y `data/raw/capa3/gobpe_listado.csv` (solo se cuentan notas por distrito y año). |
| Cruce de evidencia | `resultados/evidencias.csv`, `hallazgos_integrados.csv`, `patrones.csv`, `segmentos.csv`, `cambios_primera_version.csv`, `validacion_integracion.csv`. |
| Actividades | `resultados/fichas_actividad.csv`, `fichas_componentes.csv`, `fichas_convocatoria.csv`, `segmentos.csv`, `evidencias.csv`. |

Salvo que se indique otra carpeta, los archivos están en `data/processed/`. El observatorio no recalcula
estimaciones: filtra, ordena y dibuja lo que produjo el pipeline de Python.

## Reglas de contenido

- **Cifras.** Las cifras de los textos se citan con `ev("E-###")` desde `resultados/evidencias.csv`, igual que el
  informe; no se escriben a mano.
- **Precisión.** Una cifra referencial (CV entre 15 % y 25 %) lleva asterisco en el texto y marcador hueco en el
  gráfico. Una no publicable no se muestra; `ev()` se detiene si se la pide.
- **Color y forma.**
  - El color indica el ámbito: rojo, Lima Este; negro, Lima Metropolitana; gris, Perú urbano.
  - En los gráficos por sexo, la forma indica el sexo: círculo, mujeres; rombo, hombres; cuadrado, total.
- **Etiquetas.** Cada bloque de gráfico sigue la secuencia "¿Qué nos dice?" → "Importante" → fuente, y lleva la
  etiqueta de su ámbito.
- **Cantidades.** Se muestran con las dos bases de población (Dato Joven 2026 y la expansión de la encuesta), sin
  combinarlas.
- **Actividades.**
  - No hay ranking: las fichas se ordenan por línea temática.
  - El estado de cada paso del recorrido sale de reglas fijas sobre los códigos de la integración
    (`R/fichas.R`), no de un juicio caso por caso.

## Interacciones

- Navegación entre las seis secciones y pestañas internas, sin recargar la página.
- **Contexto.** Filtros de sexo y grupo de edad en la población.
- **Oferta.**
  - Filtros de distrito, tema, público, tipo de evidencia, costo, año, organizador y tipo de oferta.
  - Los filtros actualizan los indicadores, los gráficos y la tabla.
  - Una actividad con varios distritos o temas aparece al filtrar por cualquiera de ellos.
- **Cruce de evidencia.**
  - Filtros de patrones por tipo, y de hallazgos por capa y por cambio respecto de la primera versión.
  - Buscador en el registro de evidencias.
  - Al pasar el cursor sobre una referencia E-### se ve su ficha técnica.
- **Actividades.**
  - Un mapa de evidencia enlaza con cada ficha.
  - Un explorador muestra una ficha a la vez, con índice filtrable por línea, tipo y alcance.
  - En cada ficha, las casillas del recorrido llevan al detalle de cada paso.
- **Gráficos.** Muestran el valor, el intervalo y la precisión al pasar el cursor.

## Limitaciones pendientes

- **Actividades.** Las fichas son alternativas derivadas de evidencia secundaria. La participación concreta se
  validará con jóvenes en una fase posterior.
- **Tipografías.** Sin internet se usan las del sistema, y el diseño cambia un poco.
- **Oferta.** El registro se basa en notas consultadas el 25/09/2026 y no se actualiza solo.
- **Tamaño.** El HTML pesa unos 6 MB porque incluye las librerías de gráficos y tablas.
- **Pantallas pequeñas.** Se probó en navegador de escritorio y a 500 px de ancho. Las tablas anchas se desplazan
  dentro de su recuadro.
