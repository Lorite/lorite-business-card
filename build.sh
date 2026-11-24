#!/usr/bin/env bash
# Render card.html to print PDFs: a 91 x 61 mm page (85 x 55 mm trim + 3 mm bleed) and an A4 sheet of 10 cards with cut marks.
# The phone number comes from private.env (git ignores it). Without that file, or with PUBLIC=1, the phone line is removed,
# which is what the GitHub Actions build does. PUBLIC=1 also writes docs/preview.png for the README.
# It also writes Alejandro-Lorite-Mora.vcf from contact.vcf, with the same rule for the phone line.
set -euo pipefail
cd "$(dirname "$0")"
PLACEHOLDER="+45 00 00 00 00"
PHONE=""
if [ "${PUBLIC:-0}" != 1 ] && [ -f private.env ]; then
    # shellcheck disable=SC1091
    source private.env
fi
if [ -n "$PHONE" ]; then
    sed "s|$PLACEHOLDER|$PHONE|g" card.html > .card.build.html
    sed "s|$PLACEHOLDER|$PHONE|g" contact.vcf > Alejandro-Lorite-Mora.vcf.tmp
else
    echo "No phone number (no private.env or PUBLIC=1): building without the phone line"
    sed '/class="phone"/d' card.html > .card.build.html
    sed '/^TEL/d' contact.vcf > Alejandro-Lorite-Mora.vcf.tmp
fi
# vCard lines end in CRLF (RFC 2426)
sed 's/\r\?$/\r/' Alejandro-Lorite-Mora.vcf.tmp > Alejandro-Lorite-Mora.vcf
rm -f Alejandro-Lorite-Mora.vcf.tmp
trap 'rm -f .card.build.html' EXIT
google-chrome --headless=new --disable-gpu --password-store=basic --no-pdf-header-footer \
    --virtual-time-budget=5000 --print-to-pdf=business-card-print.pdf "file://$PWD/.card.build.html" 2>/dev/null
uv run -q --with pypdf python finalize.py
pdfinfo -box business-card-print.pdf | grep -E "Media|Trim"
pdftoppm -r 400 -png business-card-print.pdf preview
if [ "${PUBLIC:-0}" = 1 ]; then
    mkdir -p docs
    pdftoppm -r 200 -png -singlefile business-card-print.pdf docs/preview
    echo "docs/preview.png written without the phone number"
fi
ls preview-*.png
