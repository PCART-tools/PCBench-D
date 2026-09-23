    def fillna(self, value=None, method=None, limit=None):
        # TODO(GH-20300): remove this
        # Just overriding to ensure that we avoid an astype(object).
        # Either 20300 or a `_values_for_fillna` would avoid this duplication.
        if isinstance(value, ABCSeries):
            value = value.array

        value, method = validate_fillna_kwargs(value, method)

        mask = self.isna()

        if is_array_like(value):
            if len(value) != len(self):
                raise ValueError(
                    "Length of 'value' does not match. Got ({}) "
                    " expected {}".format(len(value), len(self))
                )
            value = value[mask]

        if mask.any():
            if method is not None:
                if method == "pad":
                    func = missing.pad_1d
                else:
                    func = missing.backfill_1d

                values = self._data
                if not is_period_dtype(self):
                    # For PeriodArray self._data is i8, which gets copied
                    #  by `func`.  Otherwise we need to make a copy manually
                    # to avoid modifying `self` in-place.
                    values = values.copy()

                new_values = func(values, limit=limit, mask=mask)
                if is_datetime64tz_dtype(self):
                    # we need to pass int64 values to the constructor to avoid
                    #  re-localizing incorrectly
                    new_values = new_values.view("i8")
                new_values = type(self)(new_values, dtype=self.dtype)
            else:
                # fill with value
                new_values = self.copy()
                new_values[mask] = value
        else:
            new_values = self.copy()
        return new_values
