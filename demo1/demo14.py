import os

from qgis.gui import QgsMapCanvas
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsProject,
    QgsField,
    QgsRasterLayer,
    QgsPointXY,
    QgsVectorLayer,
    QgsFeature,
    QgsSymbol,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMarkerSymbol,
    QgsFillSymbol,
    QgsRasterMarkerSymbolLayer,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateTransformContext,
    QgsSingleSymbolRenderer,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer,
    QgsPrintLayout,
    QgsLayoutPageCollection,
    QgsLayoutItemMap,
    QgsLayoutItemLegend,
    QgsLayoutItemLabel,
    QgsRectangle,
    QgsReadWriteContext,
    QgsMargins,
    QgsTextFormat,
    QgsMapSettings,
    QgsLayoutAligner,
    QgsLayoutMeasurement,
    QgsUnitTypes,
    QgsLayoutSize,
    QgsLayoutItem,
    QgsLayerTreeLayer,
    QgsLayoutItemShape,
    QgsLayoutItemGroup
)
from qgis.core import Qgis
# from qgis.PyQt.QtCore import QVariant, QMetaType, QRectF
from qgis.PyQt import QtCore
# from qgis.PyQt.QtGui import QColor
from qgis.PyQt import QtGui
# from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtXml
from typing import Optional

import sys, os
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PROJECT_DIR)
from core.PaperSize import PaperSpecification
from utils.unit_util import UnitUtil


LAYOUT_DIR = "D:/iProject/pypath/qgis-x/common/layout"
GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/projects'
ICON_PREFIX = 'D:/iProject/pypath/qgis-x/common/icon'


