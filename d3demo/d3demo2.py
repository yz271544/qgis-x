from qgis.core import QgsApplication, QgsProject, QgsLayerTreeNode, QgsVectorLayer, QgsCesiumUtils


GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/project3d'

if __name__ == '__main__':

    # 初始化 QGIS 应用
    # app = QApplication([])
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 创建 QGIS 项目
    project = QgsProject.instance()

    # 添加3D Tiles图层
    uri = "type=3dtiles&url=http://172.31.100.34:38083/map/qxmx/jkg/tileset.json"  # 替换为您的3D Tiles URL
    layer = QgsVectorLayer(uri, "3D Tiles Layer", "3dtiles")

    QgsCesiumUtils()

    if not layer.isValid():
        print("3D Tiles Layer failed to load!")
    else:
        project.addMapLayer(layer)  # 将图层添加到项目

    # 保存项目
    project.write(f"{GEOJSON_PREFIX}/d3demo2.qgz")

    # 退出 QGIS
    qgs.exitQgis()
