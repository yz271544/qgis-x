#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: qt_font.py
@author: Lyndon
@time: 2024/11/5 15:54
@env: Python @desc:
@ref: @blog:
"""

from qgis.PyQt import QtGui
from qgis.core import Qgis, QgsTextFormat


class QtFontUtil:
    @staticmethod
    def create_font(font_family: str, font_size: int, font_color: str,
                    is_bold: bool = False, is_italic :bool = False,
                    orientation: Qgis.TextOrientation = Qgis.TextOrientation.Horizontal,
                    spacing: float = 0.0):
        text_format = QgsTextFormat() # 创建文本格式
        font = text_format.font() # 获取字体
        text_format.allowHtmlFormatting() # 允许html格式
        font.setFamily(font_family) # 设置字体名称
        font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, spacing)  # 设置字体间距
        text_format.setFont(font) # 设置字体
        text_format.setColor(QtGui.QColor(font_color))  # 设置字体颜色
        text_format.setForcedBold(is_bold)  # 设置是否加粗
        text_format.setForcedItalic(is_italic) # 设置是否斜体
        text_format.setOrientation(orientation) # 设置文字方向
        text_format.setSizeUnit(Qgis.RenderUnit.Points) # 设置字体大小单位
        text_format.setSize(font_size) # 设置字体大小
        # text_css = text_format.asCSS()
        # print(f"create_font:{text_css}")
        return text_format



