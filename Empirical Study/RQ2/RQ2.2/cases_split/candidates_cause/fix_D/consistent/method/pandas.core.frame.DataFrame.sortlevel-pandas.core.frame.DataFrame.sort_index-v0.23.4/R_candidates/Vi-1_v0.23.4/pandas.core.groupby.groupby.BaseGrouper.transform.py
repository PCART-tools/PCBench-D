    def transform(self, values, how, axis=0, **kwargs):
        return self._cython_operation('transform', values, how, axis, **kwargs)
