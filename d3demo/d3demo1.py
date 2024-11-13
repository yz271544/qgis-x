from qgis.core import (
    QgsApplication,
    QgsProject,
)
from qgis.gui import Qgs3DMapCanvas
from qgis._3d import Qgs3DMapScene, Qgs3DMapSettings, Qgs3DLayer

if __name__ == '__main__':

    # 初始化 QGIS 应用程序
    app = QgsApplication([], False)
    app.initQgis()

    # 创建QGIS项目实例
    project = QgsProject.instance()

    # 创建3D地图画布和3D地图设置
    canvas = Qgs3DMapCanvas()
    map_settings = Qgs3DMapSettings()
    scene = Qgs3DMapScene(canvas)
    

    # 配置3D Tiles图层
    uri = "type=3dtiles&url=https://your-3dtiles-url/tileset.json"  # 替换为您的3D Tiles URL
    layer = Qgs3DLayer(uri, "3D Tiles Layer")

    # 检查图层是否有效并添加到场景
    if not layer.isValid():
        print("3D Tiles Layer failed to load!")
    else:
        map_settings.addLayer(layer)
        scene.setMapSettings(map_settings)
        canvas.setMapScene(scene)

    # 如果需要保存QGIS项目
    project.write("/path/to/your/project.qgz")

    # 退出 QGIS 应用程序
    app.exitQgis()