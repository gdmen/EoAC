#!/bin/bash

# build
BIN="../dist/linux"
TEST="../ac_client"
zip $BIN/jerboa.zip *.py
cat $BIN/bundle.sh $BIN/jerboa.zip > $BIN/jerboa

# cleanup
rm $BIN/jerboa.zip

# run
    cp autoexec.cfg $TEST/config/autoexec.cfg
    cp $BIN/jerboa $TEST/jerboa
    mkdir -p $TEST/jerboa_logs/past
    logfiles=$(ls $TEST/jerboa_logs/*.txt 2> /dev/null | wc -l)
    [ "$logfiles" == "0" ] || mv $TEST/jerboa_logs/*.txt $TEST/jerboa_logs/past
if ! $1 ; then
    cd $TEST
    ./jerboa
fi
