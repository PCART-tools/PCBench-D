    @cached_property
    def is_postgresql_14(self):
        return self.connection.pg_version >= 140000
