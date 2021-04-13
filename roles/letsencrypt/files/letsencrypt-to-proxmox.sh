#! /bin/bash

domains=$(openssl x509 -text < /data/project/letsencrypt/keys/chained.pem | grep DNS:)

for node in $(ls /etc/pve/nodes); do
  echo $node
  if [[ "$domains" == *"$node"* ]]; then
    cp /data/project/letsencrypt/keys/domain.key  "/etc/pve/nodes/$node/pveproxy-ssl.key"
    cp /data/project/letsencrypt/keys/chained.pem "/etc/pve/nodes/$node/pveproxy-ssl.pem"
    sudo -u letsencrypt ssh letsencrypt@$node.openstreetmap.fr sudo systemctl reload pveproxy
  else
    echo "  - skipped"
  fi
done
