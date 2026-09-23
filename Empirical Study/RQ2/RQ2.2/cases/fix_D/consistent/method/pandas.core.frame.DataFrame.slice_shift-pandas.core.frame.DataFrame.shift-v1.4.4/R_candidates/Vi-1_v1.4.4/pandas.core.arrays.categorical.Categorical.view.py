    def view(self, dtype=None):
        if dtype is not None:
            raise NotImplementedError(dtype)
        return self._from_backing_data(self._ndarray)
