    def _accumulate(
        self, name: str, *, skipna: bool = True, **kwargs
    ) -> BaseMaskedArray:
        data = self._data
        mask = self._mask

        op = getattr(masked_accumulations, name)
        data, mask = op(data, mask, skipna=skipna, **kwargs)

        return type(self)(data, mask, copy=False)
