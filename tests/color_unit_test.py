#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: color_unit_test.py
@author: Lyndon
@time: 2024/10/29 9:36
@env: Python @desc:
@ref: @blog:
"""
import unittest
import sys
import os

# Add the parent directory of 'utils' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.color_transform_util import ColorTransformUtil


class ColorUnitTest(unittest.TestCase):

    def test_str_rgba_to_hex(self):
        c1, cap1 = ColorTransformUtil.str_rgba_to_hex("rgba(47,153,243,0.4)")
        print("color: ", c1, "capacity: ", cap1)
        c2, cap2 = ColorTransformUtil.str_rgba_to_hex("rgba(0,205,82,0.4)")
        print("color: ", c2, "capacity: ", cap2)
        c3, cap3 = ColorTransformUtil.str_rgba_to_hex("rgba(47,153,243,0.4))")
        print("color: ", c3, "capacity: ", cap3)
