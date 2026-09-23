class GeoAggregate(Aggregate):
    function = None
    is_extent = False

    @cached_property
    def output_field(self):
        return self.output_field_class(self.source_expressions[0].output_field.srid)

    def as_sql(self, compiler, connection, function=None, **extra_context):
        # this will be called again in parent, but it's needed now - before
        # we get the spatial_aggregate_name
        connection.ops.check_expression_support(self)
        return super().as_sql(
            compiler,
            connection,
            function=function or connection.ops.spatial_aggregate_name(self.name),
            **extra_context
        )

    def as_oracle(self, compiler, connection, **extra_context):
        tolerance = self.extra.get('tolerance') or getattr(self, 'tolerance', 0.05)
        template = None if self.is_extent else '%(function)s(SDOAGGRTYPE(%(expressions)s,%(tolerance)s))'
        return self.as_sql(compiler, connection, template=template, tolerance=tolerance, **extra_context)

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        c = super().resolve_expression(query, allow_joins, reuse, summarize, for_save)
        for expr in c.get_source_expressions():
            if not hasattr(expr.field, 'geom_type'):
                raise ValueError('Geospatial aggregates only allowed on geometry fields.')
        return c
