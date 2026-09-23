    def view(self, dtype=None):
        if dtype is None or dtype is self.dtype:
            return type(self)(self._data, dtype=self.dtype)
        return self._data.view(dtype=dtype)
