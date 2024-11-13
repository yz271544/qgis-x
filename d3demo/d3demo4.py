from qgis.core import QgsApplication, QgsProject, QgsVector3D, QgsTiledSceneLayer
from qgis._3d import Qgs3DMapCanvas, Qgs3DMapSettings, QgsTiledSceneLayer3DRenderer



GEOJSON_PREFIX = '/lyndon/iProject/pypath/qgis-x/common/output/project3d'


if __name__ == '__main__':

    # 初始化 QGIS 应用
    qgs = QgsApplication([], False)
    qgs.initQgis()

    url = "https://storage.googleapis.com/ahp-research/maquette/corsica_5m/tiles2/layer.json"
    tsl = QgsTiledSceneLayer(url, "qmtest", "quantizedmesh")
    tsl.setRenderer3D(QgsTiledSceneLayer3DRenderer())

    # 创建 QGIS 项目
    project = QgsProject.instance()
    project.addMapLayer(tsl)

    # 创建3D地图画布
    canvas = Qgs3DMapCanvas()

    # 保存项目
    project.write(f"{GEOJSON_PREFIX}/d3demo4.qgz")

    # 退出 QGIS
    qgs.exitQgis()



