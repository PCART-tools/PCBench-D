    def get_placeholder(self, value, compiler, connection):
        return connection.ops.binary_placeholder_sql(value)
