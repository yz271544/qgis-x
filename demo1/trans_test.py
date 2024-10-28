#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: trans_test.py
@author: Lyndon
@time: 2024/10/28 10:23
@env: Python @desc:
@ref: @blog:
"""
from qgis.core import QgsPointXY
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject


import unittest


class TestTrans(unittest.TestCase):

    def test_trans(self):
        # 定义源和目标坐标系
        crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84
        crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")  # Web Mercator

        # 创建坐标转换器
        transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())

        # 定义源坐标 (EPSG:4326)
        point_4326 = QgsPointXY(116.4073963, 39.9041999)  # 北京

        # 转换到 EPSG:3857
        point_3857 = transformer.transform(point_4326)

        print(f"原始坐标 (EPSG:4326): {point_4326}")
        print(f"转换后坐标 (EPSG:3857): {point_3857}")


    def test_trans2(self):
        # 定义源和目标坐标系
        crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84
        crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")  # Web Mercator

        # 创建坐标转换器
        transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())

        # 定义源坐标 (EPSG:4326)
        points_4326 = [QgsPointXY(111.4775222, 40.7290133),  #
              QgsPointXY(111.4766598, 40.7282033) ]

        # 转换到 EPSG:3857
        points_3857 = []
        for e in points_4326:
            points_3857.append(transformer.transform(e))

        for point_4326, point_3857 in zip(points_4326, points_3857):
            print(f"原始坐标 (EPSG:4326): {point_4326}")
            print(f"转换后坐标 (EPSG:3857): {point_3857}")

