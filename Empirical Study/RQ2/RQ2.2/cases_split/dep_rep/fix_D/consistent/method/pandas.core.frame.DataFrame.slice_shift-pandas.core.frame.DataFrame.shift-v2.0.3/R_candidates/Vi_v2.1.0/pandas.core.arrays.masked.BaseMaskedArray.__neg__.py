    def __neg__(self) -> Self:
        return self._simple_new(-self._data, self._mask.copy())
