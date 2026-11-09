#!/bin/sh
# Create the Python environment for sss-browser-2 in the directory given as $1.
# torch comes from the CPU-only index (about 3.4 GB smaller than the CUDA build);
# everything else from PyPI, pinned by restricciones.txt. Needs internet.
# The new environment is built next to the target and only moved into place when complete.
set -eu
VENV="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
NEW="$VENV.nuevo"
[ -e "$NEW" ] && rm -rf "$NEW"
python3 -m venv "$NEW"
"$NEW/bin/pip" install --disable-pip-version-check --no-input -q \
    --index-url https://download.pytorch.org/whl/cpu "torch==2.13.0"
"$NEW/bin/pip" install --disable-pip-version-check --no-input -q \
    -r "$HERE/requisitos.txt" -c "$HERE/restricciones.txt"
"$NEW/bin/python" -c "import torch, sentence_transformers, flask, ddgs, lxml, PySide6.QtWebEngineWidgets"
cat "$HERE/requisitos.txt" "$HERE/restricciones.txt" | md5sum | cut -d' ' -f1 > "$NEW/.sss-requisitos.md5"
if [ -e "$VENV" ]; then
    mv "$VENV" "$VENV.anterior"
    mv "$NEW" "$VENV"
    rm -rf "$VENV.anterior"
else
    mv "$NEW" "$VENV"
fi
echo "Entorno de SSS listo en $VENV ($(du -sh "$VENV" | cut -f1))"
