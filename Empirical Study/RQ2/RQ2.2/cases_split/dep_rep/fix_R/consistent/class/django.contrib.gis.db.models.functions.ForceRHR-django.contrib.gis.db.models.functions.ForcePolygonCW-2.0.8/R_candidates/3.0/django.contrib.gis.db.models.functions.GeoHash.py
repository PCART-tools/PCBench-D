class GeoHash(GeoFunc):
    output_field = TextField()

    def __init__(self, expression, precision=None, **extra):
        expressions = [expression]
        if precision is not None:
            expressions.append(self._handle_param(precision, 'precision', int))
        super().__init__(*expressions, **extra)

    def as_mysql(self, compiler, connection, **extra_context):
        clone = self.copy()
        # If no precision is provided, set it to the maximum.
        if len(clone.source_expressions) < 2:
            clone.source_expressions.append(Value(100))
        return clone.as_sql(compiler, connection, **extra_context)
