#!/bin/sh
# Copia el observatorio interno a web/publico/observatorio/ para publicarlo junto con el sitio.
# Esa carpeta está en .gitignore: el observatorio nunca se sube a GitHub (el repositorio es público).
#
# Uso, desde la carpeta web/:   sh copiar_observatorio.sh
set -e
cd "$(dirname "$0")"
ORIGEN="../proyectos/modelo-definicion-actividades/observatorio/salida/sitio/observatorio/index.html"
DESTINO="publico/observatorio/index.html"
if [ ! -f "$ORIGEN" ]; then
  echo "No encuentro el observatorio en $ORIGEN"
  echo "Genéralo primero (ver proyectos/modelo-definicion-actividades/observatorio/README.md)."
  exit 1
fi
mkdir -p publico/observatorio
cp "$ORIGEN" "$DESTINO"
echo "Listo: observatorio copiado en web/$DESTINO (no se sube a GitHub)."
