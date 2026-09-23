    def unique(self: BaseMaskedArrayT) -> BaseMaskedArrayT:
        """
        Compute the BaseMaskedArray of unique values.

        Returns
        -------
        uniques : BaseMaskedArray
        """
        uniques, mask = algos.unique_with_mask(self._data, self._mask)
        return type(self)(uniques, mask, copy=False)