def add_points(layer_name: str, icon_name: str, point_name_prefix: str, points: list[tuple[float, float]],
               point_size: int = 5) -> QgsVectorLayer:
    """
    增加图层：相同大小和图标的点
    :param layer_name:
    :param icon_name:
    :param point_name_prefix:
    :param points:
    :param point_size:
    :return:
    """
    # global pointLayer, options
    # Create vector layer
    pointLayer = QgsVectorLayer("Point?crs=EPSG:3857", layer_name, "memory")
    pointProvider = pointLayer.dataProvider()
    pointProvider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("x", QtCore.QMetaType.Type(QtCore.QVariant.Double)),
        QgsField("y", QtCore.QMetaType.Type(QtCore.QVariant.Double))
    ])
    pointLayer.updateFields()
    # Set coordinate transform
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    pointLayer.startEditing()
    # Transform and add points
    for i, point in enumerate(points):
        transformed_point = transformer.transform(QgsPointXY(*point))
        feature = QgsFeature(pointLayer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(transformed_point))
        print(f"{point_name_prefix}{i + 1}", transformed_point.x(), transformed_point.y())
        feature.setAttributes([f"{point_name_prefix}{i + 1}", transformed_point.x(), transformed_point.y()])
        pointProvider.addFeature(feature)
    # Commit changes to the vector layer
    if pointLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + pointProvider.error().message())
    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"

    # Define GeoJSON file path
    # geojson_path = 'D:/iProject/pypath/qgis-x/output/projects/MinJing_Points.geojson'
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(pointLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    pointLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not pointLayer.isValid():
        print("Failed to load the layer!")
        sys.exit(1)
    # icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    icon_path = f'{ICON_PREFIX}/{icon_name}.png'
    raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    raster_layer.setSize(point_size)
    # symbol = QgsMarkerSymbol()
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
    symbol.changeSymbolLayer(0, raster_layer)
    # pointLayer.renderer().setSymbol(symbol)  # 直接设置渲染器的符号
    renderer = QgsSingleSymbolRenderer(symbol)
    pointLayer.setRenderer(renderer)
    return pointLayer


def add_line(layer_name: str, lines: list[list[tuple[float, float]]], color: str) -> QgsVectorLayer:
    """
    增加图层：相同颜色的道路线
    :param layer_name:
    :param lines:
    :param color:
    :return:
    """
    lineLayer = QgsVectorLayer("LineString?crs=EPSG:3857", layer_name, "memory")
    lineProvider = lineLayer.dataProvider()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    lineLayer.startEditing()

    for line in lines:
        transformed_line = [transformer.transform(QgsPointXY(*point)) for point in line]
        feature = QgsFeature(pointLayer.fields())
        lineString = QgsGeometry.fromPolylineXY(transformed_line)
        feature.setGeometry(lineString)
        lineProvider.addFeature(feature)

    if lineLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + lineProvider.error().message())

    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"
    # Define GeoJSON file path
    # geojson_path = 'D:/iProject/pypath/qgis-x/output/projects/MinJing_Points.geojson'
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(lineLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    lineLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not lineLayer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
    # symbol.setColor("#e77148")
    symbol.setColor(QtGui.QColor(color))
    symbol.setWidth(2)
    renderer = QgsSingleSymbolRenderer(symbol)
    lineLayer.setRenderer(renderer)

    return lineLayer


def add_polygon(layer_name: str, polygons: list[list[list[tuple[float, float]]]], color: str, opacity: float=0.5) -> QgsVectorLayer:
    """
    增加图层：相同颜色的多边形
    :param layer_name:
    :param polygons:
    :param color:
    :return:
    """
    polygonLayer = QgsVectorLayer("Polygon?crs=EPSG:3857", layer_name, "memory")
    polygonProvider = polygonLayer.dataProvider()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    polygonLayer.startEditing()

    for polygon in polygons:
        transformed_polygon = [[transformer.transform(QgsPointXY(*point)) for point in line] for line in polygon]
        feature = QgsFeature(pointLayer.fields())
        qgsPolygon = QgsGeometry.fromPolygonXY(transformed_polygon)
        feature.setGeometry(qgsPolygon)
        polygonProvider.addFeature(feature)

    if polygonLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + polygonProvider.error().message())

    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"
    # Define GeoJSON file path
    # geojson_path = 'D:/iProject/pypath/qgis-x/output/projects/MinJing_Points.geojson'
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(polygonLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    polygonLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not polygonLayer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
    # symbol.setColor("#e77148")
    symbol.setColor(QtGui.QColor(color))
    symbol.setOpacity(opacity)
    renderer = QgsSingleSymbolRenderer(symbol)
    polygonLayer.setRenderer(renderer)

    return polygonLayer


def add_circle(layer_name: str, center_point: tuple[float, float], radius: float, color: str, opacity: float=0.5, num_segments: int = 36) -> QgsVectorLayer:
    """
    增加图层：圆形
    :param layer_name: 图层名称
    :param center_point: 圆心坐标
    :param radius: 半径
    :param num_segments: 用于近似圆形的线段数量，数值越大越接近圆形
    :return:
    """
    circleLayer = QgsVectorLayer("Polygon?crs=EPSG:3857", layer_name, "memory")
    circleProvider = circleLayer.dataProvider()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    center_transformed = transformer.transform(QgsPointXY(*center_point))

    points = []
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = center_transformed.x() + radius * math.cos(angle)
        y = center_transformed.y() + radius * math.sin(angle)
        points.append(QgsPointXY(x, y))
    points.append(points[0])  # 闭合多边形

    circle_geometry = QgsGeometry.fromPolygonXY([points])
    circleLayer.startEditing()
    feature = QgsFeature()
    feature.setGeometry(circle_geometry)
    circleProvider.addFeature(feature)

    if circleLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + circleProvider.error().message())

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF - 8"
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(circleLayer, geojson_path, QgsCoordinateTransformContext(), options)
    circleLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not circleLayer.isValid():
        print("Failed to load the circleLayer!")
        sys.exit(1)

    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
    symbol.setColor(QtGui.QColor(color))
    symbol.setOpacity(opacity)
    renderer = QgsSingleSymbolRenderer(symbol)
    circleLayer.setRenderer(renderer)
    return circleLayer


