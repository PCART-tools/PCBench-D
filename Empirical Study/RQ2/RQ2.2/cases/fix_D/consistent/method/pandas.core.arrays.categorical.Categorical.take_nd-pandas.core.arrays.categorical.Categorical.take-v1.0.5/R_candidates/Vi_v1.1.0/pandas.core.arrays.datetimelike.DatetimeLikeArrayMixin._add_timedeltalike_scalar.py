    def _add_timedeltalike_scalar(self, other):
        """
        Add a delta of a timedeltalike

        Returns
        -------
        Same type as self
        """
        if isna(other):
            # i.e np.timedelta64("NaT"), not recognized by delta_to_nanoseconds
            new_values = np.empty(self.shape, dtype="i8")
            new_values[:] = iNaT
            return type(self)(new_values, dtype=self.dtype)

        inc = delta_to_nanoseconds(other)
        new_values = checked_add_with_arr(self.asi8, inc, arr_mask=self._isnan).view(
            "i8"
        )
        new_values = self._maybe_mask_results(new_values)

        new_freq = None
        if isinstance(self.freq, Tick) or is_period_dtype(self.dtype):
            # adding a scalar preserves freq
            new_freq = self.freq

        return type(self)(new_values, dtype=self.dtype, freq=new_freq)
