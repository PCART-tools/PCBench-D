    @cache_readonly
    def _engine(self):
        # we are going to look things up with the codes themselves.
        # To avoid a reference cycle, bind `codes` to a local variable, so
        # `self` is not passed into the lambda.
        codes = self.codes
        return self._engine_type(lambda: codes, len(self))
