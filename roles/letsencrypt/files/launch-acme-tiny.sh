#! /bin/sh

set -e

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