def add_circle_key_areas(layer_name: str, center_point: tuple[float, float], radius: float, percent: tuple[float, float, float],
                         colors: tuple[str, str, str], opacities: tuple[float, float, float],
                         num_segments: int = 36) -> Optional[QgsVectorLayer]:
    """
    增加图层：三个同心圆
    :param layer_name: 图层名称
    :param center_point: 圆心坐标
    :param radii: 三个圆的半径
    :param colors: 三个圆的颜色
    :param capacities: 三个圆的透明度
    :param num_segments: 用于近似圆形的线段数量，数值越大越接近圆形
    :return:
    """
    radii = [radius]
    if len(percent) < 3:
        print("percent should have 3 elements")
        return None
    radii.append(radius * (percent[1] + percent[2]) / 100)
    radii.append(radius * percent[2] / 100)

    # 创建一个空的矢量图层
    circleLayer = QgsVectorLayer("Polygon?crs=EPSG:3857", layer_name, "memory")
    circleProvider = circleLayer.dataProvider()
    circleProvider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254)  # Ensure field name length does not exceed 254
    ])
    circleLayer.updateFields()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    center_transformed = transformer.transform(QgsPointXY(*center_point))

    circleLayer.startEditing()
    # 分别创建三个同心圆并添加到图层
    level = 1
    for radius in radii:
        points = []
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            x = center_transformed.x() + radius * math.cos(angle)
            y = center_transformed.y() + radius * math.sin(angle)
            points.append(QgsPointXY(x, y))
        points.append(points[0])  # 闭合多边形
        circle_geometry = QgsGeometry.fromPolygonXY([points])
        feature = QgsFeature(circleLayer.fields())
        feature.setAttribute("name", f"level-{level}")
        feature.setGeometry(circle_geometry)
        circleProvider.addFeature(feature)
        level += 1

    if circleLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + circleLayer.dataProvider().error().message())

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF - 8"
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(circleLayer, geojson_path, QgsCoordinateTransformContext(), options)
    circleLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not circleLayer.isValid():
        print("Failed to load the circleLayer!")
        sys.exit(1)

    # 为每个圆分别设置样式
    categories = []
    border_color = "#ffffff"  # 边线颜色，这里设置为黑色
    border_width = 0.2  # 边线宽度
    for i, (color, opacity) in enumerate(zip(colors, opacities)):
        symbol = QgsFillSymbol()
        symbol.setColor(QtGui.QColor(color))
        symbol.setOpacity(opacity)
        # 设置边线颜色和宽度
        symbol.symbolLayer(0).setStrokeColor(QtGui.QColor(border_color))
        symbol.symbolLayer(0).setStrokeWidth(border_width)
        category = QgsRendererCategory(f"level-{i + 1}", symbol, f"level-{i + 1}")
        categories.append(category)

    renderer = QgsCategorizedSymbolRenderer("name", categories)
    circleLayer.setRenderer(renderer)
    return circleLayer


def customize_legend(legend, legend_title):
    # Set the legend title
    legend.setTitle(legend_title)

    # Control which layers are included in the legend
    legend.setAutoUpdateModel(False)  # Disable auto-update to manually control layers
    # Remove all existing layers from the legend
    legend_model = legend.model()
    while legend_model.rowCount() > 0:
        legend_model.removeRow(0)
    # legend.cleanup()  # Clear existing legend items

    # Add specific layers to the legend
    project = QgsProject.instance()
    layers = project.mapLayersByName("民警") + project.mapLayersByName("应急道路") + project.mapLayersByName("重点区域")
    for layer in layers:
        legend_model.rootGroup().addLayer(layer)
    # Customize the appearance of legend items
    for layer in layers:
        layer_tree_layer = legend_model.rootGroup().findLayer(layer.id())
        if layer_tree_layer:
            for i in range(len(layer_tree_layer.children())):
                item = layer_tree_layer.children()[i]
                if isinstance(item, QgsLayerTreeLayer):
                    item.setFont(QtGui.QFont("Arial", 10))  # Set font for legend items
                    item.setSymbolSize(QtCore.QSizeF(10, 10))  # Set symbol size



