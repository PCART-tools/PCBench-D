    @cached_property
    def is_postgresql_13(self):
        return self.connection.pg_version >= 130000
