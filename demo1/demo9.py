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
    pointLayer = add_points("MinJing_Points", "民警", "minjing-Point",
                            [(111.4775222, 40.7290133), (111.4766598, 40.7282033)])
    project.addMapLayer(pointLayer)

    # Add line layer to project
    lineLayer = add_line("yingji", [
        [(111.4857822, 40.726082), (111.4866153, 40.7256001), (111.4882815, 40.726957), (111.4901084, 40.7284965),
         (111.4901084, 40.7284965)]], "#e77148")
    project.addMapLayer(lineLayer)

    # Add polygon layer to project
    polygonLayer = add_polygon("zhongdian", [[[(111.4839918, 40.7258937), (111.4855557, 40.7250408),
                                               (111.4869734, 40.7262813), (111.4855264, 40.7272782),
                                               (111.4855264, 40.7272782), (111.4839918, 40.7258937)]]], "#e77148")
    project.addMapLayer(polygonLayer)

    # Add polygon layer to project
    polygonLayerCir1 = add_polygon("cir1", [[
        [(111.4781697, 40.7251671)], [(111.478166, 40.725167)], [(111.4781622, 40.725167)],
        [(111.4781585, 40.7251668)], [(111.4781547, 40.7251667)], [(111.478151, 40.7251664)],
        [(111.4781473, 40.7251662)], [(111.4781435, 40.7251658)], [(111.4781398, 40.7251655)],
        [(111.4781361, 40.725165)], [(111.4781324, 40.7251646)], [(111.4781287, 40.7251641)],
        [(111.4781251, 40.7251635)], [(111.4781214, 40.7251629)], [(111.4781178, 40.7251622)],
        [(111.4781141, 40.7251615)], [(111.4781105, 40.7251607)], [(111.4781069, 40.7251599)],
        [(111.4781034, 40.7251591)], [(111.4780998, 40.7251582)], [(111.4780963, 40.7251572)],
        [(111.4780928, 40.7251562)], [(111.4780893, 40.7251552)], [(111.4780858, 40.7251541)],
        [(111.4780824, 40.725153)], [(111.478079, 40.7251518)], [(111.4780756, 40.7251506)],
        [(111.4780723, 40.7251493)], [(111.4780689, 40.725148)], [(111.4780656, 40.7251467)],
        [(111.4780624, 40.7251453)], [(111.4780592, 40.7251438)], [(111.478056, 40.7251423)],
        [(111.4780528, 40.7251408)], [(111.4780497, 40.7251392)], [(111.4780466, 40.7251376)],
        [(111.4780435, 40.725136)], [(111.4780405, 40.7251343)], [(111.4780376, 40.7251326)],
        [(111.4780346, 40.7251308)], [(111.4780317, 40.725129)], [(111.4780289, 40.7251272)],
        [(111.4780261, 40.7251253)], [(111.4780233, 40.7251234)], [(111.4780206, 40.7251214)],
        [(111.4780179, 40.7251194)], [(111.4780153, 40.7251174)], [(111.4780127, 40.7251153)],
        [(111.4780102, 40.7251132)], [(111.4780077, 40.7251111)], [(111.4780053, 40.7251089)],
        [(111.4780029, 40.7251068)], [(111.4780006, 40.7251045)], [(111.4779983, 40.7251023)],
        [(111.4779961, 40.7251)], [(111.4779939, 40.7250977)], [(111.4779918, 40.7250954)],
        [(111.4779897, 40.725093)], [(111.4779877, 40.7250906)], [(111.4779857, 40.7250882)],
        [(111.4779838, 40.7250857)], [(111.477982, 40.7250833)], [(111.4779802, 40.7250808)],
        [(111.4779785, 40.7250782)], [(111.4779768, 40.7250757)], [(111.4779752, 40.7250731)],
        [(111.4779736, 40.7250706)], [(111.4779721, 40.725068)], [(111.4779707, 40.7250653)],
        [(111.4779693, 40.7250627)], [(111.477968, 40.72506)], [(111.4779668, 40.7250574)],
        [(111.4779656, 40.7250547)], [(111.4779645, 40.725052)], [(111.4779634, 40.7250492)],
        [(111.4779624, 40.7250465)], [(111.4779614, 40.7250437)], [(111.4779606, 40.725041)],
        [(111.4779598, 40.7250382)], [(111.477959, 40.7250354)], [(111.4779583, 40.7250326)],
        [(111.4779577, 40.7250298)], [(111.4779572, 40.725027)], [(111.4779567, 40.7250242)],
        [(111.4779562, 40.7250214)], [(111.4779559, 40.7250186)], [(111.4779556, 40.7250157)],
        [(111.4779554, 40.7250129)], [(111.4779552, 40.7250101)], [(111.4779551, 40.7250072)],
        [(111.4779551, 40.7250044)], [(111.4779551, 40.7250016)], [(111.4779552, 40.7249987)],
        [(111.4779554, 40.7249959)], [(111.4779556, 40.7249931)], [(111.4779559, 40.7249902)],
        [(111.4779562, 40.7249874)], [(111.4779567, 40.7249846)], [(111.4779572, 40.7249818)],
        [(111.4779577, 40.724979)], [(111.4779583, 40.7249762)], [(111.477959, 40.7249734)],
        [(111.4779598, 40.7249706)], [(111.4779606, 40.7249678)], [(111.4779614, 40.724965)],
        [(111.4779624, 40.7249623)], [(111.4779634, 40.7249596)], [(111.4779645, 40.7249568)],
        [(111.4779656, 40.7249541)], [(111.4779668, 40.7249514)], [(111.477968, 40.7249488)],
        [(111.4779693, 40.7249461)], [(111.4779707, 40.7249435)], [(111.4779721, 40.7249408)],
        [(111.4779736, 40.7249382)], [(111.4779752, 40.7249357)], [(111.4779768, 40.7249331)],
        [(111.4779785, 40.7249306)], [(111.4779802, 40.724928)], [(111.477982, 40.7249255)],
        [(111.4779838, 40.7249231)], [(111.4779857, 40.7249206)], [(111.4779877, 40.7249182)],
        [(111.4779897, 40.7249158)], [(111.4779918, 40.7249134)], [(111.4779939, 40.7249111)],
        [(111.4779961, 40.7249088)], [(111.4779983, 40.7249065)], [(111.4780006, 40.7249043)],
        [(111.4780029, 40.724902)], [(111.4780053, 40.7248998)], [(111.4780077, 40.7248977)],
        [(111.4780102, 40.7248956)], [(111.4780127, 40.7248935)], [(111.4780153, 40.7248914)],
        [(111.4780179, 40.7248894)], [(111.4780206, 40.7248874)], [(111.4780233, 40.7248854)],
        [(111.4780261, 40.7248835)], [(111.4780289, 40.7248816)], [(111.4780317, 40.7248798)],
        [(111.4780346, 40.724878)], [(111.4780376, 40.7248762)], [(111.4780405, 40.7248745)],
        [(111.4780435, 40.7248728)], [(111.4780466, 40.7248712)], [(111.4780497, 40.7248696)],
        [(111.4780528, 40.724868)], [(111.478056, 40.7248665)], [(111.4780592, 40.724865)],
        [(111.4780624, 40.7248635)], [(111.4780656, 40.7248621)], [(111.4780689, 40.7248608)],
        [(111.4780723, 40.7248595)], [(111.4780756, 40.7248582)], [(111.478079, 40.724857)],
        [(111.4780824, 40.7248558)], [(111.4780858, 40.7248547)], [(111.4780893, 40.7248536)],
        [(111.4780928, 40.7248525)], [(111.4780963, 40.7248516)], [(111.4780998, 40.7248506)],
        [(111.4781034, 40.7248497)], [(111.4781069, 40.7248489)], [(111.4781105, 40.724848)],
        [(111.4781141, 40.7248473)], [(111.4781178, 40.7248466)], [(111.4781214, 40.7248459)],
        [(111.4781251, 40.7248453)], [(111.4781287, 40.7248447)], [(111.4781324, 40.7248442)],
        [(111.4781361, 40.7248437)], [(111.4781398, 40.7248433)], [(111.4781435, 40.724843)],
        [(111.4781473, 40.7248426)], [(111.478151, 40.7248424)], [(111.4781547, 40.7248421)],
        [(111.4781585, 40.724842)], [(111.4781622, 40.7248418)], [(111.478166, 40.7248418)],
        [(111.4781697, 40.7248417)], [(111.4781734, 40.7248418)], [(111.4781772, 40.7248418)],
        [(111.4781809, 40.724842)], [(111.4781847, 40.7248421)], [(111.4781884, 40.7248424)],
        [(111.4781921, 40.7248426)], [(111.4781959, 40.724843)], [(111.4781996, 40.7248433)],
        [(111.4782033, 40.7248437)], [(111.478207, 40.7248442)], [(111.4782106, 40.7248447)],
        [(111.4782143, 40.7248453)], [(111.478218, 40.7248459)], [(111.4782216, 40.7248466)],
        [(111.4782252, 40.7248473)], [(111.4782289, 40.724848)], [(111.4782324, 40.7248489)],
        [(111.478236, 40.7248497)], [(111.4782396, 40.7248506)], [(111.4782431, 40.7248516)],
        [(111.4782466, 40.7248525)], [(111.4782501, 40.7248536)], [(111.4782536, 40.7248547)],
        [(111.478257, 40.7248558)], [(111.4782604, 40.724857)], [(111.4782638, 40.7248582)],
        [(111.4782671, 40.7248595)], [(111.4782705, 40.7248608)], [(111.4782737, 40.7248621)],
        [(111.478277, 40.7248635)], [(111.4782802, 40.724865)], [(111.4782834, 40.7248665)],
        [(111.4782866, 40.724868)], [(111.4782897, 40.7248696)], [(111.4782928, 40.7248712)],
        [(111.4782959, 40.7248728)], [(111.4782989, 40.7248745)], [(111.4783018, 40.7248762)],
        [(111.4783048, 40.724878)], [(111.4783077, 40.7248798)], [(111.4783105, 40.7248816)],
        [(111.4783133, 40.7248835)], [(111.4783161, 40.7248854)], [(111.4783188, 40.7248874)],
        [(111.4783215, 40.7248894)], [(111.4783241, 40.7248914)], [(111.4783267, 40.7248935)],
        [(111.4783292, 40.7248956)], [(111.4783317, 40.7248977)], [(111.4783341, 40.7248998)],
        [(111.4783365, 40.724902)], [(111.4783388, 40.7249043)], [(111.4783411, 40.7249065)],
        [(111.4783433, 40.7249088)], [(111.4783455, 40.7249111)], [(111.4783476, 40.7249134)],
        [(111.4783497, 40.7249158)], [(111.4783517, 40.7249182)], [(111.4783537, 40.7249206)],
        [(111.4783556, 40.7249231)], [(111.4783574, 40.7249255)], [(111.4783592, 40.724928)],
        [(111.4783609, 40.7249306)], [(111.4783626, 40.7249331)], [(111.4783642, 40.7249357)],
        [(111.4783658, 40.7249382)], [(111.4783673, 40.7249408)], [(111.4783687, 40.7249435)],
        [(111.4783701, 40.7249461)], [(111.4783714, 40.7249488)], [(111.4783726, 40.7249514)],
        [(111.4783738, 40.7249541)], [(111.4783749, 40.7249568)], [(111.478376, 40.7249596)],
        [(111.478377, 40.7249623)], [(111.4783779, 40.724965)], [(111.4783788, 40.7249678)],
        [(111.4783796, 40.7249706)], [(111.4783804, 40.7249734)], [(111.4783811, 40.7249762)],
        [(111.4783817, 40.724979)], [(111.4783822, 40.7249818)], [(111.4783827, 40.7249846)],
        [(111.4783831, 40.7249874)], [(111.4783835, 40.7249902)], [(111.4783838, 40.7249931)],
        [(111.478384, 40.7249959)], [(111.4783842, 40.7249987)], [(111.4783843, 40.7250016)],
        [(111.4783843, 40.7250044)], [(111.4783843, 40.7250072)], [(111.4783842, 40.7250101)],
        [(111.478384, 40.7250129)], [(111.4783838, 40.7250157)], [(111.4783835, 40.7250186)],
        [(111.4783831, 40.7250214)], [(111.4783827, 40.7250242)], [(111.4783822, 40.725027)],
        [(111.4783817, 40.7250298)], [(111.4783811, 40.7250326)], [(111.4783804, 40.7250354)],
        [(111.4783796, 40.7250382)], [(111.4783788, 40.725041)], [(111.4783779, 40.7250437)],
        [(111.478377, 40.7250465)], [(111.478376, 40.7250492)], [(111.4783749, 40.725052)],
        [(111.4783738, 40.7250547)], [(111.4783726, 40.7250574)], [(111.4783714, 40.72506)],
        [(111.4783701, 40.7250627)], [(111.4783687, 40.7250653)], [(111.4783673, 40.725068)],
        [(111.4783658, 40.7250706)], [(111.4783642, 40.7250731)], [(111.4783626, 40.7250757)],
        [(111.4783609, 40.7250782)], [(111.4783592, 40.7250808)], [(111.4783574, 40.7250833)],
        [(111.4783556, 40.7250857)], [(111.4783537, 40.7250882)], [(111.4783517, 40.7250906)],
        [(111.4783497, 40.725093)], [(111.4783476, 40.7250954)], [(111.4783455, 40.7250977)],
        [(111.4783433, 40.7251)], [(111.4783411, 40.7251023)], [(111.4783388, 40.7251045)],
        [(111.4783365, 40.7251068)], [(111.4783341, 40.7251089)], [(111.4783317, 40.7251111)],
        [(111.4783292, 40.7251132)], [(111.4783267, 40.7251153)], [(111.4783241, 40.7251174)],
        [(111.4783215, 40.7251194)], [(111.4783188, 40.7251214)], [(111.4783161, 40.7251234)],
        [(111.4783133, 40.7251253)], [(111.4783105, 40.7251272)], [(111.4783077, 40.725129)],
        [(111.4783048, 40.7251308)], [(111.4783018, 40.7251326)], [(111.4782989, 40.7251343)],
        [(111.4782959, 40.725136)], [(111.4782928, 40.7251376)], [(111.4782897, 40.7251392)],
        [(111.4782866, 40.7251408)], [(111.4782834, 40.7251423)], [(111.4782802, 40.7251438)],
        [(111.478277, 40.7251453)], [(111.4782737, 40.7251467)], [(111.4782705, 40.725148)],
        [(111.4782671, 40.7251493)], [(111.4782638, 40.7251506)], [(111.4782604, 40.7251518)],
        [(111.478257, 40.725153)], [(111.4782536, 40.7251541)], [(111.4782501, 40.7251552)],
        [(111.4782466, 40.7251562)], [(111.4782431, 40.7251572)], [(111.4782396, 40.7251582)],
        [(111.478236, 40.7251591)], [(111.4782324, 40.7251599)], [(111.4782289, 40.7251607)],
        [(111.4782252, 40.7251615)], [(111.4782216, 40.7251622)], [(111.478218, 40.7251629)],
        [(111.4782143, 40.7251635)], [(111.4782106, 40.7251641)], [(111.478207, 40.7251646)],
        [(111.4782033, 40.725165)], [(111.4781996, 40.7251655)], [(111.4781959, 40.7251658)],
        [(111.4781921, 40.7251662)], [(111.4781884, 40.7251664)], [(111.4781847, 40.7251667)],
        [(111.4781809, 40.7251668)], [(111.4781772, 40.725167)], [(111.4781734, 40.725167)],
        [(111.4781697, 40.7251671)]
    ]], "#2f99f3")
    project.addMapLayer(polygonLayerCir1)

    # Save project
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo8.qgz")

    # Exit QGIS application
    qgis.exitQgis()