def add_print_layout(project, canvas) -> QgsPrintLayout:
    layout = QgsPrintLayout(project)
    layout.setName("位置图")
    layout.setUnits(QgsUnitTypes.LayoutMillimeters)
    layout.initializeDefaults()

    # 设置纸张类型和大小（以A4为例）
    page_collection = layout.pageCollection()
    page = page_collection.page(0)
    # 1表示横向，0表示纵向
    page.setPageSize(PaperSpecification.A4.get_name(), 1)

    # 设置布局的边距 (单位：毫米) 左上右下
    left_margin = 22
    top_margin = 30
    right_margin = 18
    bottom_margin = 22

    # Print margins information
    print(f"Left: {left_margin}, Top: {top_margin}, Right: {right_margin}, Bottom: {bottom_margin}")

    map_item = QgsLayoutItemMap(layout)
    map_item.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    print("Canvas CRS:", canvas.mapSettings().destinationCrs().authid())
    print("Map Item CRS:", map_item.crs().authid())

    map_item.setKeepLayerSet(False)
    map_item.setFrameEnabled(True)


    # 设置地图项在布局中的位置和大小
    map_width = PaperSpecification.A4.value[1] - left_margin - right_margin
    map_height = PaperSpecification.A4.value[0] - top_margin - bottom_margin
    print(f"x: {left_margin}, y: {top_margin}, width: {map_width}, height: {map_height}")
    map_item.attemptSetSceneRect(QtCore.QRectF(left_margin, top_margin, map_width, map_height), True)  # 设置地图项在布局中的大小
    map_item.setFrameStrokeWidth(QgsLayoutMeasurement(1, QgsUnitTypes.LayoutMillimeters))
    # 设置地图项的固定大小
    fixed_size = QgsLayoutSize(map_width, map_height, QgsUnitTypes.LayoutMillimeters)
    map_item.setFixedSize(fixed_size)


    # 获取主画布范围并设置到地图项
    main_canvas_extent = canvas.extent()
    map_item.setExtent(main_canvas_extent)


    # map_item.atlasScalingMode()
    # map_item.setPos(QtCore.QPointF(0, 0))
    layout.addLayoutItem(map_item)

    # # 添加标题
    title = QgsLayoutItemLabel(layout)
    title.setText("郑州二期警务部署图")

    # Use QgsTextFormat to set the font
    text_format = QgsTextFormat()
    text_format.allowHtmlFormatting()
    font = QtGui.QFont("SimSun", 30)
    font.setFamily("SimSun")
    font.setPixelSize(30)
    font.setPointSize(30)
    text_format.setFont(font)
    text_format.setForcedBold(True)
    title.setVAlign(QtCore.Qt.AlignBottom)  # 垂直居中
    title.setHAlign(QtCore.Qt.AlignHCenter)  # 水平居中
    title.adjustSizeToText()
    text_format.setNamedStyle("font-size: 30px")
    text_css = text_format.asCSS()
    print(f"text_css: {text_css}")
    title.setTextFormat(text_format)
    title.setFont(font)
    title.attemptSetSceneRect(QtCore.QRectF(left_margin, 0, map_width, top_margin - 10))
    # title.setPos(QtCore.QPointF(50, 50))
    layout.addLayoutItem(title)

    # 添加图例
    legend = QgsLayoutItemLegend(layout)
    # legend.setTitle("图例")
    # legend.setAutoUpdateModel(True)
    customize_legend(legend, "图例")
    legend_width = 40
    legend_height = 80
    legend_x = left_margin + map_width - legend_width - 0.5
    legend_y = top_margin + map_height - legend_height - 0.5
    legend.setReferencePoint(QgsLayoutItem.ReferencePoint.LowerRight)
    legend.attemptSetSceneRect(QtCore.QRectF(legend_x, legend_y, 40, 80))
    legend_fixed_size = QgsLayoutSize(legend_width, legend_height, QgsUnitTypes.LayoutMillimeters)
    legend.setFixedSize(legend_fixed_size)
    # legend.setPos(QtCore.QPointF(120, 10))
    layout.addLayoutItem(legend)


    # Add remarks box background
    remarks_text = "备注: 这里填写备注信息"
    remarks_format = QgsTextFormat()
    remarks_format.setFont(QtGui.QFont("SimSun", 12))
    remarks_width = 100  # Adjust width as needed
    remarks_height = 20  # Adjust height as needed
    remarks_x = left_margin + 1
    remarks_y = top_margin + map_height + 1 - remarks_height  # Adjust position as needed


    remarks_bg = QgsLayoutItemShape(layout)
    remarks_bg.setShapeType(QgsLayoutItemShape.Rectangle)
    remarks_bg.setBackgroundColor(QtGui.QColor(255, 255, 255))  # Set background color to white
    remarks_bg.setFrameEnabled(True)
    remarks_bg.setFrameStrokeWidth(QgsLayoutMeasurement(0.5, QgsUnitTypes.LayoutMillimeters))
    remarks_bg.attemptSetSceneRect(QtCore.QRectF(remarks_x, remarks_y, remarks_width, remarks_height))
    layout.addLayoutItem(remarks_bg)

    # Add remarks text
    remarks = QgsLayoutItemLabel(layout)
    remarks.setText(remarks_text)
    remarks.setTextFormat(remarks_format)
    remarks.setVAlign(QtCore.Qt.AlignTop)
    remarks.setHAlign(QtCore.Qt.AlignLeft)
    remarks.adjustSizeToText()
    remarks.attemptSetSceneRect(QtCore.QRectF(remarks_x + 2, remarks_y + 2, remarks.boundingRect().width(), remarks.boundingRect().height()))
    layout.addLayoutItem(remarks)

    # Group the background and text
    group = QgsLayoutItemGroup(layout)
    group.addItem(remarks_bg)
    group.addItem(remarks)
    # group.setReferencePoint(QgsLayoutItem.ReferencePoint.LowerLeft)
    # group.attemptSetSceneRect(QtCore.QRectF(remarks_x, remarks_y, remarks_width, remarks_height))
    layout.addLayoutItem(group)

    layout.refresh()
    #
    # # 保存为.qpt文件
    # qpt_file_path = f"{GEOJSON_PREFIX}/jingwei3.qpt"
    # context = QgsReadWriteContext()
    # layout.saveAsTemplate(qpt_file_path, context)

    # 或者保存为.qpt模板文件
    # doc = QtXml.QDomDocument()
    # layout.saveAsTemplate(doc)
    # with open('D:/iProject/pypath/qgis-x/output/projects/demo_layout.qpt', 'w') as f:
    #     f.write(doc.toString())

    return layout


