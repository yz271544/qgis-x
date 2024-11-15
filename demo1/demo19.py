import base64
import sys, os
import math
import time

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
    QgsLayoutItemGroup,
    QgsRuleBasedRenderer,
    QgsLayoutExporter,
    QgsLineSymbol,
    QgsArrowSymbolLayer,
    QgsProperty,
    QgsLegendModel,
    QgsMapLayerLegendUtils,
    QgsLegendRenderer,
    QgsSymbolLegendNode,
    QgsFontMarkerSymbolLayer,
    QgsSymbolLayer,
    QgsPointClusterRenderer,
)
from qgis.core import Qgis
# from qgis.PyQt.QtCore import QVariant, QMetaType, QRectF
from qgis.PyQt import QtCore
# from qgis.PyQt.QtGui import QColor
from qgis.PyQt import QtGui
# from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtXml
from typing import Optional


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR:{BASE_DIR}")
PROJECT_DIR = os.path.dirname(BASE_DIR)
print(f"PROJECT_DIR:{PROJECT_DIR}")
sys.path.append(BASE_DIR)
sys.path.append(PROJECT_DIR)
from core.PaperSize import PaperSpecification
from utils.unit_util import UnitUtil
from utils.file_util import FileUtil
from utils.qt_font import QtFontUtil
print(f"libs: {BASE_DIR}/venv/Lib/site-packages")
sys.path.append(f"{BASE_DIR}/venv/Lib/site-packages")
from addict import Dict

LAYOUT_DIR = "D:/iProject/pypath/qgis-x/common/layout"
GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/projects'
# ICON_PREFIX = 'D:/iProject/pypath/qgis-x/common/icon'
ICON_PREFIX = 'D:/iProject/pypath/qgis-x/common/output/projects'


