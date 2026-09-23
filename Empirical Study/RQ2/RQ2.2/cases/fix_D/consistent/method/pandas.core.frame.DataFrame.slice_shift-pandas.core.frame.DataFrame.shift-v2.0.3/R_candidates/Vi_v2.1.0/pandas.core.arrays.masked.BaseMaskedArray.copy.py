    def copy(self) -> Self:
        data = self._data.copy()
        mask = self._mask.copy()
        return self._simple_new(data, mask)
