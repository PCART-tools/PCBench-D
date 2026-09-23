    def transform(self, values, how: str, axis: int = 0, **kwargs):
        return self._cython_operation("transform", values, how, axis, **kwargs)
