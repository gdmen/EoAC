#!/bin/bash

# build
NAME="eoac"
LOGDIR="EoAC_logs"
BIN="../dist/linux"
WIN_DIST="../dist/win/dist/"$NAME".exe"
DIST="../../jerboa_website/downloads"
TEST="../ac_client"
zip $BIN/jerboa.zip *.py
cat $BIN/bundle.sh $BIN/jerboa.zip > $BIN/$NAME
cp $BIN/$NAME $DIST/$NAME
cp $WIN_DIST $DIST

# cleanup
rm $BIN/jerboa.zip

# run
    cp autoexec.cfg $TEST/config/autoexec.cfg
    cp $BIN/$NAME $TEST/$NAME
    mkdir -p $TEST/$LOGDIR/past
    logfiles=$(ls $TEST/$LOGDIR/*.txt 2> /dev/null | wc -l)
    [ "$logfiles" == "0" ] || mv $TEST/$LOGDIR/*.txt $TEST/$LOGDIR/past
if ! $1 ; then
    cd $TEST
    ./$NAME -d
fi
