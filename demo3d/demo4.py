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


from qgis.core import QgsApplication, QgsProject
from qgis._3d import Qgs3DMapCanvas, Qgs3DMapScene, Qgs3DMapSettings, Qgs3DLayer

if __name__ == '__main__':

    # 初始化 QGIS 应用
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 创建 QGIS 项目
    project = QgsProject.instance()

    # 创建3D地图画布
    canvas = Qgs3DMapCanvas()
    map_settings = Qgs3DMapSettings()
    scene = Qgs3DMapScene(canvas)

    # 添加3D Tiles图层 - 需要确保使用的是正确的3D支持类型
    uri = "3dtiles://http://172.31.100.34:38083/map/qxmx/jkg/tileset.json"  # 替换为您的3D Tiles URL
    layer = Qgs3DLayer(uri, "3D Tiles Layer")  # 注意：Qgs3DLayer示例

    if not layer.isValid():
        print("3D Tiles Layer failed to load!")
    else:
        map_settings.addLayer(layer)
        scene.setMapSettings(map_settings)
        canvas.setMapScene(scene)

    # 保存项目
    project.write("/path/to/your/project.qgz")

    # 退出 QGIS
    qgs.exitQgis()
