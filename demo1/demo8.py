import os

from qgis.core import (
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
    QgsRasterMarkerSymbolLayer,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateTransformContext,
    QgsSingleSymbolRenderer
)
from qgis.PyQt.QtCore import QVariant, QMetaType
from qgis.PyQt.QtGui import QColor
import sys


GEOJSON_PREFIX = 'D:/iProject/pypath/qgis-x/output/projects/'
ICON_PREFIX = 'D:/iProject/pypath/qgis-x/common/icon/'


def add_points(layer_name: str, icon_name: str, point_name_prefix: str, points: list[tuple[float, float]], point_size: int = 5) -> QgsVectorLayer:
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
        QgsField("name", QMetaType.Type(QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("x", QMetaType.Type(QVariant.Double)),
        QgsField("y", QMetaType.Type(QVariant.Double))
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
    geojson_path = GEOJSON_PREFIX + f'{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(pointLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    pointLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not pointLayer.isValid():
        print("Failed to load the layer!")
        sys.exit(1)
    # icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    icon_path = ICON_PREFIX + f'{icon_name}.png'
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
    geojson_path = GEOJSON_PREFIX + f'{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(lineLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    lineLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not lineLayer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
    # symbol.setColor("#e77148")
    symbol.setColor(QColor(color))
    symbol.setWidth(2)
    renderer = QgsSingleSymbolRenderer(symbol)
    lineLayer.setRenderer(renderer)

    return lineLayer



def add_polygon(layer_name: str, polygons: list[list[list[tuple[float, float]]]], color: str) -> QgsVectorLayer:
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
    geojson_path = GEOJSON_PREFIX + f'{layer_name}.geojson'
    QgsVectorFileWriter.writeAsVectorFormatV3(polygonLayer, geojson_path, QgsCoordinateTransformContext(), options)
    # Load the GeoJSON file
    polygonLayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
    if not polygonLayer.isValid():
        print("Failed to load the lineLayer!")
        sys.exit(1)

    # Set line style, exp: color, stroke width
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
    # symbol.setColor("#e77148")
    symbol.setColor(QColor(color))
    symbol.setOpacity(0.5)
    renderer = QgsSingleSymbolRenderer(symbol)
    polygonLayer.setRenderer(renderer)

    return polygonLayer


if __name__ == '__main__':
    qgis = QgsApplication([], False)
    qgis.initQgis()

    # Create project instance
    project = QgsProject.instance()

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
    pointLayer = add_points("MinJing_Points", "民警", "minjing-Point", [(111.4775222, 40.7290133), (111.4766598, 40.7282033)])
    project.addMapLayer(pointLayer)

    # Add line layer to project
    lineLayer = add_line("yingji", [[(111.4857822, 40.726082), (111.4866153, 40.7256001), (111.4882815, 40.726957), (111.4901084, 40.7284965), (111.4901084, 40.7284965)]], "#e77148")
    project.addMapLayer(lineLayer)

    # Add polygon layer to project
    polygonLayer = add_polygon("zhongdian", [[[(111.4839918, 40.7258937), (111.4855557, 40.7250408), (111.4869734, 40.7262813), (111.4855264, 40.7272782), (111.4855264, 40.7272782), (111.4839918, 40.7258937)]]], "#e77148")
    project.addMapLayer(polygonLayer)

    # Save project
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo8.qgz")

    # Exit QGIS application
    qgis.exitQgis()
