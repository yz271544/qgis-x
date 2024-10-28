#!/bin/bash
cd "$(dirname "$0")/.."
export OSGEO4W_ROOT=$(pwd)
export PATH="$OSGEO4W_ROOT/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
for file in "$OSGEO4W_ROOT/etc/ini/"*.sh; do
    source "$file"
done
