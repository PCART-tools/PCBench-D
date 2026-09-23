class AsKML(AsGML):
    def as_sqlite(self, compiler, connection, **extra_context):
        # No version parameter
        clone = self.copy()
        clone.set_source_expressions(self.get_source_expressions()[1:])
        return clone.as_sql(compiler, connection, **extra_context)
