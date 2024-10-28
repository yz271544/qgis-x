#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo4.py
@author: Lyndon
@time: 2024/10/25 17:51
@env: Python @desc:
@ref: @blog:
"""

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsMarkerSymbol
)
import sys
import os

if __name__ == '__main__':
    # Set QGIS installation path (modify according to your actual installation)
    qgis_path = "D:/iSoft/QGIS-3.38.1"
    QgsApplication.setPrefixPath(qgis_path, True)
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

    # Loading base tile layer with correct type 'raster'
    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    base_layer_name = "Base_Tile-Server"
    base_tile_layer = QgsRasterLayer(base_tile_url, base_layer_name, "raster")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)
    else:
        print("Base Tile layer failed to load! Check the URL and ensure it returns a valid raster image.")

    # Loading additional tile layer
    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    layer_name = "Tile-Server"
    tile_layer = QgsRasterLayer(tile_url, layer_name, "raster")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)
    else:
        print("Tile layer failed to load! Check the URL and ensure it returns a valid raster image.")

    # 创建点图层 (确保与瓦片图层一致的坐标系 EPSG:3857)
    point_layer = QgsVectorLayer("Point?crs=EPSG:3857", "Police Stations", "memory")
    if not point_layer.isValid():
        print("Failed to create point layer")

    # 获取点图层的数据提供者
    point_provider = point_layer.dataProvider()

    # 转换坐标并创建点特征
    features = []
    # 民警站立位置的经纬度
    points = [
        (12958071, 4856091),  # 转换后的坐标
        (12958307, 4856449)
    ]

    for point in points:
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point[0], point[1])))
        features.append(feature)

    # 添加特征到图层
    point_provider.addFeatures(features)
    point_layer.updateExtents()
    project.addMapLayer(point_layer)

    # 设置图层的样式
    symbol = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': 'blue', 'size': '6'})
    point_layer.renderer().setSymbol(symbol)

    # 保存项目到 .qgs 或 .qgz 文件
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo4.qgz")

    # Exit QGIS application
    qgis.exitQgis()
