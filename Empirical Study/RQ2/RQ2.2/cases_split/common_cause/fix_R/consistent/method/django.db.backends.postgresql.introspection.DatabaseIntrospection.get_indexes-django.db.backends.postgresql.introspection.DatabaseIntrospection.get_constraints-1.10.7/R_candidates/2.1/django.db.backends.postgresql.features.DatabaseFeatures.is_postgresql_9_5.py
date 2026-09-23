    @cached_property
    def is_postgresql_9_5(self):
        return self.connection.pg_version >= 90500