def add_points(layer_name: str, icon_name: str, point_name_prefix: str, points: list[tuple[float, float]],
               point_size: int = 5, icon_base64: str = "") -> QgsVectorLayer:
    """
    增加图层：相同大小和图标的点
    :param layer_name:
    :param icon_name:
    :param point_name_prefix:
    :param points:
    :param point_size:
    :param icon_base64: Base64 encoded image string
    :return:
    """
    # global pointLayer, options
    # Create vector layer
    point_layer = QgsVectorLayer("Point?crs=EPSG:3857", layer_name, "memory")
    point_provider = point_layer.dataProvider()
    point_provider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("type", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),
        QgsField("x", QtCore.QMetaType.Type(QtCore.QVariant.Double)),
        QgsField("y", QtCore.QMetaType.Type(QtCore.QVariant.Double))
    ])
    point_layer.updateFields()
    # Set coordinate transform
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    point_layer.startEditing()
    # Transform and add points
    for i, point in enumerate(points):
        transformed_point = transformer.transform(QgsPointXY(*point))
        feature = QgsFeature(point_layer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(transformed_point))
        print(f"{point_name_prefix}{i + 1}", transformed_point.x(), transformed_point.y())
        feature.setAttributes([f"{point_name_prefix}{i + 1}", "point", transformed_point.x(), transformed_point.y()])
        point_provider.addFeature(feature)
    # Commit changes to the vector layer
    if point_layer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + point_provider.error().message())
    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"

    # Define GeoJSON file path
    # geojson_path = 'D:/iProject/pypath/qgis-x/output/projects/MinJing_Points.geojson'
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(point_layer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    point_layer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not point_layer.isValid():
        print("Failed to load the layer!")
        sys.exit(1)
    # icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    icon_path = f'{ICON_PREFIX}/{icon_name}.png'
    if icon_base64 != "":
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(base64.b64decode(icon_base64))


    label_style = Dict()
    label_font_color = "#0000ff"
    label_style.font_family = "SimSun"
    label_style.font_size = 10
    label_style.font_color = label_font_color
    label_style.is_bold = True
    label_style.is_italic = False
    label_style.spacing = 0.0

    # 创建一个嵌入式规则渲染器
    rule_symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
    rule_font_marker = QgsFontMarkerSymbolLayer(label_style.font_family)
    rule_font_marker.setSize(label_style.font_size)
    rule_font_marker.setColor(QtGui.QColor(label_style.font_color))
    rule_font_marker.setDataDefinedProperty(QgsSymbolLayer.PropertyCharacter, QgsProperty.fromExpression("name"))
    rule_font_marker.setOffset(QtCore.QPointF(0, -15))
    rule_raster_marker = QgsRasterMarkerSymbolLayer(icon_path)
    rule_raster_marker.setSize(point_size)
    rule_symbol.changeSymbolLayer(0, rule_raster_marker)
    rule_symbol.appendSymbolLayer(rule_font_marker)
    root_rule = QgsRuleBasedRenderer.Rule(None)
    rule = QgsRuleBasedRenderer.Rule(rule_symbol)
    rule.setFilterExpression("ELSE")  # Else rule
    root_rule.appendChild(rule)
    rule_renderer = QgsRuleBasedRenderer(root_rule)

    # 设置聚合渲染器
    cluster_symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
    font_marker = QgsFontMarkerSymbolLayer(label_style.font_family)
    font_marker.setSize(label_style.font_size)
    font_marker.setColor(QtGui.QColor(label_style.font_color))
    font_marker.setDataDefinedProperty(QgsSymbolLayer.PropertyCharacter,
                                       QgsProperty.fromExpression("concat('(', @cluster_size, ')')"))
    font_marker.setOffset(QtCore.QPointF(0, -15))
    raster_marker = QgsRasterMarkerSymbolLayer(icon_path)
    raster_marker.setSize(point_size)
    cluster_symbol.changeSymbolLayer(0, raster_marker)
    cluster_symbol.appendSymbolLayer(font_marker)
    cluster_renderer = QgsPointClusterRenderer()
    cluster_renderer.setTolerance(10)
    cluster_renderer.setToleranceUnit(QgsUnitTypes.RenderMillimeters)
    cluster_renderer.setClusterSymbol(cluster_symbol)
    # 插入嵌入式渲染器
    cluster_renderer.setEmbeddedRenderer(rule_renderer)

    point_layer.setRenderer(cluster_renderer)

    point_layer.triggerRepaint()

    return point_layer


def add_line(layer_name: str, lines: list[list[tuple[float, float]]], color: str,
             width: float,
             additional_widths: Optional[list[float]],
             additional_colors: Optional[list[str]],
             additional_opacities: Optional[list[float]]) -> QgsVectorLayer:
    """
    增加图层：相同颜色的道路线，并增加宽度和不同颜色和透明度的标注
    :param layer_name: 图层名称
    :param lines: 线的坐标列表
    :param color: 线的颜色
    :param width: 线的宽度
    :param additional_widths: 额外宽度列表
    :param additional_colors: 额外颜色列表
    :param additional_opacities: 额外透明度列表
    :return: QgsVectorLayer
    """
    line_layer = QgsVectorLayer("LineString?crs=EPSG:3857", layer_name, "memory")
    line_provider = line_layer.dataProvider()
    line_provider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),
        QgsField("type", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254)
    ])
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    line_layer.startEditing()

    for line in lines:
        transformed_line = [transformer.transform(QgsPointXY(*point)) for point in line]
        feature = QgsFeature(line_layer.fields())
        lineString = QgsGeometry.fromPolylineXY(transformed_line)
        feature.setGeometry(lineString)
        feature.setAttributes([layer_name, "line"])
        line_provider.addFeature(feature)

    if line_layer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + line_provider.error().message())

    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(line_layer, geojson_path, QgsCoordinateTransformContext(), options)
    line_layer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not line_layer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    root_rule = QgsRuleBasedRenderer.Rule(None)
    base_symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
    base_symbol.setColor(QtGui.QColor(color))
    base_symbol.setWidth(width)
    base_rule = QgsRuleBasedRenderer.Rule(base_symbol)
    root_rule.appendChild(base_rule)

    # Add additional widths with different colors and opacities
    if additional_widths is not None and additional_colors is not None and additional_opacities is not None:
        for add_width, add_color, add_opacity in zip(additional_widths, additional_colors, additional_opacities):
            add_symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
            add_symbol.setColor(QtGui.QColor(add_color))
            add_symbol.setWidth(add_width)
            add_symbol.setOpacity(add_opacity)
            add_rule = QgsRuleBasedRenderer.Rule(add_symbol)
            root_rule.appendChild(add_rule)

    renderer = QgsRuleBasedRenderer(root_rule)
    line_layer.setRenderer(renderer)


    return line_layer


