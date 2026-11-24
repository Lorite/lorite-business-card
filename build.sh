#!/usr/bin/env bash
# Render card.html to print PDFs: a 91 x 61 mm page (85 x 55 mm trim + 3 mm bleed) and an A4 sheet of 10 cards with cut marks.
# The phone number comes from private.env (git ignores it). Without that file, or with PUBLIC=1, the card shows the placeholder
# from card.html, and PUBLIC=1 also writes docs/preview.png for the README.
set -euo pipefail
cd "$(dirname "$0")"
PLACEHOLDER="+45 00 00 00 00"
PHONE="$PLACEHOLDER"
if [ "${PUBLIC:-0}" != 1 ] && [ -f private.env ]; then
    # shellcheck disable=SC1091
    source private.env
fi
sed "s|$PLACEHOLDER|$PHONE|g" card.html > .card.build.html
trap 'rm -f .card.build.html' EXIT
google-chrome --headless=new --disable-gpu --password-store=basic --no-pdf-header-footer \
    --virtual-time-budget=5000 --print-to-pdf=business-card-print.pdf "file://$PWD/.card.build.html" 2>/dev/null
uv run -q --with pypdf python finalize.py
pdfinfo -box business-card-print.pdf | grep -E "Media|Trim"
pdftoppm -r 400 -png business-card-print.pdf preview
if [ "${PUBLIC:-0}" = 1 ]; then
    mkdir -p docs
    pdftoppm -r 200 -png -singlefile business-card-print.pdf docs/preview
    echo "docs/preview.png written with the placeholder phone number"
fi
ls preview-*.png
