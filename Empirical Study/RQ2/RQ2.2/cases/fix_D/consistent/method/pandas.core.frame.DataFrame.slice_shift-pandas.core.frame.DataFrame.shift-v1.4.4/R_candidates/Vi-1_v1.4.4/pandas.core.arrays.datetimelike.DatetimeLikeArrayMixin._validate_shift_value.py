    def _validate_shift_value(self, fill_value):
        # TODO(2.0): once this deprecation is enforced, use _validate_scalar
        if is_valid_na_for_dtype(fill_value, self.dtype):
            fill_value = NaT
        elif isinstance(fill_value, self._recognized_scalars):
            fill_value = self._scalar_type(fill_value)
        else:
            new_fill: DatetimeLikeScalar

            # only warn if we're not going to raise
            if self._scalar_type is Period and lib.is_integer(fill_value):
                # kludge for #31971 since Period(integer) tries to cast to str
                new_fill = Period._from_ordinal(fill_value, freq=self.freq)
            else:
                new_fill = self._scalar_type(fill_value)

            # stacklevel here is chosen to be correct when called from
            #  DataFrame.shift or Series.shift
            warnings.warn(
                f"Passing {type(fill_value)} to shift is deprecated and "
                "will raise in a future version, pass "
                f"{self._scalar_type.__name__} instead.",
                FutureWarning,
                # There is no way to hard-code the level since this might be
                #  reached directly or called from the Index or Block method
                stacklevel=find_stack_level(),
            )
            fill_value = new_fill

        return self._unbox(fill_value, setitem=True)
