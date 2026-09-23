    def _commit(self):
        if self.connection is not None:
            with wrap_oracle_errors():
                return self.connection.commit()
