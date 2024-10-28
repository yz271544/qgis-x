#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo1.py
@author: Lyndon
@time: 2024/10/24 15:57
@env: Python @desc:
@ref: @blog:
"""

from qgis.core import QgsProject, QgsVectorLayer

# 初始化 QGIS 应用程序
from qgis.core import QgsApplication

if __name__ == '__main__':
    QgsApplication.setPrefixPath("/usr", True)  # 设置 QGIS 路径，适用于 Linux，Windows 系统需要调整路径
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 创建一个 QGIS 项目
    project = QgsProject.instance()

    # 创建并添加图层
    layer = QgsVectorLayer("D:/iProject/pypath/qgis-x/output/projects/shapefile.shp", "LayerName", "ogr")
    if not layer.isValid():
        print("Layer failed to load!")
    else:
        print("Layer loaded successfully!")

    # 将图层添加到项目
    project.addMapLayer(layer)

    # 保存项目到 .qgs 或 .qgz 文件
    project.write("D:/iProject/pypath/qgis-x/output/projects//project.qgz")

    # 退出 QGIS 应用程序
    qgs.exitQgis()
