#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: color_transform_util.py
@author: Lyndon
@time: 2024/10/29 9:33
@env: Python @desc:
@ref: @blog:
"""


class ColorTransformUtil:

    @staticmethod
    def str_rgba_to_hex(rgba: str) -> (str, float):
        """
        :param rgba: rgba(47,153,243,0.4)
        :return: #2f99f3
        """
        rgba = rgba.replace('rgba(', '').replace(')', '')
        rgba = rgba.split(',')
        rgb = tuple(map(int, rgba[:3]))
        capacity = rgba[3]
        return ColorTransformUtil.rgb_to_hex(rgb), capacity

    @staticmethod
    def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
        return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))




