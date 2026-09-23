    def transform(self, values, how, axis=0):
        return self._cython_operation('transform', values, how, axis)
