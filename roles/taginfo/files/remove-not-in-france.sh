#!/bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
echo "$(date --rfc-3339=s) INFO: conversion o5m"
[ -f france.o5m ] || osmconvert data/france.osm.pbf -o=france.o5m
echo "$(date --rfc-3339=s) INFO: osmfilter drop-relations"
# il n'est pas tres clair comment fonctionne le or avec des valeurs multiple. pour le moment je met une valeur par ligne
osmfilter france.o5m --drop-relations="@id=6900538 or type=network" -o=new.o5m && mv -f new.o5m france.o5m
osmfilter france.o5m --drop-relations="@id=52411 or type=collection" -o=new.o5m && mv -f new.o5m france.o5m
echo "$(date --rfc-3339=s) INFO: conversion pbf"
osmconvert france.o5m -o=data/france.osm.pbf ; rm -f france.o5m
echo "$(date --rfc-3339=s) INFO: ${0} end."
