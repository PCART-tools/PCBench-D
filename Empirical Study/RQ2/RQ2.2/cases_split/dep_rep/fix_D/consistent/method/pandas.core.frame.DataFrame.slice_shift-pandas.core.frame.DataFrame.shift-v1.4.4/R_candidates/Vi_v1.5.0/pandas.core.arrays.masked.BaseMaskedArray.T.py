    @property
    def T(self: BaseMaskedArrayT) -> BaseMaskedArrayT:
        return type(self)(self._data.T, self._mask.T)