def add_polygon(layer_name: str, polygons: list[list[list[tuple[float, float]]]], color: str, opacity: float=0.5) -> QgsVectorLayer:
    """
    增加图层：相同颜色的多边形
    :param layer_name:
    :param polygons:
    :param color:
    :return:
    """
    polygon_layer = QgsVectorLayer("Polygon?crs=EPSG:3857", layer_name, "memory")
    polygon_provider = polygon_layer.dataProvider()
    polygon_provider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("type", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),
    ])
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    # Start editing the vector layer
    polygon_layer.startEditing()

    for polygon in polygons:
        transformed_polygon = [[transformer.transform(QgsPointXY(*point)) for point in line] for line in polygon]
        feature = QgsFeature(polygon_layer.fields())
        qgsPolygon = QgsGeometry.fromPolygonXY(transformed_polygon)
        feature.setGeometry(qgsPolygon)
        feature.setAttributes([layer_name, "polygon"])
        polygon_provider.addFeature(feature)

    if polygon_layer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + polygon_provider.error().message())

    # Save the vector layer to a GeoJSON file
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"
    # Define GeoJSON file path
    # geojson_path = 'D:/iProject/pypath/qgis-x/output/projects/MinJing_Points.geojson'
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(polygon_layer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    polygon_layer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not polygon_layer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
    # symbol.setColor("#e77148")
    symbol.setColor(QtGui.QColor(color))
    symbol.setOpacity(opacity)
    renderer = QgsSingleSymbolRenderer(symbol)
    polygon_layer.setRenderer(renderer)

    return polygon_layer


def add_circle(layer_name: str, center_point: tuple[float, float], radius: float, color: str, opacity: float=0.5, num_segments: int = 36) -> QgsVectorLayer:
    """
    增加图层：圆形
    :param layer_name: 图层名称
    :param center_point: 圆心坐标
    :param radius: 半径
    :param num_segments: 用于近似圆形的线段数量，数值越大越接近圆形
    :return:
    """
    circle_layer = QgsVectorLayer("Polygon?crs=EPSG:3857", layer_name, "memory")
    circle_provider = circle_layer.dataProvider()
    circle_provider.addAttributes([
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("type", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),
    ])
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
    circle_layer.startEditing()
    feature = QgsFeature()
    feature.setGeometry(circle_geometry)
    feature.setAttributes([f"{layer_name}", "circle"])
    circle_provider.addFeature(feature)

    if circle_layer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + circle_provider.error().message())

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF - 8"
    geojson_path = f'{GEOJSON_PREFIX}/{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(circle_layer, geojson_path, QgsCoordinateTransformContext(), options)
    circle_layer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not circle_layer.isValid():
        print("Failed to load the circleLayer!")
        sys.exit(1)

    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
    symbol.setColor(QtGui.QColor(color))
    symbol.setOpacity(opacity)
    renderer = QgsSingleSymbolRenderer(symbol)
    circle_layer.setRenderer(renderer)
    return circle_layer

def add_arrow(layer_name):
    # 创建一个箭头符号层
    arrow_layer = QgsArrowSymbolLayer()
    # 设置箭头头部大小（这里示例设置为3毫米，单位是地图单位，可根据需求调整）
    arrow_layer.setHeadLength(3)
    arrow_layer.setHeadThickness(3)
    # 设置箭头颜色（这里设置为蓝色）
    arrow_layer.setColor(QtGui.QColor(0, 0, 255))
    return arrow_layer

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
        QgsField("name", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("type", QtCore.QMetaType.Type(QtCore.QVariant.String), len=254)
    ])
    circleLayer.updateFields()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)
    center_transformed = transformer.transform(QgsPointXY(*center_point))

    circleLayer.startEditing()
    # 分别创建三个同心圆并添加到图层
    area_name = ['控制区','警戒区','核心区']
    level = 0
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
        feature.setAttribute("name", area_name[level])
        feature.setAttribute("type", "leveled-circle")
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
        category = QgsRendererCategory(area_name[i], symbol, area_name[i])
        categories.append(category)

    renderer = QgsCategorizedSymbolRenderer("name", categories)
    circleLayer.setRenderer(renderer)
    return circleLayer


