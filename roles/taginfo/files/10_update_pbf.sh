#! /bin/bash

echo "$(date --rfc-3339=s) INFO: ${0} start ..."
echo "$(date --rfc-3339=s) INFO: ${0} pbf avant maj"
SOURCE_OSM_FILE="/data/work/taginfo/data/france.osm.pbf"
ls -l $SOURCE_OSM_FILE
WORKDIR=/data/work/taginfo/
OSMOSIS=/data/project/taginfo/osmosis/bin/osmosis
#OSMOSIS=/usr/bin/osmosis

CURDATE="`date +%F-%R`"

LOCKFILE="$WORKDIR/osmosis/lock-osmosis-maj"
CHANGEFILE="$WORKDIR/osmosis/change-${CURDATE}.osc.gz"
TARGET_OSM_FILE="$WORKDIR/osmosis/france-${CURDATE}.osm.pbf"
POLYGON="$HOME/france.poly"

if [ -e "$LOCKFILE" ]; then
  echo "Lock file $LOCKFILE still present - aborting update"
  exit 1
fi

touch $LOCKFILE

cd $WORKDIR/osmosis

echo "$(date --rfc-3339=s) INFO: *** Get changes from server"
cp "$WORKDIR/osmosis/state.txt" "$WORKDIR/osmosis/state.txt.old"
$OSMOSIS --read-replication-interval workingDirectory="$WORKDIR/osmosis" --simplify-change --write-xml-change "$CHANGEFILE"
if [ $? -ne 0 ]; then
  cp "$WORKDIR/osmosis/state.txt.old" "$WORKDIR/osmosis/state.txt"
  rm $LOCKFILE
  exit 1
fi

ls -l "$CHANGEFILE"

echo "$(date --rfc-3339=s) INFO: *** Update $SOURCE_OSM_FILE"
#$OSMOSIS --read-xml-change "$CHANGEFILE" --read-pbf "$SOURCE_OSM_FILE" --apply-change --buffer --bounding-polygon file="$POLYGON" --buffer --write-pbf file="$TARGET_OSM_FILE"
$OSMOSIS --read-xml-change "$CHANGEFILE" --read-pbf "$SOURCE_OSM_FILE" --apply-change --buffer --buffer --write-pbf file="$TARGET_OSM_FILE"
if [ $? -ne 0 ]; then
  cp "$WORKDIR/osmosis/state.txt.old" "$WORKDIR/osmosis/state.txt"
  rm $LOCKFILE
  exit 1
fi

rm "$SOURCE_OSM_FILE"
ln "$TARGET_OSM_FILE" "$SOURCE_OSM_FILE"

rm "$TARGET_OSM_FILE"
rm "$CHANGEFILE"

rm $LOCKFILE
echo "$(date --rfc-3339=s) INFO: ${0} pbf apres maj"
ls -l $SOURCE_OSM_FILE
echo "$(date --rfc-3339=s) INFO: ${0} end."
