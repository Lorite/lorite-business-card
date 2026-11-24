#!/usr/bin/env bash
# Re-render Spot and the drone from the Slidev theme's stick props, then make the color, duotone and watermark PNGs.
# Needs a folder with `npm i playwright@1.63.0`: pass it as PW=<dir>.
set -euo pipefail
cd "$(dirname "$0")"
TH=~/git/lorite_presentations_phd_slidev/slidev-theme-lorite-phd/stick
cp "$TH/stick.js" "$TH/robots.js" .
NODE_PATH="$PW/node_modules" node shot.mjs
A=../assets
convert duo.png -trim +repage "$A/robots-color.png"
convert "$A/robots-color.png" \( +clone -alpha extract \) \( -clone 0 -alpha off -colorspace gray +level-colors "#1b2a41","#bfe6e8" \) -delete 0 +swap -compose CopyOpacity -composite "$A/robots-duotone.png"
convert "$A/robots-color.png" \( +clone -alpha extract \) \( -clone 0 -alpha off -colorspace gray +level-colors "#c9d0d8","#eef1f4" \) -delete 0 +swap -compose CopyOpacity -composite "$A/robots-watermark.png"
rm -f stick.js robots.js duo.png
