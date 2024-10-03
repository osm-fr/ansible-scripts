#! /bin/bash

set -e

echo "Starting certbot.sh"

sudo certbot certonly -m admin@listes.openstreetmap.fr --agree-tos --non-interactive --expand --webroot -w /data/project/letsencrypt/challenges $(cat hosts-list) 

if [ -e /etc/init.d/nginx ]; then
  sudo systemctl reload nginx

{% if inventory_hostname in groups["cluster-free"] %}
{%   for node in groups["cluster-free"] %}
{%     if node != inventory_hostname %}
#    ssh letsencrypt@{{ node }} sudo /etc/init.d/nginx reload
{%     endif %}
{%   endfor %}
{% elif inventory_hostname in groups["cluster-ovh"] %}
{%   for node in groups["cluster-ovh"] %}
{%     if node != inventory_hostname %}
  ssh letsencrypt@{{ node }} sudo /usr/local/bin/letsencrypt-to-nginx.sh
{%     endif %}
{%   endfor %}
{% endif %}
  echo "nginx was reloaded"
fi

if [ -e /etc/pve/nodes ]; then
  sudo /usr/local/bin/letsencrypt-to-proxmox.sh
fi
if [ -e /etc/pmg/pmg-api.pem ]; then
  sudo /usr/local/bin/letsencrypt-to-proxmox-mail-gateway.sh
fi
