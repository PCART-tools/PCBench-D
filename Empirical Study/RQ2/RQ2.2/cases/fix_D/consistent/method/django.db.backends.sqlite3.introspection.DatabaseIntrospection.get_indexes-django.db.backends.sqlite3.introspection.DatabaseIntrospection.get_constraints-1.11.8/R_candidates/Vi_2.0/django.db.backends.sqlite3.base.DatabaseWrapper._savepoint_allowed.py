    def _savepoint_allowed(self):
        # Two conditions are required here:
        # - A sufficiently recent version of SQLite to support savepoints,
        # - Being in a transaction, which can only happen inside 'atomic'.

        # When 'isolation_level' is not None, sqlite3 commits before each
        # savepoint; it's a bug. When it is None, savepoints don't make sense
        # because autocommit is enabled. The only exception is inside 'atomic'
        # blocks. To work around that bug, on SQLite, 'atomic' starts a
        # transaction explicitly rather than simply disable autocommit.
        return self.features.uses_savepoints and self.in_atomic_block
