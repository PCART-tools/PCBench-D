    @cached_property
    def has_fetch_offset_support(self):
        return self.connection.oracle_version >= (12, 2)
