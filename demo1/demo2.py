from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer
)
import sys
import os

if __name__ == '__main__':
    # Set QGIS installation path (modify according to your actual installation)
    # qgis_path = "D:/iSoft/QGIS-3.38.1/apps/qgis"
    # Initialize QGIS application
    # QgsApplication.setPrefixPath(qgis_path, True)
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    # Layer name
    base_layer_name = "Base_Tile-Server"
    # Create and load tile layer
    base_tile_layer = QgsRasterLayer(base_tile_url, base_layer_name, "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)
    else:
        print("Base Tile layer failed to load! Error:", base_tile_layer.error().message())
        print("Check the URL and ensure it returns a valid raster image.")

    # Tile service URL
    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    # Layer name
    layer_name = "Tile-Server"
    # Create and load tile layer
    tile_layer = QgsRasterLayer(tile_url, layer_name, "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)
    else:
        print("Tile layer failed to load! Error:", tile_layer.error().message())
        print("Check the URL and ensure it returns a valid raster image.")

    # 保存项目到 .qgs 或 .qgz 文件
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo2.qgz")


    # Exit QGIS application
    qgis.exitQgis()