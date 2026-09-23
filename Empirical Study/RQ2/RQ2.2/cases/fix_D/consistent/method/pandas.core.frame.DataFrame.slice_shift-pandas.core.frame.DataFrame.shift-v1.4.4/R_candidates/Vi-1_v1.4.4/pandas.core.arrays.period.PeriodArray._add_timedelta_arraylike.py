    def _add_timedelta_arraylike(self, other):
        """
        Parameters
        ----------
        other : TimedeltaArray or ndarray[timedelta64]

        Returns
        -------
        result : ndarray[int64]
        """
        if not isinstance(self.freq, Tick):
            # We cannot add timedelta-like to non-tick PeriodArray
            raise TypeError(
                f"Cannot add or subtract timedelta64[ns] dtype from {self.dtype}"
            )

        if not np.all(isna(other)):
            delta = self._check_timedeltalike_freq_compat(other)
        else:
            # all-NaT TimedeltaIndex is equivalent to a single scalar td64 NaT
            return self + np.timedelta64("NaT")

        ordinals = self._addsub_int_array(delta, operator.add).asi8
        return type(self)(ordinals, dtype=self.dtype)
