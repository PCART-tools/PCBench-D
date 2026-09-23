    def swapaxes(self: BaseMaskedArrayT, axis1, axis2) -> BaseMaskedArrayT:
        data = self._data.swapaxes(axis1, axis2)
        mask = self._mask.swapaxes(axis1, axis2)
        return type(self)(data, mask)
