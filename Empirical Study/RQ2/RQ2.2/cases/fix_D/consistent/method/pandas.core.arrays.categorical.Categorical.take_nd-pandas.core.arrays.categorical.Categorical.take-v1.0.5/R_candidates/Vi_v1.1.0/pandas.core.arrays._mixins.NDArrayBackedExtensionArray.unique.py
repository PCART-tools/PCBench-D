    def unique(self: _T) -> _T:
        new_data = unique(self._ndarray)
        return self._from_backing_data(new_data)
