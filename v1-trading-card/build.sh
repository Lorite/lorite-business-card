#!/usr/bin/env bash
# Render card.html to a print PDF (69 x 94 mm pages = 63 x 88 mm trim + 3 mm bleed) and PNG previews.
set -euo pipefail
cd "$(dirname "$0")"
google-chrome --headless=new --disable-gpu --password-store=basic --no-pdf-header-footer \
    --virtual-time-budget=5000 --print-to-pdf=business-card-print.pdf "file://$PWD/card.html" 2>/dev/null
uv run -q --with pypdf python finalize.py
pdfinfo -box business-card-print.pdf | grep -E "Media|Trim"

pdftoppm -r 400 -png business-card-print.pdf preview
ls preview-*.png
