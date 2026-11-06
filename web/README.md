# Sitio público de la Organización Juvenil Rita Poma

Es la página que se ve en **https://web.organizacionritapoma.workers.dev/**. Está alojada en Cloudflare, en un
Worker llamado `web`.

Es un sitio **público**: todo lo que está en `publico/` lo puede ver cualquier persona. El observatorio de juventudes
es **interno** y **no** está aquí (ver más abajo).

## Qué tiene

| Dirección | Página | Archivo |
|---|---|---|
| `/` | Portada con botones, tipo "linktree" | `publico/index.html` |
| `/rita-poma-y-el-puno/` | Informe *Rita Poma y el Puno de su tiempo* en formato web | `publico/rita-poma-y-el-puno/index.html` |
| `/descargas/rita-poma-y-el-puno-de-su-tiempo.pdf` | El mismo informe en PDF | `publico/descargas/` |
| `/observatorio/` | Ya no existe: lleva a la portada | `publico/_redirects` |
| cualquier otra | Página "no existe" | `publico/404.html` |

## Estructura

```
web/
├── README.md            este archivo
├── wrangler.jsonc       configuración del Worker "web" (para publicar desde la terminal)
├── og/plantilla.html    plantilla de las imágenes para compartir (no se publica)
└── publico/             TODO lo que se sube a Cloudflare
    ├── index.html                    portada
    ├── rita-poma-y-el-puno/index.html  informe
    ├── 404.html                      página de error
    ├── _redirects                    redirecciones (Cloudflare las lee; no se ven como página)
    ├── .assetsignore                 archivos que no se suben (.DS_Store)
    ├── favicon.ico
    ├── descargas/                    PDF del informe
    └── recursos/
        ├── css/marca.css             colores, tipografías y botones del manual de marca
        ├── css/portada.css           diseño de la portada
        ├── css/documento.css         diseño del informe
        ├── js/documento.js           interacción del informe (opcional: sin él se lee igual)
        ├── fuentes/                  Anton y Archivo (licencia SIL OFL 1.1, archivos OFL-*.txt)
        ├── img/                      logos y elementos gráficos del kit de marca
        ├── favicon/                  íconos del kit de marca
        └── og/                       imágenes que aparecen al compartir el enlace
```

No hay que instalar nada ni compilar nada: son archivos HTML, CSS y JavaScript simples.

## Marca

Todo sale del *Manual de marca 2026* y del *Kit de marca*:

- **Colores:** rojo carmesí `#B71C32`, azul luminoso `#557FE0`, verde soleado `#70C447`, blanco cálido `#FAFAF7`,
  gris claro `#EDEEEA`, negro carbón `#252525` y negro profundo `#181818` (en `recursos/css/marca.css`).
- **Tipografías:** Anton para titulares; Archivo para textos, subtítulos y antetítulos.
- **Versión oscura** (portadas, impacto) en la portada; **versión clara** (documentos y web) en el informe.
- **Línea de fuego** siempre en línea, nunca rellena; **banda de libros** como remate inferior; **libro sólido** como viñeta.
- **Diseño editorial, no de plantilla:** separaciones con líneas finas (como el índice del manual) y tablas como las
  del PDF. Sin tarjetas con bordes de colores, sin cajas de cifras y sin fechas en los rótulos.
- Logos sin deformar, sin sombras y por encima del tamaño mínimo (isotipo ≥ 48 px, logo principal ≥ 120 px).

## Verlo en tu computadora

Abre la Terminal en esta carpeta (`web/`) y escribe:

```bash
python3 -m http.server 8000 -d publico
```

Luego entra a <http://localhost:8000> en el navegador. Para cerrarlo: `Ctrl + C`.

También se puede abrir `publico/index.html` con doble clic y los botones funcionan, pero el navegador bloquea las
tipografías de la marca en archivos locales (se ven otras letras). Para revisar el diseño, usa el comando de arriba.

## Publicar en Cloudflare

Cada publicación **reemplaza todo** lo que había en el Worker `web` por lo que hay en `publico/`. Lo que no esté en
`publico/` deja de existir en internet.

### Opción A · Desde la terminal (recomendada)

Necesita Node.js (ya está instalado). Desde la carpeta `web/`:

```bash
npx wrangler login      # solo la primera vez: abre el navegador para entrar a Cloudflare
npx wrangler deploy     # publica publico/ en el Worker "web"
```

Usa `wrangler.jsonc`, que ya tiene el nombre del Worker (`web`), la carpeta (`./publico`) y la página 404.

### Opción B · Desde el panel de Cloudflare

1. Entra a <https://dash.cloudflare.com> → **Workers & Pages** → el Worker **web**.
2. Busca la opción para subir una nueva versión de los archivos estáticos (la misma con la que se subió `sitio/` el
   1 de octubre) y arrastra **la carpeta `publico`** completa.
3. Publica (Deploy) esa versión.

### Después de publicar, revisar

- La portada abre en <https://web.organizacionritapoma.workers.dev/>.
- El botón lleva al informe y el PDF se descarga.
- <https://web.organizacionritapoma.workers.dev/observatorio/> **ya no muestra el observatorio** (lleva a la portada).

## Agregar un botón a la portada

En `publico/index.html`, dentro de `<ul class="enlaces">`, copia un `<li>` completo y cambia el enlace y el título:

```html
<li>
  <a class="enlace" href="DIRECCIÓN-DEL-ENLACE">
    <span class="enlace__titulo">Título del botón</span>
    <svg …>…</svg>  <!-- la flecha: copiarla igual que en el botón existente -->
  </a>
</li>
```

- Los botones son cápsulas como los stickers del manual y toman los colores en orden: rojo, azul, blanco.
- Si es una página nueva del sitio: crea una carpeta en `publico/` con su `index.html` y usa `href="nombre-carpeta/"`.
- Si es un enlace externo (Instagram, WhatsApp, formulario): usa la dirección completa, por ejemplo
  `href="https://www.instagram.com/ritapoma.limaeste/"`.

## Actualizar el informe

- **Texto de la web:** está en `publico/rita-poma-y-el-puno/index.html`, copiado tal cual del PDF. Cada capítulo es
  un `<section id="…">` y las citas van dentro de `<span class="ref">(Autor, año)</span>` (se ven en gris).
- **PDF:** reemplaza `publico/descargas/rita-poma-y-el-puno-de-su-tiempo.pdf` manteniendo el mismo nombre.
- **Contacto al final** («¿Tienes más información?»): correo `organizacionritapoma@gmail.com` e Instagram
  `@ritapoma.limaeste`. Están en la sección `id="mas-informacion"` del mismo archivo.

## Imágenes para compartir

`publico/recursos/og/portada.png` y `documento.png` (1200 × 630 px) son las que aparecen al compartir los enlaces por
WhatsApp, Facebook o Instagram. Se hicieron con `og/plantilla.html` (`?pieza=portada` o `?pieza=documento`),
abierta en un navegador de 1200 × 630 y capturada. Están enlazadas con la dirección completa del sitio: si algún día
se usa otro dominio (por ejemplo `organizacionritapoma.com`), hay que cambiar esa dirección en las etiquetas
`og:image` de cada página.

## El observatorio (interno)

El Observatorio de Juventudes de Lima Este está en `proyectos/modelo-definicion-actividades/observatorio/` y se
genera solo en local (`salida/` no se versiona). **No se publica en este sitio.** Si se necesita compartirlo con el
equipo, debe ir en un Worker aparte protegido con Cloudflare Access (acceso solo por correo autorizado), nunca en
`publico/`.
