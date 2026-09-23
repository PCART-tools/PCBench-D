    def delete(self: BaseMaskedArrayT, loc, axis: int = 0) -> BaseMaskedArrayT:
        data = np.delete(self._data, loc, axis=axis)
        mask = np.delete(self._mask, loc, axis=axis)
        return type(self)(data, mask)
