#! /bin/bash

set -e

mkdir -p /etc/ssl/letsencrypt/
cp /data/project/letsencrypt/keys/chained.pem      "/etc/ssl/letsencrypt/chained.pem"
cp /data/project/letsencrypt/keys/domain.key       "/etc/ssl/letsencrypt/domain.key"
cp /data/project/letsencrypt/keys/dhparams.pem     "/etc/ssl/letsencrypt/dhparams.pem"
cp /data/project/letsencrypt/keys/intermediate.pem "/etc/ssl/letsencrypt/intermediate.pem"
cp /data/project/letsencrypt/keys/signed.crt       "/etc/ssl/letsencrypt/signed.crt"
systemctl reload apache2
