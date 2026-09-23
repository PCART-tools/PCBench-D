    def aggregate(self, values, how, axis=0):
        return self._cython_operation('aggregate', values, how, axis)
