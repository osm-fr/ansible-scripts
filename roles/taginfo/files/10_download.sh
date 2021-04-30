#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
if [ -d /data/work/taginfo/data ]; then
 echo "$(date --rfc-3339=s) DEBUG: dir ok"
else
 echo "$(date --rfc-3339=s) WARN: dir /data/work/taginfo/data inexistant. tentative mkdir"
 mkdir -p /data/work/taginfo/data || { echo "$(date --rfc-3339=s) ERROR: mkdir" ; exit 1 ; }
 echo "$(date --rfc-3339=s) INFO: mkdir ok"
fi
cd /data/work/taginfo/data || { echo "$(date --rfc-3339=s) ERROR: cd" ; exit 1 ; }
if [ -f france.osm.pbf ]; then
  echo "$(date --rfc-3339=s) INFO: ${0} pbf avant download"
  ls -l france.osm.pbf
else
  echo "$(date --rfc-3339=s) INFO: ${0} pas de pbf avant download"
fi
wget -N http://download.openstreetmap.fr/extracts/europe/france.osm.pbf || echo "$(date --rfc-3339=s) ERROR: wget"
echo "$(date --rfc-3339=s) INFO: ${0} pbf apres download"
ls -l france.osm.pbf
wget -q -N http://download.openstreetmap.fr/extracts/europe/france.state.txt || echo "$(date --rfc-3339=s) ERROR: wget" 
mv france.state.txt ../osmosis/state.txt || { echo "$(date --rfc-3339=s) ERROR: mv" ; exit 1 ; }
echo "$(date --rfc-3339=s) INFO: ${0} retrait relation admin hors france"
./remove-not-in-france.sh || echo "$(date --rfc-3339=s) ERROR: remove-not-in-france.sh but trying to continue" 
echo "$(date --rfc-3339=s) INFO: ${0} recherche timestamp des donnees"
osmconvert france.osm.pbf --out-statistics | grep "^timestamp max: " | sed "s/timestamp max: //" | tee france.osm.pbf.timestamp
echo "$(date --rfc-3339=s) INFO: ${0} end."
