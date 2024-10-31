#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: unit_util.py
@author: Lyndon
@time: 2024/10/30 9:07
@env: Python @desc:
@ref: @blog:
"""


class UnitUtil:

    # constant coefficient
    INCH_TO_CM = 2.54
    INCH_TO_MM = 25.4

    # inch to cm
    @staticmethod
    def inch_to_cm(inch):
        return inch * UnitUtil.INCH_TO_CM

    # inch to mm
    @staticmethod
    def inch_to_mm(inch):
        return inch * UnitUtil.INCH_TO_MM

    # cm to inch
    @staticmethod
    def cm_to_inch(cm):
        return cm / UnitUtil.INCH_TO_CM

    # mm to inch
    @staticmethod
    def mm_to_inch(mm):
        return mm / UnitUtil.INCH_TO_MM