    def _add_delta(self, other):
        """
        Add a timedelta-like, Tick or TimedeltaIndex-like object
        to self, yielding an int64 numpy array

        Parameters
        ----------
        delta : {timedelta, np.timedelta64, Tick,
                 TimedeltaIndex, ndarray[timedelta64]}

        Returns
        -------
        result : ndarray[int64]

        Notes
        -----
        The result's name is set outside of _add_delta by the calling
        method (__add__ or __sub__), if necessary (i.e. for Indexes).
        """
        if isinstance(other, (Tick, timedelta, np.timedelta64)):
            new_values = self._add_timedeltalike_scalar(other)
        elif is_timedelta64_dtype(other):
            # ndarray[timedelta64] or TimedeltaArray/index
            new_values = self._add_delta_tdi(other)

        return new_values
