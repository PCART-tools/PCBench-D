    @cached_property
    def oracle_full_version(self):
        with self.temporary_connection():
            return self.connection.version
