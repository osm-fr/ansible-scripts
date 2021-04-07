#!/bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
if [ -d taginfo-tools ]; then
 cd taginfo-tools/ || { echo "$(date --rfc-3339=s) ERROR: cd "; exit 1;}
 git fetch || { echo "$(date --rfc-3339=s) ERROR: git fetch"; exit 2;}
 git rebase origin/master || { echo "$(date --rfc-3339=s) ERROR: git rebase"; exit 3;}
else
 git clone https://github.com/taginfo/taginfo-tools.git || { echo "$(date --rfc-3339=s) ERROR: git clone"; exit 4;}
 cd taginfo-tools/ || { echo "$(date --rfc-3339=s) ERROR: cd "; exit 1;}
fi
git submodule update --init || { echo "$(date --rfc-3339=s) ERROR: git submodule update"; exit 5;}
mkdir -p build || { echo "$(date --rfc-3339=s) ERROR: mkdir"; exit 6;}
cd build
cmake .. || { echo "$(date --rfc-3339=s) ERROR: cmake"; exit 7;}
make || { echo "$(date --rfc-3339=s) ERROR: make"; exit 8;}

cd ../../taginfo/
timestamp=$(date --utc +%Y-%m-%d-%H-%M-%S)
git checkout -b master-$timestamp || { echo "$(date --rfc-3339=s) ERROR: checkout -b"; exit 9;}
git checkout master || { echo "$(date --rfc-3339=s) ERROR: checkout master"; exit 10;}
git fetch || { echo "$(date --rfc-3339=s) ERROR: fetch"; exit 11;}
git stash || { echo "$(date --rfc-3339=s) ERROR: stash"; exit 12;}
git rebase origin/master || { echo "$(date --rfc-3339=s) ERROR: rebase"; exit 13;}

cd ~/bin
cp -p ../taginfo-tools/build/src/taginfo-* . || { echo "$(date --rfc-3339=s) ERROR: cp"; exit 14;}
cd ..

cp -p taginfo-config.json taginfo-config.json-$timestamp || { echo "$(date --rfc-3339=s) ERROR: cp2"; exit 15;}
colordiff -u taginfo-config.json taginfo/taginfo-config-example.json | less -R
vi taginfo-config.json

./20_update.sh || { echo "$(date --rfc-3339=s) ERROR: 20_update.sh"; exit 16;}
./30_restart_webserver.sh || { echo "$(date --rfc-3339=s) ERROR: 30_restart_webserver.sh"; exit 17;}
echo "$(date --rfc-3339=s) INFO: ${0} end."
