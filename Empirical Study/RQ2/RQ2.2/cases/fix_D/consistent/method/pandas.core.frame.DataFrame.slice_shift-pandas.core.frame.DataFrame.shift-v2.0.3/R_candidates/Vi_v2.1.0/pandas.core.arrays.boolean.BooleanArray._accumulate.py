    def _accumulate(
        self, name: str, *, skipna: bool = True, **kwargs
    ) -> BaseMaskedArray:
        data = self._data
        mask = self._mask
        if name in ("cummin", "cummax"):
            op = getattr(masked_accumulations, name)
            data, mask = op(data, mask, skipna=skipna, **kwargs)
            return self._simple_new(data, mask)
        else:
            from pandas.core.arrays import IntegerArray

            return IntegerArray(data.astype(int), mask)._accumulate(
                name, skipna=skipna, **kwargs
            )
