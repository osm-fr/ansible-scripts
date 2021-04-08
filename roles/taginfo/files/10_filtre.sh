#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
osmconvert data/france.osm.pbf -B=france.poly --complete-multipolygons --complete-boundaries -o=tmp.pbf ; mv tmp.pbf data/france.osm.pbf
echo "$(date --rfc-3339=s) INFO: ${0} end."