def load_qpt_template(project, qpt_file_path):
    doc = QtXml.QDomDocument()
    if os.path.exists(qpt_file_path):
        with open(qpt_file_path, 'r') as file:
            doc.setContent(file.read())
        layout = QgsPrintLayout(project)
        layout.loadFromTemplate(doc, QgsReadWriteContext())
        layout_name = "Loaded-Layout"
        # 你可以自定义布局名称
        layout.setName(layout_name)
        project.layoutManager().addLayout(layout)


def update_layout_extent(layout_name):
    project = QgsProject.instance()
    layout_manager = project.layoutManager()
    layout = layout_manager.layoutByName(layout_name)
    if layout:
        for item in layout.items():
            if isinstance(item, QgsLayoutItemMap):
                canvas = QgsMapCanvas()  # Ensure you get the correct instance of the main window map canvas
                item.setExtent(canvas.extent())
                layout.refresh()



if __name__ == '__main__':
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

    # Create map settings and set the extent
    map_settings = QgsMapSettings()
    map_extent = QgsRectangle(111.47, 40.72, 111.49, 40.73)
    map_settings.setExtent(map_extent)

    # qpt_file_path = f"{GEOJSON_PREFIX}/jingwei1.qpt"
    # load_qpt_template(project, qpt_file_path)

    # Load tile layers
    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    base_tile_layer = QgsRasterLayer(base_tile_url, "Base-Tile", "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)

    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    tile_layer = QgsRasterLayer(tile_url, "Main-Tile", "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)

    # Add vector layer to project
    pointLayer = add_points("民警", "民警", "minjing-Point",
                            [(111.4775222, 40.7290133), (111.4766598, 40.7282033)])
    project.addMapLayer(pointLayer)

    # Add line layer to project
    lineLayer = add_line("应急道路", [
        [(111.4857822, 40.726082), (111.4866153, 40.7256001), (111.4882815, 40.726957), (111.4901084, 40.7284965),
         (111.4901084, 40.7284965)]], "#e77148")
    project.addMapLayer(lineLayer)

    # Add polygon layer to project
    polygonLayer = add_polygon("重点区域", [[[(111.4839918, 40.7258937), (111.4855557, 40.7250408),
                                               (111.4869734, 40.7262813), (111.4855264, 40.7272782),
                                               (111.4855264, 40.7272782), (111.4839918, 40.7258937)]]], "#e77148")
    project.addMapLayer(polygonLayer)

    # cir1Layer = add_circle("cir1", (111.477486, 40.724372), 41, "#2f99f3", 0.6,72)
    # project.addMapLayer(cir1Layer)

    cir1Layer = add_circle_key_areas("防范区域", (111.477486, 40.724372), 41, (40, 30, 30),
                                     ("#ff4040", "#00cd52", "#2f99f3"), (0.4, 0.4, 0.4), 72)
    project.addMapLayer(cir1Layer)

    # 如下是将添加到地图的图层，设置为地图视口范围
    # Create map settings and set the extent
    map_settings = QgsMapSettings()

    # Calculate the combined extent of all layers
    extent = QgsRectangle()

    projectLayers = project.mapLayers().values()
    for layer in projectLayers:
        if layer.name() not in ["Main-Tile", "Base-Tile"]:
            extent.combineExtentWith(layer.extent())

    # Set the map canvas extent to the combined extent
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    map_settings.setExtent(extent)

    # Create a map canvas and set its extent
    canvas = QgsMapCanvas()
    canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    canvas.setExtent(extent)

    project.layoutManager().addLayout(add_print_layout(project, canvas))
    # canvas.extentsChanged.connect(lambda: update_layout_extent("位置图"))

    # Save project
    project.write(f"{GEOJSON_PREFIX}/demo14.qgz")

    # Exit QGIS application
    qgis.exitQgis()
