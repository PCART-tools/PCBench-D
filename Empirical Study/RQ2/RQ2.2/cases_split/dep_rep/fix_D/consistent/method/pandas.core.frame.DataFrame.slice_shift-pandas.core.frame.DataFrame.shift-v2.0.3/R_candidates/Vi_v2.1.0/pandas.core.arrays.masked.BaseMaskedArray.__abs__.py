    def __abs__(self) -> Self:
        return self._simple_new(abs(self._data), self._mask.copy())
