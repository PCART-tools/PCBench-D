    def addError(self, test, err):
        super().addError(test, err)
        if self.debug_sql_stream is None:
            # Error before tests e.g. in setUpTestData().
            sql = ""
        else:
            self.debug_sql_stream.seek(0)
            sql = self.debug_sql_stream.read()
        self.errors[-1] = self.errors[-1] + (sql,)
