#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=`getApplication`

# 1. clean old results
./clean.sh
rm log.*
# 2. generate mesh using blockMesh
blockMesh

topoSet
setFields

# . snappy
#snappyHexMesh -overwrite
# 5. run

# runApplication $application
runApplication decomposePar
runParallel $application
runApplication reconstructPar
