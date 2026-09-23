    @cache_readonly
    def _engine(self):
        # property, for now, slow to look up

        # to avoid a reference cycle, bind `_ndarray_values` to a local variable, so
        # `self` is not passed into the lambda.
        _ndarray_values = self._ndarray_values
        return self._engine_type(lambda: _ndarray_values, len(self))
