#!/bin/bash

################################################################################
# v1.1.0, 2023/04/11, Marc_marc:
# - pushd to bin dir to avoid the need of -i for sudo
################################################################################
# v1.0.0, 2023/03/09, Marc_marc:
# - initial public release
################################################################################
## Copyrights Marc_marc <marcmarcmarcmarc@protonmail.com> 2023                ##
## License : GNU General Public License as published by                       ##
## the Free Software Foundation, either version 3 of the License,             ##
## or (at your option) any later version.                                     ##
## http://www.gnu.org/licenses/                                               ##
################################################################################

# exemple d'utilisation simplie dans l'infrastructure osm-fr
# ssh osm144.openstreetmap.fr sudo -u umap /srv/umap/anonymous_edit_url.sh htps:/....
# ssh osm144.openstreetmap.fr sudo -u umap /srv/umap/anonymous_edit_url.sh 42

echo "$(date --rfc-3339=s) INFO: ${0} start..."

pushd $(dirname ${0}) > /dev/null || { echo "unable to cd $(dirname ${0}) ; exit 2 ; }

if [ -z "${1}" ]; then
  echo "usage: ${0} numero_de_carte"
  exit 1
fi
source venv/bin/activate
umap anonymous_edit_url $(echo $1 | cut -d"#" -f1 | cut -d"_" -f2) | grep http | sed "s/http:/https:/" | sed "s/\/en\//\/fr\//"

popd > /dev/null

echo "$(date --rfc-3339=s) INFO: ${0} end."
