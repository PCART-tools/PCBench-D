    def __enter__(self):
        with self.connection.cursor() as c:
            # Some SQLite schema alterations need foreign key constraints to be
            # disabled. This is the default in SQLite but can be changed with a
            # build flag and might change in future, so can't be relied upon.
            # We enforce it here for the duration of the transaction.
            c.execute('PRAGMA foreign_keys')
            self._initial_pragma_fk = c.fetchone()[0]
            c.execute('PRAGMA foreign_keys = 0')
        return super(DatabaseSchemaEditor, self).__enter__()
