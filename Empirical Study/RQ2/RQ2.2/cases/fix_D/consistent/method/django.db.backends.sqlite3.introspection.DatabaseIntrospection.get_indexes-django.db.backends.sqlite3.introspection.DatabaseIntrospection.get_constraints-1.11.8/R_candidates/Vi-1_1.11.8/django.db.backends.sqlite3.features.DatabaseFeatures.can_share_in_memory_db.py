    @cached_property
    def can_share_in_memory_db(self):
        return (
            six.PY3 and
            Database.__name__ == 'sqlite3.dbapi2' and
            Database.sqlite_version_info >= (3, 7, 13)
        )
