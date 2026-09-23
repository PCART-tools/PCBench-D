    def _add_delta(self, delta):
        """
        Add a timedelta-like, DateOffset, or TimedeltaIndex-like object
        to self.

        Parameters
        ----------
        delta : {timedelta, np.timedelta64, DateOffset,
                 TimedelaIndex, ndarray[timedelta64]}

        Returns
        -------
        result : DatetimeIndex

        Notes
        -----
        The result's name is set outside of _add_delta by the calling
        method (__add__ or __sub__)
        """
        from pandas import TimedeltaIndex

        if isinstance(delta, (Tick, timedelta, np.timedelta64)):
            new_values = self._add_delta_td(delta)
        elif is_timedelta64_dtype(delta):
            if not isinstance(delta, TimedeltaIndex):
                delta = TimedeltaIndex(delta)
            new_values = self._add_delta_tdi(delta)
        else:
            new_values = self.astype('O') + delta

        tz = 'UTC' if self.tz is not None else None
        result = DatetimeIndex(new_values, tz=tz, freq='infer')
        if self.tz is not None and self.tz is not utc:
            result = result.tz_convert(self.tz)
        return result
