    def copy(self: _T) -> _T:
        new_data = self._ndarray.copy()
        return self._from_backing_data(new_data)
