class Extent(GeoAggregate):
    name = 'Extent'
    is_extent = '2D'

    def __init__(self, expression, **extra):
        super().__init__(expression, output_field=ExtentField(), **extra)

    def convert_value(self, value, expression, connection):
        return connection.ops.convert_extent(value)
