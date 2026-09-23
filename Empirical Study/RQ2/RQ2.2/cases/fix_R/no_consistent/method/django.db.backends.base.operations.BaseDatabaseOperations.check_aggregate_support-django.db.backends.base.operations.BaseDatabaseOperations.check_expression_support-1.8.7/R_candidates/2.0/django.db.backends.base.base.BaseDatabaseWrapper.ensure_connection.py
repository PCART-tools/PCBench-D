    def ensure_connection(self):
        """Guarantee that a connection to the database is established."""
        if self.connection is None:
            with self.wrap_database_errors:
                self.connect()
