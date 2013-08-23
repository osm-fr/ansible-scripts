#! /bin/bash

rm /data/work/taginfo/data/*.db
cp `find /data/work/taginfo/build -name '*.db'` /data/work/taginfo/data
cp /data/work/taginfo/build/download/* /data/work/taginfo/download

pkill taginfo.rb
sleep 2

cd taginfo/web
export GEM_HOME=./gem
./taginfo.rb 4567 2> /data/work/taginfo/server.err > /data/work/taginfo/server.log &
