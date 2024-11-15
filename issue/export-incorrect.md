# After customizing the legend, the exported png/pdf/svg is incorrect


hi, I used `QgsPointClusterRenderer` and embedded a `QgsRuleBasedRenderer` to modify the point layer. But when outputting the layout, it put the text and the set offset and other styles into the legend.

```python
def add_points(layer_name: str, icon_name: str, point_name_prefix: str, points: list[tuple[float, float]],
               point_size: int = 5, icon_base64: str = "") -> QgsVectorLayer:
    """
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
        print("commit successed")
    else:
        print("commit failed：" + point_provider.error().message())
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

    # create QgsRuleBasedRenderer 
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

    # create QgsPointClusterRenderer 
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
    # embed the RuleBasedRenderer
    cluster_renderer.setEmbeddedRenderer(rule_renderer)

    point_layer.setRenderer(cluster_renderer)

    point_layer.triggerRepaint()

    return point_layer
```

So, I wrote a custom legend method to filter out the redundant FontMarker from the custom symbol of the legend element.

```python
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

```

Finally, I opened the generated qgz file with qgis, and it looked correct. But the only problem is that when exporting png/pdf/svg, it still carries the FontMarker that has not been filtered out.

CASE WHEN @cluster_size=0 THEN name ELSE concat('(', @cluster_size, ')') END