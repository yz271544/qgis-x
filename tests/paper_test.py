#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: serilizer_test.py
@author: Lyndon
@time: 2024/10/29 12:13
@env: Python @desc:
@ref: @blog:
"""

import json
import unittest

from core.PaperSize import PaperSpecification
from utils.unit_util import UnitUtil


class PaperTest(unittest.TestCase):

    def test_paper_a4(self):
        UnitUtil.mm_to_inch(PaperSpecification.A4.value[0])
