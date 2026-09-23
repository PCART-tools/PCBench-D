    def _add_timedeltalike_scalar(self, other):
        """
        Parameters
        ----------
        other : timedelta, Tick, np.timedelta64

        Returns
        -------
        result : ndarray[int64]
        """
        assert isinstance(self.freq, Tick)  # checked by calling function
        assert isinstance(other, (timedelta, np.timedelta64, Tick))

        if notna(other):
            # special handling for np.timedelta64("NaT"), avoid calling
            #  _check_timedeltalike_freq_compat as that would raise TypeError
            other = self._check_timedeltalike_freq_compat(other)

        # Note: when calling parent class's _add_timedeltalike_scalar,
        #  it will call delta_to_nanoseconds(delta).  Because delta here
        #  is an integer, delta_to_nanoseconds will return it unchanged.
        ordinals = super()._add_timedeltalike_scalar(other)
        return ordinals
