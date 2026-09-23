    @property
    def T(self) -> Self:
        return self._simple_new(self._data.T, self._mask.T)
