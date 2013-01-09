#!/bin/sh
PYTHON=$(which python 2>/dev/null)
if [ ! -x "$PYTHON" ] ; then
    echo "Python not found!"
    exit 1
fi
exec $PYTHON -c "
import sys, os
sys.path.insert(0, sys.argv[1])
del sys.argv[0:1]
import jerboa
jerboa.main()
" $0 $@
