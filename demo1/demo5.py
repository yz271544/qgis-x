#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo5.py
@author: Lyndon
@time: 2024/10/28 11:27
@env: Python @desc:
@ref: @blog:
"""
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsField,
    QgsRasterLayer,
    QgsPointXY,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMarkerSymbol,
    QgsRasterMarkerSymbolLayer,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext
)

from qgis.PyQt.QtCore import QVariant, QMetaType
import sys
import os

if __name__ == '__main__':
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

    # 加载瓦片图层
    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    base_tile_layer = QgsRasterLayer(base_tile_url, "Base_Tile-Server", "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)

    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    tile_layer = QgsRasterLayer(tile_url, "Tile-Server", "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)

    # 创建矢量图层
    shapefile_path = "/common/output/projects/Transformed_Points.shp"
    pointLayer = QgsVectorLayer("Point?crs=EPSG:3857", "Transformed_Points", "ogr")
    pointProvider = pointLayer.dataProvider()
    pointProvider.addAttributes([QgsField("name", QMetaType.Type(QVariant.String)), QgsField("x", QMetaType.Type(QVariant.Int)), QgsField("y", QMetaType.Type(QVariant.Int))])
    pointLayer.updateFields()

    # 设置标记符号为栅格图像类型
    symbol = QgsMarkerSymbol()
    icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    raster_layer.setSize(10)
    symbol.changeSymbolLayer(0, raster_layer)

    # Ensure the renderer is valid before setting the symbol
    # renderer = pointLayer.renderer()
    # if renderer is not None:
    #     renderer.setSymbol(symbol)
    # else:
    #     print("Failed to get the renderer for the layer!")
    #     sys.exit(1)

    # 设置坐标转换
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())

    # Start editing the vector layer
    pointLayer.startEditing()

    # 转换并添加点
    points = [QgsPointXY(111.4775222, 40.7290133), QgsPointXY(111.4766598, 40.7282033)]
    for i, point in enumerate(points):
        transformed_point = transformer.transform(point)
        feature = QgsFeature(pointLayer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(transformed_point))
        print(f"mingjing-Point{i + 1}", transformed_point.x(), transformed_point.y())
        feature.setAttributes([f"mingjing-Point{i + 1}", int(transformed_point.x()), int(transformed_point.y())])
        pointProvider.addFeature(feature)


    # 持久化图层数据到 shapefile
    layer_output_path = "/common/output/projects/Transformed_Points.shp"
    # error = QgsVectorFileWriter.writeAsVectorFormat(pointLayer, layer_output_path, "UTF-8", pointLayer.crs(),
    #                                                 "ESRI Shapefile")

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    # options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"

    error = QgsVectorFileWriter.writeAsVectorFormatV3(pointLayer, layer_output_path, QgsCoordinateTransformContext(), options)
    if error == QgsVectorFileWriter.NoError:
        print("图层数据已成功保存到", layer_output_path)
    else:
        print("保存图层数据时出错：", error)


    if pointLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + pointProvider.error().message())


    # 添加矢量图层到项目
    project.addMapLayer(pointLayer)

    # 保存项目
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo5.qgz")

    # Exit QGIS application
    qgis.exitQgis()
