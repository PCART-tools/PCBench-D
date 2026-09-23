class Area(OracleToleranceMixin, GeoFunc):
    arity = 1

    @cached_property
    def output_field(self):
        return AreaField(self.geo_field)

    def as_sql(self, compiler, connection, **extra_context):
        if not connection.features.supports_area_geodetic and self.geo_field.geodetic(connection):
            raise NotSupportedError('Area on geodetic coordinate systems not supported.')
        return super().as_sql(compiler, connection, **extra_context)

    def as_sqlite(self, compiler, connection, **extra_context):
        if self.geo_field.geodetic(connection):
            extra_context['template'] = '%(function)s(%(expressions)s, %(spheroid)d)'
            extra_context['spheroid'] = True
        return self.as_sql(compiler, connection, **extra_context)
