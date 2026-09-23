    @Appender(ExtensionArray.shift.__doc__)
    def shift(self, periods=1, fill_value=None, axis=0):
        if not self.size or periods == 0:
            return self.copy()

        if is_valid_nat_for_dtype(fill_value, self.dtype):
            fill_value = NaT
        elif not isinstance(fill_value, self._recognized_scalars):
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
                stacklevel=7,
            )
            fill_value = new_fill

        fill_value = self._unbox_scalar(fill_value)

        new_values = self._data

        # make sure array sent to np.roll is c_contiguous
        f_ordered = new_values.flags.f_contiguous
        if f_ordered:
            new_values = new_values.T
            axis = new_values.ndim - axis - 1

        new_values = np.roll(new_values, periods, axis=axis)

        axis_indexer = [slice(None)] * self.ndim
        if periods > 0:
            axis_indexer[axis] = slice(None, periods)
        else:
            axis_indexer[axis] = slice(periods, None)
        new_values[tuple(axis_indexer)] = fill_value

        # restore original order
        if f_ordered:
            new_values = new_values.T

        return type(self)._simple_new(new_values, dtype=self.dtype)
