#! /bin/bash

set -e

echo "Starting launch-acme-tiny.sh"

need_update=0

if [ ! -f "./signed.crt" ]; then
  need_update=1
elif [ "$(find ./account.key ./domain.csr -newer ./signed.crt)" ]; then
  need_update=1
elif [ "$(find ./signed.crt -mtime +62)" ]; then
  # file is more than 2 months old
  need_update=1
fi

if [ "$need_update" -eq 0 ]; then
  echo "Update is not necessary"
  exit 0
fi

python ../acme-tiny/acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir /data/project/letsencrypt/challenges > ./signed.crt.tmp

mv ./signed.crt.tmp ./signed.crt

if [ -e intermediate.pem ]; then
  cat ./signed.crt intermediate.pem > chained.pem
  if [ -e /etc/init.d/apache2 ]; then
    sudo /etc/init.d/apache2 reload
    echo "apache2 was reloaded"
  fi
  if [ -e /etc/init.d/nginx ]; then
    sudo /etc/init.d/nginx reload
{% if inventory_hostname == "osm26.openstreetmap.fr" %}
    ssh letsencrypt@osm27.openstreetmap.fr sudo /etc/init.d/nginx reload
    ssh letsencrypt@osm28.openstreetmap.fr sudo /etc/init.d/nginx reload
{% endif %}
    echo "nginx was reloaded"
  fi
fi
