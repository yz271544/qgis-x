from qgis.core import QgsApplication, QgsProject, QgsVector3D
from qgis._3d import Qgs3DMapCanvas, Qgs3DMapSettings


if __name__ == '__main__':

    # 初始化 QGIS 应用
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # 创建 QGIS 项目
    project = QgsProject.instance()
    project.read("/path/to/your/project.qgz")  # 替换为您的项目路径，如果没有项目路径可选新建

    # 创建3D地图画布
    canvas = Qgs3DMapCanvas()

    # 创建并配置3D地图设置
    map_settings = Qgs3DMapSettings()
    map_settings.setOrigin(QgsVector3D(0, 0, 0))  # 可以设置原点位置，或其他必要的配置
    map_settings.set

    # 设置3D地图画布的地图设置
    canvas.mapSettings().setMapSettings(map_settings)

    # 你还可以添加其他设置，比如3D图层、坐标系、视角等

    # 退出 QGIS
    qgs.exitQgis()
