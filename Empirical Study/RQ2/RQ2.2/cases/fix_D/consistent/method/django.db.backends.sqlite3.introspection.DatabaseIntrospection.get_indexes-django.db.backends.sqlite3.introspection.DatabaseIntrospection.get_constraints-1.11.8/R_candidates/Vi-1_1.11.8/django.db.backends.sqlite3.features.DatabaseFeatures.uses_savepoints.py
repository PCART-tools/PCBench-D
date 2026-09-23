    @cached_property
    def uses_savepoints(self):
        return Database.sqlite_version_info >= (3, 6, 8)
