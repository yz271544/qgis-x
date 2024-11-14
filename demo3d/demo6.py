#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo4.py
@author: Lyndon
@time: 2024/11/13 14:43
@env: Python @desc:
@ref: @blog:
"""
from qgis._gui import QgsMapCanvas
# from qgis._3d_p import QgsTiledSceneLayer3DRenderer
from qgis.core import QgsTiledSceneLayer, QgsCoordinateReferenceSystem, QgsRectangle
from qgis.core import QgsApplication, QgsProject, QgsVector3D
from qgis._3d import Qgs3DMapSettings, Qgs3DMapScene, Qgs3DMapCanvas, QgsTiledSceneLayer3DRenderer


GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/project3d'


if __name__ == '__main__':
    from qgis.core import QgsApplication, QgsProject
    from qgis._3d import Qgs3DMapCanvas, Qgs3DMapSettings

    # 初始化 QGIS 应用
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 创建 QGIS 项目
    project = QgsProject.instance()
    # project.read("/path/to/your/project.qgz")  # 替换为您的项目路径，如果没有项目路径可选新建
    crs = QgsCoordinateReferenceSystem("EPSG:3857")
    project.setCrs(crs)

    # url = "http://172.31.100.34:38083/map/qxmx/jkg/tileset.json"
    url = "url=http://172.31.100.34:38083/map/qxmx/jkg/tileset.json&http-header:referer="
    tsl = QgsTiledSceneLayer(url, "qmtest", "cesiumtiles")
    tsl.setRenderer3D(QgsTiledSceneLayer3DRenderer())
    project.addMapLayer(tsl)

    # 创建2D地图画布
    canvas2d = QgsMapCanvas()
    canvas2d.setDestinationCrs(crs)
    # 创建3D地图画布
    canvas3d = Qgs3DMapCanvas()
    map_settings_3d = Qgs3DMapSettings()

    # # 配置3D地图设置
    # map_settings.setOrigin(QgsVector3D(0, 0, 0))  # 根据需要设置地图的原点或其他设置
    #
    # # 应用设置到3D画布
    extent = QgsRectangle()

    project_layers = project.mapLayers().values()
    for layer in project_layers:
        extent.combineExtentWith(layer.extent())

    # Set the map canvas extent to the combined extent
    project.setCrs(crs)
    map_settings_3d.setExtent(extent)
    canvas2d.setExtent(extent)
    canvas2d.refresh()

    project.write(f"{GEOJSON_PREFIX}/d3demo6.qgz")
    # 如果您需要进一步添加图层和配置3D Tiles，可以通过设置`map_settings`对象

    # 退出 QGIS
    qgs.exitQgis()
