class Collect(GeoAggregate):
    name = 'Collect'
    output_field_class = GeometryCollectionField
