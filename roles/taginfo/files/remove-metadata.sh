#!/bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
Input=data/france.osm.pbf
if [ -f france.o5m ]; then
  echo "$(date --rfc-3339=s) WARNING: fichier o5m deja present"
else
  echo "$(date --rfc-3339=s) INFO: conversion o5m"
  ./osmconvert $Input -o=france.o5m
fi
if [ -f /data/work/$USER/out-key.txt ]; then
 echo "$(date --rfc-3339=s) INFO: liste de clef avant traitement deja present"
 #true # pas de debug
else
 echo "$(date --rfc-3339=s) INFO: liste de clef avant traitement"
 ./osmfilter france.o5m --out-count > /data/work/$USER/out-key.txt
 wc -l /data/work/$USER/out-key.txt
fi

# pernet a titre de debug de lister la valeur des sources avant purge
#[ -f /data/work/$USER/out-key-source.txt ] || ./osmfilter france.o5m --out-count=source > /data/work/$USER/out-key-source.txt

#echo "$(date --rfc-3339=s) INFO: change_source-maxspeed_into_maxspeed-type"
#./change_source-maxspeed_into_maxspeed-type.sh france.o5m

./remove-source.sh france.o5m || echo error remove-source-sh

echo "$(date --rfc-3339=s) INFO: liste de clef apres traitement"
./osmfilter france.o5m --out-count > /data/work/$USER/out-key-new.txt
wc -l /data/work/$USER/out-key-new.txt

echo "$(date --rfc-3339=s) INFO: diff"
diff /data/work/$USER/out-key.txt /data/work/$USER/out-key-new.txt

echo "$(date --rfc-3339=s) INFO: conversion pbf"
./osmconvert france.o5m -o=$Input ; rm -f france.o5m

echo "$(date --rfc-3339=s) INFO: ${0} end."
