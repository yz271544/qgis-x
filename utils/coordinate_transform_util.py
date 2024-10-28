#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: coordinate_transform_util.py
@author: Lyndon
@time: 2024/10/28 10:33
@env: Python @desc:
@ref: @blog:
"""


from qgis.core import QgsPointXY
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject


class CoordinateTransformUtil:
    @staticmethod
    def transform_point(point_4326: QgsPointXY, crs_4326: QgsCoordinateReferenceSystem, crs_3857: QgsCoordinateReferenceSystem) -> QgsPointXY:
        # 创建坐标转换器
        transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())
        # 转换到 EPSG:3857
        point_3857 = transformer.transform(point_4326)
        return point_3857

    @staticmethod
    def transform_points(points_4326: list[QgsPointXY], crs_4326: QgsCoordinateReferenceSystem, crs_3857: QgsCoordinateReferenceSystem) -> list[QgsPointXY]:
        # 创建坐标转换器
        transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())
        # 转换到 EPSG:3857
        points_3857 = []
        for e in points_4326:
            points_3857.append(transformer.transform(e))
        return points_3857
