#! /bin/bash

export GEM_HOME=`pwd`/taginfo/web/gem

cd taginfo/sources

BUILD=/data/work/taginfo/build
mkdir -p $BUILD/db
mkdir -p $BUILD/log
[ ! -e $BUILD/db/taginfo-db.db ] || sqlite3 $BUILD/db/taginfo-db.db "select 1;"
#rm $BUILD/log/*

./update_all.sh $BUILD

cat `ls -t $BUILD/log/* | head -1` | grep "Done update_all" && exit 0
exit 1
