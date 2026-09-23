    def _validate_shift_value(self, fill_value):
        # TODO(2.0): once this deprecation is enforced, use _validate_fill_value
        if is_valid_nat_for_dtype(fill_value, self.dtype):
            fill_value = NaT
        elif isinstance(fill_value, self._recognized_scalars):
            fill_value = self._scalar_type(fill_value)
        else:
            # only warn if we're not going to raise
            if self._scalar_type is Period and lib.is_integer(fill_value):
                # kludge for #31971 since Period(integer) tries to cast to str
                new_fill = Period._from_ordinal(fill_value, freq=self.dtype.freq)
            else:
                new_fill = self._scalar_type(fill_value)

            # stacklevel here is chosen to be correct when called from
            #  DataFrame.shift or Series.shift
            warnings.warn(
                f"Passing {type(fill_value)} to shift is deprecated and "
                "will raise in a future version, pass "
                f"{self._scalar_type.__name__} instead.",
                FutureWarning,
                stacklevel=8,
            )
            fill_value = new_fill

        return self._unbox(fill_value)
