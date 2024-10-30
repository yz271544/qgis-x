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
import sys

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

    main_tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    main_tile_layer = QgsRasterLayer(main_tile_url, "Main-Tile", "wms")
    if main_tile_layer.isValid():
        project.addMapLayer(main_tile_layer)

    # Create vector layer
    pointLayer = QgsVectorLayer("Point?crs=EPSG:3857", "MinJing_Points", "memory")
    pointProvider = pointLayer.dataProvider()
    pointProvider.addAttributes([
        QgsField("name", QMetaType.Type(QVariant.String), len=254),  # Ensure field name length does not exceed 254
        QgsField("x", QMetaType.Type(QVariant.Double)),
        QgsField("y", QMetaType.Type(QVariant.Double))
    ])
    pointLayer.updateFields()

    # # Set marker symbol to raster image type
    # icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    # raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    # raster_layer.setSize(10)
    # symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
    # symbol.changeSymbolLayer(0, raster_layer)
    # renderer = QgsSingleSymbolRenderer(symbol)
    # pointLayer.setRenderer(renderer)

    # Set coordinate transform
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, project)

    # Start editing the vector layer
    pointLayer.startEditing()

    # Transform and add points
    points = [QgsPointXY(111.4775222, 40.7290133), QgsPointXY(111.4766598, 40.7282033)]
    for i, point in enumerate(points):
        transformed_point = transformer.transform(point)
        feature = QgsFeature(pointLayer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(transformed_point))
        print(f"minjing-Point{i + 1}", transformed_point.x(), transformed_point.y())
        feature.setAttributes([f"minjing-Point{i + 1}", transformed_point.x(), transformed_point.y()])
        pointProvider.addFeature(feature)

    # pointLayer.updateExtents()
    # pointLayer.triggerRepaint()

    # Commit changes to the vector layer
    if pointLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + pointProvider.error().message())

    # Save the vector layer to a shapefile
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    options.fileEncoding = "UTF-8"
    layer_output_path = '/common/output/projects/MinJing_Points.shp'
    QgsVectorFileWriter.writeAsVectorFormatV3(pointLayer, layer_output_path, QgsCoordinateTransformContext(), options)

    pointLayer = QgsVectorLayer(layer_output_path, "MinJing_Points", "ogr")
    if not pointLayer.isValid():
        print("Failed to load the layer!")
        sys.exit(1)

    # Set marker symbol to raster image type
    icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    raster_layer.setSize(5)
    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
    symbol.changeSymbolLayer(0, raster_layer)
    renderer = QgsSingleSymbolRenderer(symbol)
    pointLayer.setRenderer(renderer)

    # Add vector layer to project
    project.addMapLayer(pointLayer)

    # Save project
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo7.qgz")

    # Exit QGIS application
    qgis.exitQgis()