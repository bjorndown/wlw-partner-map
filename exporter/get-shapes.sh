#!/bin/sh
set -o errexit
curl https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2022-05/swissboundaries3d_2022-05_2056_5728.shp.zip > swissboundaries3d.zip
mkdir -p shapes
unzip -u swissboundaries3d.zip -d shapes
rm swissboundaries3d.zip