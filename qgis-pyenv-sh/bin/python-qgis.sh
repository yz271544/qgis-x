#!/bin/bash
source "$(dirname "$0")/o4w_env.sh"

export PATH="$OSGEO4W_ROOT/apps/qgis/bin:$PATH"
export QGIS_PREFIX_PATH="${OSGEO4W_ROOT//\\//}/apps/qgis"
export GDAL_FILENAME_IS_UTF8="YES"
export VSI_CACHE="TRUE"
export VSI_CACHE_SIZE="1000000"
export QT_PLUGIN_PATH="$OSGEO4W_ROOT/apps/qgis/qtplugins:$OSGEO4W_ROOT/apps/qt5/plugins"
export PYTHONPATH="$OSGEO4W_ROOT/apps/qgis/python:$PYTHONPATH"
echo "PATH: $PATH"
echo "PYTHONPATH: $PYTHONPATH"
python "$@"
