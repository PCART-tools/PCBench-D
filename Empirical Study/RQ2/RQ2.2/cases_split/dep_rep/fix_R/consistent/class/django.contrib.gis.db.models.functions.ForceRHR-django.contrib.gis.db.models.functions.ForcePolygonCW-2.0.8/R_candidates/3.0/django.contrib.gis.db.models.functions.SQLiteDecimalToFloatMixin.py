class SQLiteDecimalToFloatMixin:
    """
    By default, Decimal values are converted to str by the SQLite backend, which
    is not acceptable by the GIS functions expecting numeric values.
    """
    def as_sqlite(self, compiler, connection, **extra_context):
        for expr in self.get_source_expressions():
            if hasattr(expr, 'value') and isinstance(expr.value, Decimal):
                expr.value = float(expr.value)
        return super().as_sql(compiler, connection, **extra_context)
