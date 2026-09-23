    @cached_property
    def is_postgresql_12(self):
        return self.connection.pg_version >= 120000
