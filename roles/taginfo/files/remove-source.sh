#!/bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."

echo "$(date --rfc-3339=s) DEBUG: arg ${*}"
[ -z "${1}" ] && echo "$(date --rfc-3339=s) ERROR: ${0} <file>" && exit 1
[ ! -f "${1}" ] && echo "$(date --rfc-3339=s) ERROR: fichier ${1} illisible" && exit 2
[ ! -f /data/work/$USER/out-key.txt ] && echo "$(date --rfc-3339=s) ERROR: fichier /data/work/$USER/out-key.txt illisible" && exit 3
[ ! -f /data/project/$USER/key-source-valide.txt ] && echo "$(date --rfc-3339=s) ERROR: fichier /data/project/$USER/key-source-valide.txt illisible" && exit 4

Nbr=$(cat /data/work/$USER/out-key.txt | awk '{ print $2 }' | grep -i source | egrep -vf /data/project/$USER/key-source-valide.txt | egrep -v '( |"|=)' | wc -l)
echo "$(date --rfc-3339=s) DEBUG: il y a $Nbr ligne(s) source (hormis exeption) dans le /data/work/$USER/out-key.txt"

[ $Nbr -gt 0 ] || { echo "$(date --rfc-3339=s) WARNING: nombre de clef source egale a 0, rien a faire" && exit 0 ; }

# purge limité a 1000 clefs par execution pour éviter le debordement en arg lors de la 1ere execution
./osmfilter ${1} --drop-tags="$(for key in $(cat /data/work/$USER/out-key.txt | awk '{ print $2 }' | grep -i source | egrep -vf /data/work/$USER/key-source-valide.txt | egrep -v '( |"|=)' | head -n 1000); do echo -n "$key= "; done | sed "s/ $//")" -o=tmp.$(basename ${0} .sh).o5m ; mv -f tmp.$(basename ${0} .sh).o5m ${1}

echo "$(date --rfc-3339=s) INFO: ${0} end."
