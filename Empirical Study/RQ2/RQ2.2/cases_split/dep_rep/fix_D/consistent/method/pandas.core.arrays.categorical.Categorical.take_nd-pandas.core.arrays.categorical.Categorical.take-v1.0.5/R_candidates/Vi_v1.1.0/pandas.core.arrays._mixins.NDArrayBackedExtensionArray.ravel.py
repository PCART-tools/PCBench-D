    def ravel(self: _T, *args, **kwargs) -> _T:
        new_data = self._ndarray.ravel(*args, **kwargs)
        return self._from_backing_data(new_data)
