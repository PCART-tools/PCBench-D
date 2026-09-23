    def __abs__(self: BaseMaskedArrayT) -> BaseMaskedArrayT:
        return type(self)(abs(self._data), self._mask.copy())
