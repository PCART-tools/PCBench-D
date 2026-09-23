    @doc(ExtensionArray.fillna)
    def fillna(
        self: BaseMaskedArrayT, value=None, method=None, limit=None
    ) -> BaseMaskedArrayT:
        value, method = validate_fillna_kwargs(value, method)

        mask = self._mask

        if is_array_like(value):
            if len(value) != len(self):
                raise ValueError(
                    f"Length of 'value' does not match. Got ({len(value)}) "
                    f" expected {len(self)}"
                )
            value = value[mask]

        if mask.any():
            if method is not None:
                func = missing.get_fill_func(method, ndim=self.ndim)
                new_values, new_mask = func(
                    self._data.copy().T,
                    limit=limit,
                    mask=mask.copy().T,
                )
                return type(self)(new_values.T, new_mask.view(np.bool_).T)
            else:
                # fill with value
                new_values = self.copy()
                new_values[mask] = value
        else:
            new_values = self.copy()
        return new_values
