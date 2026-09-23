    @doc(ExtensionArray.fillna)
    def fillna(
        self: NDArrayBackedExtensionArrayT, value=None, method=None, limit=None
    ) -> NDArrayBackedExtensionArrayT:
        value, method = validate_fillna_kwargs(
            value, method, validate_scalar_dict_value=False
        )

        mask = self.isna()
        # error: Argument 2 to "check_value_size" has incompatible type
        # "ExtensionArray"; expected "ndarray"
        value = missing.check_value_size(
            value, mask, len(self)  # type: ignore[arg-type]
        )

        if mask.any():
            if method is not None:
                # TODO: check value is None
                # (for now) when self.ndim == 2, we assume axis=0
                func = missing.get_fill_func(method, ndim=self.ndim)
                new_values, _ = func(self._ndarray.T.copy(), limit=limit, mask=mask.T)
                new_values = new_values.T

                # TODO: PandasArray didn't used to copy, need tests for this
                new_values = self._from_backing_data(new_values)
            else:
                # fill with value
                new_values = self.copy()
                new_values[mask] = value
        else:
            # We validate the fill_value even if there is nothing to fill
            if value is not None:
                self._validate_setitem_value(value)

            new_values = self.copy()
        return new_values
