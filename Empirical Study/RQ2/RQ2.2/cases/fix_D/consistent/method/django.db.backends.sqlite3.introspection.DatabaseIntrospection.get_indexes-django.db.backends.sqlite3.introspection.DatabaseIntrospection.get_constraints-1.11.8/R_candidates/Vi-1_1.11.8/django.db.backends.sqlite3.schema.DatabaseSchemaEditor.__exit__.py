    def __exit__(self, exc_type, exc_value, traceback):
        super(DatabaseSchemaEditor, self).__exit__(exc_type, exc_value, traceback)
        with self.connection.cursor() as c:
            # Restore initial FK setting - PRAGMA values can't be parametrized
            c.execute('PRAGMA foreign_keys = %s' % int(self._initial_pragma_fk))
