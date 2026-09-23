    def _commit(self):
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.connection.commit()
