    @cached_property
    def supports_index_column_ordering(self):
        return Database.sqlite_version_info >= (3, 3, 0)
