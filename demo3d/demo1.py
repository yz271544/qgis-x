#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo1.py
@author: Lyndon
@time: 2024/11/13 12:31
@env: Python @desc:
@ref: @blog:
"""
from qgis._3d import Qgs3DMapScene
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsProject,
    QgsField,
    QgsRasterLayer,
    QgsVectorTileLayer,
    QgsPointXY,
    QgsVectorLayer,
    QgsFeature,
    QgsSymbol,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMarkerSymbol,
    QgsFillSymbol,
    QgsRasterMarkerSymbolLayer,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateTransformContext,
    QgsSingleSymbolRenderer,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer,
    QgsPrintLayout,
    QgsLayoutPageCollection,
    QgsLayoutItemMap,
    QgsLayoutItemLegend,
    QgsLayoutItemLabel,
    QgsRectangle,
    QgsReadWriteContext,
    QgsMargins,
    QgsTextFormat,
    QgsMapSettings,
    QgsLayoutAligner,
    QgsLayoutMeasurement,
    QgsUnitTypes,
    QgsLayoutSize,
    QgsLayoutItem,
    QgsLayerTreeLayer,
    QgsLayoutItemShape,
    QgsLayoutItemGroup,
    QgsRuleBasedRenderer,
    QgsLayoutExporter,

)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge

GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/project3d'

if __name__ == '__main__':
    # 初始化QGIS应用程序
    qgis = QgsApplication([], False)
    qgis.initQgis()
    # 创建QGIS项目并设置地图画布
    # Create project instance
    project = QgsProject.instance()

    canvas = QgsMapCanvas()
    bridge = QgsLayerTreeMapCanvasBridge(project.layerTreeRoot(), canvas)

    # 添加3D Tiles数据源
    uri = "type=3dtiles&url=http://172.31.100.34:38083/map/qxmx/jkg/tileset.json"
    # uri = "type=3dtiles&url=http://172.31.100.34:38083/map/terrain/layer.json"
    # uri = "type=3dtiles&url=http://172.31.100.34:38083/map/terrain/meta.json"
    layer = QgsVectorTileLayer(uri, "3DTilesLayer")
    if not layer.isValid():
        print("Layer failed to load!", layer.error())
    else:
        project.addMapLayer(layer)

    # 保存项目文件
    # Save project
    project.write(f"{GEOJSON_PREFIX}/d3demo1.qgz")

    # Exit QGIS application
    qgis.exitQgis()


