    def __invert__(self: BaseMaskedArrayT) -> BaseMaskedArrayT:
        return type(self)(~self._data, self._mask.copy())
