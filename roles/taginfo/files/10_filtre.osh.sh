#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
#osmconvert data/france.osh.pbf -B=france.poly --complete-multipolygons --complete-boundaries --timestamp="2022-01-17T00:59:37Z" -o=tmp.osh.pbf ; mv tmp.osh.pbf data/france.osh.pbf
osmium extract --with-history --overwrite -p france.poly data/france.osh.pbf -o tmp.osh.pbf ; mv tmp.osh.pbf data/france.osh.pbf
echo "$(date --rfc-3339=s) INFO: ${0} end."
