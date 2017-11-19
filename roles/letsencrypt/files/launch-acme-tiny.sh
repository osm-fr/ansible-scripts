#! /bin/bash

set -e

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
  exit 0
fi

python ../acme-tiny/acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir /data/project/letsencrypt/challenges > ./signed.crt.tmp

mv ./signed.crt.tmp ./signed.crt

if [ -e intermediate.pem ]; then
  cat ./signed.crt intermediate.pem > chained.pem
  if [ -e /etc/init.d/apache2 ]; then
    sudo /etc/init.d/apache2 reload
  fi
  if [ -e /etc/init.d/nginx ]; then
    sudo /etc/init.d/nginx reload
  fi
fi
