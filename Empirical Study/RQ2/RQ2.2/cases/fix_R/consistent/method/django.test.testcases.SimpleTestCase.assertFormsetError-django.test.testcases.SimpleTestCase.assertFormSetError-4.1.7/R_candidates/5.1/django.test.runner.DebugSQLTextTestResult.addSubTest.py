    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.debug_sql_stream.seek(0)
            errors = (
                self.failures
                if issubclass(err[0], test.failureException)
                else self.errors
            )
            errors[-1] = errors[-1] + (self.debug_sql_stream.read(),)
