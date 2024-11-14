#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo3.py
@author: Lyndon
@time: 2024/11/13 14:26
@env: Python @desc:
@ref: @blog:
"""

import sys
from qgis.core import QgsApplication, QgsProject
from qgis._3d import Qgs3DMapSettings, Qgs3DMapScene, Qgs3DMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout


# Create a QWidget to hold the 3D map canvas
class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.canvas = Qgs3DMapCanvas()

        # Create a container widget
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.cav(self.canvas)

        # Set the layout for the main widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)


if __name__ == '__main__':

    # Initialize QGIS Application
    # QgsApplication.setPrefixPath("/path/to/qgis", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Create a Qt application
    app = QApplication(sys.argv)

    # Create a main window
    # window = QMainWindow()
    # window.setWindowTitle("QGIS 3D Scene Example")
    # window.setGeometry(100, 100, 800, 600)

    # Create a QWidget to act as a container
    # container = QWidget()
    # # Create a QVBoxLayout to manage the layout of the container
    # layout = QVBoxLayout(container)
    # window.setCentralWidget(container)
    canvas = Qgs3DMapCanvas()
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.(canvas)

    canvas_widget = CanvasWidget()
    # layout.addWidget(canvas_widget)
    canvas_widget.show()
    sys.exit(app.exec_())

    # Create a 3D map settings object
    # map_settings = Qgs3DMapSettings()

    # Create a 3D map scene
    # map_scene = Qgs3DMapScene(map_settings)

    # Add the 3D map scene to the canvas
    # canvas.setMap(map_scene)
    #
    # # Load 3D Tiles data
    # tiles_layer = Qgs3DLayer.create("3dtiles", "path/to/3dtiles.json", "3D Tiles Layer")
    # if not tiles_layer:
    #     print("3D Tiles Layer failed to load!")
    # else:
    #     map_scene.addLayer(tiles_layer)
    #
    # # Set up navigation tools
    # navigate_tool = Qgs3DMapToolNavigate(canvas)
    # zoom_tool = Qgs3DMapToolZoom(canvas)
    # pan_tool = Qgs3DMapToolPan(canvas)
    #
    # canvas.setMapTool(navigate_tool)

    # Show the main window
    # window.show()

    # Start the Qt event loop
    # sys.exit(app.exec_())

    # Exit QGIS application
    # qgs.exitQgis()
