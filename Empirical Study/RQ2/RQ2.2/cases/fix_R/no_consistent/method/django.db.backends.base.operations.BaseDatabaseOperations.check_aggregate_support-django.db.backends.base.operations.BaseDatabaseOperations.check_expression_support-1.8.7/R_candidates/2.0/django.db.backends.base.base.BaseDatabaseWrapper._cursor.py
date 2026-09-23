    def _cursor(self, name=None):
        self.ensure_connection()
        with self.wrap_database_errors:
            return self._prepare_cursor(self.create_cursor(name))
