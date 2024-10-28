from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsField,
    QgsRasterLayer,
    QgsPointXY,
    QgsMarkerSymbol,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsSvgMarkerSymbolLayer,
    QgsRasterMarkerSymbolLayer,
    QgsPointClusterRenderer
)

from qgis.PyQt.QtCore import QVariant

import sys
import os

if __name__ == '__main__':
    # Set QGIS installation path (modify according to your actual installation)
    # qgis_path = "D:/iSoft/QGIS-3.38.1"
    # Initialize QGIS application
    # QgsApplication.setPrefixPath(qgis_path, True)
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project: QgsProject = QgsProject.instance()

    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    # Layer name
    base_layer_name = "Base_Tile-Server"
    # Create and load tile layer
    base_tile_layer = QgsRasterLayer(base_tile_url, base_layer_name, "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)
    else:
        print("Base Tile layer failed to load! Error:", base_tile_layer.error().message())
        print("Check the URL and ensure it returns a valid raster image.")

    # Tile service URL
    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    # Layer name
    layer_name = "Tile-Server"
    # Create and load tile layer
    tile_layer = QgsRasterLayer(tile_url, layer_name, "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)
    else:
        print("Tile layer failed to load! Error:", tile_layer.error().message())
        print("Check the URL and ensure it returns a valid raster image.")

    # layRenderer = tile_layer.renderer()
    #
    # pointClusterRenderer = QgsPointClusterRenderer.convertFromRenderer(layRenderer)



    # 创建矢量图层 用于存储标记点的矢量图层
    pointLayer = QgsVectorLayer("Point?crs=EPSG:3857", "Transformed_Points", "memory")
    pointProvider = pointLayer.dataProvider()

    # 添加字段
    pointProvider.addAttributes([QgsField("name", QVariant.String)])
    pointLayer.updateFields()

    # 添加点
    points = [QgsPointXY(111.4775222, 40.7290133),  #
              QgsPointXY(111.4766598, 40.7282033)]  #

    for i, point in enumerate(points):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        feature.setAttributes([f"Point {i + 1}"])
        pointProvider.addFeature(feature)

    pointLayer.updateExtents()



    # #
    # # # 设置标记符号为栅格图像类型
    # symbol = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'red'})
    # icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    # raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    # raster_layer.setSize(10)
    # symbol.changeSymbolLayer(0, raster_layer)
    #
    # # 创建点聚类渲染器
    # cluster_renderer = QgsPointClusterRenderer()
    # cluster_renderer.setClusterSymbol(symbol)
    # pointLayer.setRenderer(cluster_renderer)
    #
    # # 坐标转换与标记点添加
    # # 原始经纬度坐标（示例）
    # latitude1 = 40.7290133
    # longitude1 = 111.4775222
    # latitude2 = 40.7282033
    # longitude2 = 111.4766598
    #
    # # 创建原始坐标点
    # point1_original = QgsPointXY(longitude1, latitude1)
    # point2_original = QgsPointXY(longitude2, latitude2)
    #
    # # 定义原始坐标系统（经纬度，这里假设为EPSG:4326）
    # source_crs = QgsCoordinateReferenceSystem("EPSG:4326")
    # # 定义目标坐标系统（EPSG:3857）
    # target_crs = QgsCoordinateReferenceSystem("EPSG:3857")
    #
    # # 创建坐标转换对象
    # transform = QgsCoordinateTransform(source_crs, target_crs, project)
    #
    # # 转换坐标
    # point1_transformed = transform.transform(point1_original)
    # point2_transformed = transform.transform(point2_original)
    #
    # # 创建要素并添加到图层
    # feature1 = QgsFeature()
    # feature1.setGeometry(QgsGeometry.fromPointXY(point1_transformed))
    # feature2 = QgsFeature()
    # feature2.setGeometry(QgsGeometry.fromPointXY(point2_transformed))
    # pointProvider.addFeatures([feature1, feature2])
    #
    # 将图层添加到项目
    project.addMapLayer(pointLayer)
    #
    # # 获取标记点矢量图层
    # pointLayer = project.mapLayersByName("Transformed_Points")[0]
    # # 获取图层的范围
    # extent = pointLayer.extent()

    # viewSets = project.viewSettings()
    # print(viewSets)
    #
    #
    # # 设置合适的比例尺
    # scale = 100000  # 根据需要调整比例尺
    # project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    # project.setMapScales(scale)

    # 保存项目到 .qgs 或 .qgz 文件
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo3.qgz")

    # Exit QGIS application
    qgis.exitQgis()
