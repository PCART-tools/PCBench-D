class Length(DistanceResultMixin, OracleToleranceMixin, GeoFunc):
    def __init__(self, expr1, spheroid=True, **extra):
        self.spheroid = spheroid
        super().__init__(expr1, **extra)

    def as_sql(self, compiler, connection, **extra_context):
        if self.geo_field.geodetic(connection) and not connection.features.supports_length_geodetic:
            raise NotSupportedError("This backend doesn't support Length on geodetic fields")
        return super().as_sql(compiler, connection, **extra_context)

    def as_postgresql(self, compiler, connection, **extra_context):
        clone = self.copy()
        function = None
        if self.source_is_geography():
            clone.source_expressions.append(Value(self.spheroid))
        elif self.geo_field.geodetic(connection):
            # Geometry fields with geodetic (lon/lat) coordinates need length_spheroid
            function = connection.ops.spatial_function_name('LengthSpheroid')
            clone.source_expressions.append(Value(self.geo_field.spheroid(connection)))
        else:
            dim = min(f.dim for f in self.get_source_fields() if f)
            if dim > 2:
                function = connection.ops.length3d
        return super(Length, clone).as_sql(compiler, connection, function=function, **extra_context)

    def as_sqlite(self, compiler, connection, **extra_context):
        function = None
        if self.geo_field.geodetic(connection):
            function = 'GeodesicLength' if self.spheroid else 'GreatCircleLength'
        return super().as_sql(compiler, connection, function=function, **extra_context)
