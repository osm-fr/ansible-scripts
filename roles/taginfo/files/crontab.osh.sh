#!/bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."

# cette version met a jour le pbf local a partir des diff (2h) mais peux être relancé au besoin
#./10_update_pbf.sh

# cette version telecharge le pbf maj sur download.osm.fr (5min) mais nécessite d'être lancé après cette maj evidement
#./10_download.sh

# 2019/04/04 temporairement faire download+maj vu probleme maj sur download.openstreetmap.fr
# 2019/06/08 changement des && en ; pour eviter qu'une erreur de maj empeche l'utilisation du nouveau pbf telecharge
#./10_download.sh ; ./10_update_pbf.sh

# 2019/06/13 osmosis (2h30 pour maj+filtre) -> osmosis (30min pour maj) + osmfilter (15min pour filtre)
./10_update_pbf.osh.sh ; ./10_filtre.osh.sh

echo "DEBUG: le reste ne fonctionne pas ou pas encore en osh"
exit 0
# environ 35min
./remove-metadata.osh.sh

# environ 15min
./20_update.sh ; ./30_restart_webserver.sh

echo "$(date --rfc-3339=s) INFO: ${0} end."
