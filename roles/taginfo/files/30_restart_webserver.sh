#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
rm /data/work/taginfo/data/*.db
cp `find /data/work/taginfo/build -name '*.db'` /data/work/taginfo/data
cp /data/work/taginfo/build/download/* /data/work/taginfo/download

pkill -f taginfo.rb
sleep 2

cd taginfo/web
export GEM_HOME=./gem
./taginfo.rb 4567 2> /data/work/taginfo/server.err > /data/work/taginfo/server.log &
echo "$(date --rfc-3339=s) INFO: ${0} end."