def customize_legend(project, legend, legend_title):
    # Set the legend title
    legend.setTitle(legend_title)

    # Control which layers are included in the legend
    legend.setAutoUpdateModel(False)  # Disable auto-update to manually control layers

    legend_model: QgsLegendModel = legend.model()
    root_group = legend_model.rootGroup()
    root_group.clear()

    layers = project.mapLayers().values()
    # Customize the appearance of legend items
    for map_layer in layers:
        if map_layer.name() not in ["BaseTile", "MainTile"]:
            # root_group.addLayer(vector_layer)
            layer_custom_type = get_type(map_layer)
            if layer_custom_type == "":
                continue
            layer_renderer = map_layer.renderer()
            legend_symbol_items = layer_renderer.legendSymbolItems()
            for tr in root_group.children():
                if layer_custom_type == "point" and tr.layerId() == map_layer.id():
                    # custom symbol
                    for legend_symbol_item in legend_symbol_items:
                        symbol: QgsMarkerSymbol = legend_symbol_item.symbol()
                        symbol_layers = symbol.symbolLayers()
                        filtered_symbol_layers = []
                        for symbol_layer in symbol_layers:
                            if symbol_layer.layerType() != "FontMarker":
                                filtered_symbol_layers.append(symbol_layer.clone())
                        filtered_marker_symbol = QgsMarkerSymbol(filtered_symbol_layers)
                        legend_symbol_item.setSymbol(filtered_marker_symbol)
                        symbol_legend_node = QgsSymbolLegendNode(tr, legend_symbol_item)
                        symbol_legend_node.setCustomSymbol(filtered_marker_symbol)
                        QgsMapLayerLegendUtils.setLegendNodeCustomSymbol(tr, 0, filtered_marker_symbol)
            root_group.addLayer(map_layer)
    legend.refresh()

def get_type(layer) -> str:
    layer_custom_type = ""
    # 获取字段索引 (name)
    field_name = "type"
    field_index = layer.fields().indexFromName(field_name)
    # 检查字段是否有效
    if field_index == -1:
        print(f"Field {field_name} not found in layer {layer.name()}")
        return layer_custom_type
    else:
        # 获取字段值
        for feature in layer.getFeatures():
            layer_custom_type = feature[field_index]
            print(f"Feature ID: {feature.id()}, {field_name}: {layer_custom_type}")
        return layer_custom_type


def add_print_layout(project, canvas) -> QgsPrintLayout:
    layout = QgsPrintLayout(project)
    layout.setName("local-image")
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
    map_item.setFollowVisibilityPresetName("DefaultMap")


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

    layout.addLayoutItem(map_item)

    # # 添加标题
    title = QgsLayoutItemLabel(layout)
    title.setText("map title")

    text_format = QtFontUtil.create_font("黑体", 30, "#000000", True, False, Qgis.TextOrientation.Horizontal)

    title.setVAlign(QtCore.Qt.AlignBottom)  # 垂直居中
    title.setHAlign(QtCore.Qt.AlignHCenter)  # 水平居中
    title.adjustSizeToText()
    title.setTextFormat(text_format)
    title.attemptSetSceneRect(QtCore.QRectF(left_margin, 0, map_width, top_margin - 10))
    layout.addLayoutItem(title)

    # Add remarks box background
    remarks_text = "remark: remark message"

    remarks_format = QtFontUtil.create_font("SimSun", 12, "#000000",False, False, Qgis.TextOrientation.Horizontal)

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
    layout.addLayoutItem(group)

    # Add right side label
    add_right_side_label(layout)
    project.layoutManager().addLayout(layout)

    # 添加自定义图例
    legend = QgsLayoutItemLegend(layout)
    customize_legend(project, legend, "legend")
    legend_width = 40
    legend_height = 80
    legend_x = left_margin + map_width - legend_width - 0.5
    legend_y = top_margin + map_height - legend_height - 0.5
    legend.setReferencePoint(QgsLayoutItem.ReferencePoint.LowerRight)
    legend.attemptSetSceneRect(QtCore.QRectF(legend_x, legend_y, 40, 80))
    legend_fixed_size = QgsLayoutSize(legend_width, legend_height, QgsUnitTypes.LayoutMillimeters)
    legend.setFixedSize(legend_fixed_size)
    layout.addLayoutItem(legend)

    # Refresh layout to apply changes
    layout.updateSettings()
    layout.refresh()

    return layout


