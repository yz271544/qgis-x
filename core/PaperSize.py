#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: PaperSize.py
@author: Lyndon
@time: 2024/10/30 9:35
@env: Python @desc:
@ref: @blog:
"""

from enum import Enum

class PaperSpecification(Enum):
    """
    Paper size specification
    Unit: mm
    (x, y) -> width, height 横向打印需要交换宽高
    """
    A3 = (297, 420)
    A4 = (210, 297)
    A5 = (148, 210)
    B4 = (250, 353)
    B5 = (176, 250)
    Letter = (216, 279)
    Legal = (216, 356)
    Executive = (184, 267)
    Folio = (210, 330)
    Custom = (0, 0)

    def get_name(self) -> str:
        return self.name
