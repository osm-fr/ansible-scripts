#! /bin/bash

cat /data/project/letsencrypt/keys/domain.key /data/project/letsencrypt/keys/signed.crt > /etc/pmg/pmg-api.pem

systemctl restart pmgproxy
