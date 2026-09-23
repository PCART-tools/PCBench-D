    def _add_delta_tdi(self, other):
        """
        Parameters
        ----------
        other : TimedeltaArray or ndarray[timedelta64]

        Returns
        -------
        result : ndarray[int64]
        """
        assert isinstance(self.freq, Tick)  # checked by calling function

        if not np.all(isna(other)):
            delta = self._check_timedeltalike_freq_compat(other)
        else:
            # all-NaT TimedeltaIndex is equivalent to a single scalar td64 NaT
            return self + np.timedelta64("NaT")

        return self._addsub_int_array(delta, operator.add).asi8
