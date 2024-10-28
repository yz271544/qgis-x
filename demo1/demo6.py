import os
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsField,
    QgsRasterLayer,
    QgsPointXY,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMarkerSymbol,
    QgsRasterMarkerSymbolLayer,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateTransformContext
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
    base_tile_layer = QgsRasterLayer(base_tile_url, "Base_Tile-Server", "wms")
    if base_tile_layer.isValid():
        project.addMapLayer(base_tile_layer)

    tile_url = "type=xyz&url=http://172.31.100.34:8090/gis/%E5%81%A5%E5%BA%B7%E8%B0%B7%E6%AD%A3%E5%B0%84/{z}/{x}/{y}.png"
    tile_layer = QgsRasterLayer(tile_url, "Tile-Server", "wms")
    if tile_layer.isValid():
        project.addMapLayer(tile_layer)

    # Define shapefile path
    shapefile_path = 'D:/iProject/pypath/qgis-x/output/projects/Transformed_Points.shp'

    # Create vector layer
    pointLayer = QgsVectorLayer("Point?crs=EPSG:3857", "Transformed_Points", "memory")
    pointProvider = pointLayer.dataProvider()
    pointProvider.addAttributes([QgsField("name", QVariant.String), QgsField("x", QVariant.Double), QgsField("y", QVariant.Double)])
    pointLayer.updateFields()

    # Set marker symbol to raster image type
    symbol = QgsMarkerSymbol()
    icon_path = "D:/iProject/pypath/qgis-x/common/icon/民警.png"
    raster_layer = QgsRasterMarkerSymbolLayer(icon_path)
    raster_layer.setSize(10)
    symbol.changeSymbolLayer(0, raster_layer)

    # Ensure the renderer is valid before setting the symbol
    renderer = pointLayer.renderer()
    if renderer is not None:
        renderer.setSymbol(symbol)
    else:
        print("Failed to get the renderer for the layer!")
        sys.exit(1)

    # Set coordinate transform
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    transformer = QgsCoordinateTransform(crs_4326, crs_3857, QgsProject.instance())

    # Start editing the vector layer
    pointLayer.startEditing()

    # Transform and add points
    points = [QgsPointXY(111.4775222, 40.7290133), QgsPointXY(111.4766598, 40.7282033)]
    for i, point in enumerate(points):
        transformed_point = transformer.transform(point)
        feature = QgsFeature(pointLayer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(transformed_point))
        print(f"mingjing-Point{i + 1}", transformed_point.x(), transformed_point.y())
        feature.setAttributes([f"mingjing-Point{i + 1}", transformed_point.x(), transformed_point.y()])
        pointProvider.addFeature(feature)

    # Commit changes to the vector layer
    if pointLayer.commitChanges():
        print("数据已成功提交到图层")
    else:
        print("数据提交到图层失败：" + pointProvider.error().message())

    # Save the vector layer to a shapefile
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    options.fileEncoding = "UTF-8"
    QgsVectorFileWriter.writeAsVectorFormatV2(pointLayer, shapefile_path, QgsCoordinateTransformContext(), options)

    # Load the shapefile
    pointLayer = QgsVectorLayer(shapefile_path, "Transformed_Points", "ogr")
    if not pointLayer.isValid():
        print("Failed to load the layer!")
        sys.exit(1)

    # Add vector layer to project
    project.addMapLayer(pointLayer)

    # Save project
    project.write("D:/iProject/pypath/qgis-x/output/projects/demo6.qgz")

    # Exit QGIS application
    qgis.exitQgis()