def add_right_side_label(layout):
    # Create a label item
    label = QgsLayoutItemLabel(layout)
    label.setText("index title")

    text_format = QtFontUtil.create_font("黑体", 14, "#000000", False, False, Qgis.TextOrientation.Vertical, 3.0)

    label.setTextFormat(text_format)
    label.setVAlign(QtCore.Qt.AlignVCenter)  # 垂直居中

    # Position the label
    label_x = layout.pageCollection().page(0).pageSize().width() - 5  # 0.5 cm from the right border
    label_y = 5  # 0.5 cm from the top border
    label.attemptSetSceneRect(QtCore.QRectF(label_x, label_y, 14, 100))  # Adjust width and height as needed

    # Add the label to the layout
    layout.addLayoutItem(label)


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


def export_layout_to_image(layout, output_path):
    exporter = QgsLayoutExporter(layout)
    settings = exporter.ImageExportSettings()
    settings.dpi = 300
    start_time = time.time()

    try:
        print(f"delete file {output_path}")
        FileUtil.delete_file(output_path)
        time.sleep(0.5)
    except Exception as e:
        print(f"delete file {output_path} failed: {e}")
        pass

    if os.path.exists(output_path):
        print(f"delete file {output_path} failed")
        return

    print(f"Starting export image to {output_path}...")
    result = exporter.exportToImage(output_path, settings)

    if result == QgsLayoutExporter.Success:
        print(f"Layout exported successfully to {output_path}")
    else:
        print(f"Failed to export layout to {output_path}, result code: {result}")
    end_time = time.time()
    print(f"execution time: {end_time - start_time} seconds")


def export_layout_to_pdf(layout, output_path):
    exporter = QgsLayoutExporter(layout)
    settings = exporter.PdfExportSettings()
    settings.dpi = 300
    start_time = time.time()

    try:
        print(f"delete file {output_path}")
        FileUtil.delete_file(output_path)
        time.sleep(0.5)  # Add a small delay to ensure the file is deleted
    except Exception as e:
        print(f"delete file {output_path} failed: {e}")
        pass

    if os.path.exists(output_path):
        print(f"delete file {output_path} failed")
        return

    print(f"Starting export pdf to {output_path}...")
    result = exporter.exportToPdf(output_path, settings)

    if result == QgsLayoutExporter.Success:
        print(f"Layout exported successfully to {output_path}")
    else:
        print(f"Failed to export layout to {output_path}, result code: {result}")
    end_time = time.time()
    print(f"执行时间: {end_time - start_time} 秒")



def export_layout_to_svg(layout, output_path):
    exporter = QgsLayoutExporter(layout)
    settings = exporter.SvgExportSettings()
    settings.dpi = 300
    start_time = time.time()

    try:
        print(f"delete file {output_path}")
        FileUtil.delete_file(output_path)
        time.sleep(0.5)  # Add a small delay to ensure the file is deleted
    except Exception as e:
        print(f"delete file {output_path} failed: {e}")
        pass

    if os.path.exists(output_path):
        print(f"delete file {output_path} failed")
        return

    print(f"Starting export pdf to {output_path}...")
    result = exporter.exportToSvg(output_path, settings)

    if result == QgsLayoutExporter.Success:
        print(f"Layout exported successfully to {output_path}")
    else:
        print(f"Failed to export layout to {output_path}, result code: {result}")
    end_time = time.time()
    print(f"执行时间: {end_time - start_time} 秒")



