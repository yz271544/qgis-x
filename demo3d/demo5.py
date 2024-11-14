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
from qgis._3d import Qgs3DMapSettings, Qgs3DMapScene, Qgs3DMapCanvas

if __name__ == '__main__':
    # 初始化 QGIS 应用
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 加载 QGIS 项目
    project = QgsProject.instance()
    project.read("/path/to/your/project.qgz")  # 替换为您的项目路径

    # 创建3D地图画布
    canvas = Qgs3DMapCanvas()
    map_settings = Qgs3DMapSettings()
    scene = Qgs3DMapScene(canvas)

    # 设置地图场景
    scene.setMapSettings(map_settings)
    canvas.setMapScene(scene)

    # 进行3D Tiles加载和配置（通过手动操作验证后的图层和配置）
    # 注意，这里您可能需要直接访问项目的图层和场景设置来管理3D Tiles

    # 退出 QGIS
    qgs.exitQgis()
