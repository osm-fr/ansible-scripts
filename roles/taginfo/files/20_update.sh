#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
export GEM_HOME=`pwd`/taginfo/web/gem

cd taginfo/sources || { echo "$(date --rfc-3339=s) ERROR: cd taginfo/sources" ; exit 1 ;}

BUILD=/data/work/taginfo/build
if [ -d $BUILD/db ]; then
 echo "$(date --rfc-3339=s) DEBUG: $BUILD/db existe. rien a faire" >/dev/null
else
 echo "$(date --rfc-3339=s) ERROR: $BUILD/db n'existe pas. a creer"
 mkdir -p $BUILD/db || { echo "$(date --rfc-3339=s) ERROR: mkdir -p $BUILD/db" ; exit 1 ;}
fi
mkdir -p $BUILD/log || { echo "$(date --rfc-3339=s) ERROR: mkdir -p $BUILD/log" ; exit 1 ;}
if [ ! -e $BUILD/db/taginfo-db.db ]; then
 echo "$(date --rfc-3339=s) DEBUG: $BUILD/db/taginfo-db.db n'existe pas. rien a faire" #>/dev/null
else
 echo "$(date --rfc-3339=s) INFO: $BUILD/db/taginfo-db.db existe. test sqlite3"
 sqlite3 $BUILD/db/taginfo-db.db "select 1;" || {  echo "$(date --rfc-3339=s) ERROR: test sqlite3" ; exit 1 ; }
fi
#rm $BUILD/log/*

[ -x ./update_all.sh ] || { echo "$(date --rfc-3339=s) ERROR: /update_all.sh non executable" ; exit 1 ;}
echo "$(date --rfc-3339=s) DEBUG: before update_all.sh" #>/dev/null
./update_all.sh $BUILD || { echo "$(date --rfc-3339=s) ERROR: ./update_all.sh $BUILD" ; echo "5 dernièrs lignes du log $(ls -t $BUILD/log/* | head -1)" ; tail -n 5 $(ls -t $BUILD/log/* | head -1) ; exit 1 ;}
echo "$(date --rfc-3339=s) DEBUG: after update_all.sh" #>/dev/null

cat `ls -t $BUILD/log/* | head -1` | grep "Done update_all" && echo "$(date --rfc-3339=s) INFO: ${0} end." && exit 0
echo "$(date --rfc-3339=s) ERROR: ${0} Done update_all non trouvé dans $(ls -t $BUILD/log/* | head -1)"
echo "5 dernièrs lignes du log $(ls -t $BUILD/log/* | head -1)"
tail -n 5 $(ls -t $BUILD/log/* | head -1) 
exit 1
