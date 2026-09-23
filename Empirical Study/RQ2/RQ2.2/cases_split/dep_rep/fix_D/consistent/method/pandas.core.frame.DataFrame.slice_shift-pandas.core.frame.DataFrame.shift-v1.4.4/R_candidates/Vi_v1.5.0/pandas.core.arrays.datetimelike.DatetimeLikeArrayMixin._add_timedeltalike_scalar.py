    def _add_timedeltalike_scalar(self, other):
        """
        Add a delta of a timedeltalike

        Returns
        -------
        Same type as self
        """
        if isna(other):
            # i.e np.timedelta64("NaT"), not recognized by delta_to_nanoseconds
            new_values = np.empty(self.shape, dtype="i8").view(self._ndarray.dtype)
            new_values.fill(iNaT)
            return type(self)._simple_new(new_values, dtype=self.dtype)

        # PeriodArray overrides, so we only get here with DTA/TDA
        # error: "DatetimeLikeArrayMixin" has no attribute "_reso"
        inc = delta_to_nanoseconds(other, reso=self._reso)  # type: ignore[attr-defined]

        new_values = checked_add_with_arr(self.asi8, inc, arr_mask=self._isnan)
        new_values = new_values.view(self._ndarray.dtype)

        new_freq = None
        if isinstance(self.freq, Tick) or is_period_dtype(self.dtype):
            # adding a scalar preserves freq
            new_freq = self.freq

        # error: Unexpected keyword argument "freq" for "_simple_new" of "NDArrayBacked"
        return type(self)._simple_new(  # type: ignore[call-arg]
            new_values, dtype=self.dtype, freq=new_freq
        )