if __name__ == '__main__':
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

    # Load tile layers
    base_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/hhht/{z}/{x}/{y}.png"
    base_tile_layer = QgsRasterLayer(base_tile_url, "BaseTile", "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)

    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    tile_layer = QgsRasterLayer(tile_url, "MainTile", "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)

    # Add vector layer to project
    pointLayer = add_points("民警", "民警", "minjing-Point",
                            [(111.4775222, 40.7290133), (111.4766598, 40.7282033)], 5, "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAolBMVEUAAAC1xPmIn/SKn//n6/3e5PzS2vvN1vusvPeUqfWNpPUAMub////z9f6mt/by9P1Ia+2MovP6+/72+P7AzPiUqfQrVOoFNuYgTOnp7fzi5/xOcO2dr/UuV+p6lPISQOisvPejtPZ/l/IcSOje5Ptaeu9EaOybrvV3kfFTdO7X3vvI0vm9yfi6x/iDm/Jvi/BphvBVdu5Nb+05X+uPpPSOpPN4UAcsAAAAC3RSTlMA0y0M/fny7sF6UvKXmSMAAAGJSURBVDjLhZNXYoMwDEAhkGnZmGFICZBA9l7t/a9WRx6h6Qfvx0g22nLeeGN32Ke0P3THnvOfnhtAkLAwZIn8cHsf194ojgqeESTjRRSPvD+/D4BNSYspg0HLyMSnM/LBjPoT+7+fp6icX9liwa5zFMrc1za8AcX7VFBYheEKqEC5pAMVxwjQ/gYkBec1SDboBUboIGbKfiQvdpwX8ohUxCx+OXG1REJ5E+y+X++EziVyZQTBlijm+ZfGX2pVEXjOGDjRnEFzNhoOY8cNMiOKphF1LapdaDRZ4DrDhBiOAP7hkAMcrSoZOn1mJQEaYVWs79DQSiVoSqsKKT4wLABZkNYD5cImCpJ8TlouMEjLxpbZBolpWu4gWWtBp/kuVNqcAH5kHKcmbRXKCwqVQqISWOORlKbUplmPGJD9XZ3xQzXLtHtJQfF8goIusd1mYNag2e9Bs8aBMSOXVStAqkqdqyZL1cjZoV3y20XUVVWLy41L+6ka2u6x714cu3rb9+pt7ep1L2/n+v8CysQxDA9OhyUAAAAASUVORK5CYII=")
    project.addMapLayer(pointLayer)

    # Add line layer to project
    lineLayer = add_line("应急道路", [
        [(111.4857822, 40.726082), (111.4866153, 40.7256001), (111.4882815, 40.726957), (111.4901084, 40.7284965),
         (111.4901084, 40.7284965)]], "#e77148", 2, [8], ["#00cd52"], [0.4])
    project.addMapLayer(lineLayer)

    # Add polygon layer to project
    polygonLayer = add_polygon("重点区域", [[[(111.4839918, 40.7258937), (111.4855557, 40.7250408),
                                               (111.4869734, 40.7262813), (111.4855264, 40.7272782),
                                               (111.4855264, 40.7272782), (111.4839918, 40.7258937)]]], "#e77148")
    project.addMapLayer(polygonLayer)

    cir1Layer = add_circle_key_areas("防范区域", (111.477486, 40.724372), 41, (40, 30, 30),
                                     ("#ff4040", "#00cd52", "#2f99f3"), (0.4, 0.4, 0.4), 72)
    project.addMapLayer(cir1Layer)

    arrow1_layer = add_arrow("arrow1")

    # 如下是将添加到地图的图层，设置为地图视口范围
    # Create map settings and set the extent
    map_settings = QgsMapSettings()

    # Calculate the combined extent of all layers
    extent = QgsRectangle()

    projectLayers = project.mapLayers().values()
    for layer in projectLayers:
        if layer.name() not in ["MainTile", "BaseTile"]:
            extent.combineExtentWith(layer.extent())

    # Set the map canvas extent to the combined extent
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    map_settings.setExtent(extent)

    # Create a map canvas and set its extent
    canvas = QgsMapCanvas()
    canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    canvas.setExtent(extent)

    # Create and add print layout
    layout = add_print_layout(project, canvas)

    # Save project
    project.write(f"{GEOJSON_PREFIX}/demo19.qgz")

    # Export layout to image
    output_image_path = f"{GEOJSON_PREFIX}/demo19.png"
    export_layout_to_image(layout, output_image_path)

    output_pdf_path = f"{GEOJSON_PREFIX}/demo19.pdf"
    export_layout_to_pdf(layout, output_pdf_path)

    output_svg_path = f"{GEOJSON_PREFIX}/demo19.svg"
    export_layout_to_svg(layout, output_svg_path)

    # Exit QGIS application
    qgis.exitQgis()


