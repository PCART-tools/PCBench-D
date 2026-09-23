    @property
    def T(self: _T) -> _T:
        new_data = self._ndarray.T
        return self._from_backing_data(new_data)
