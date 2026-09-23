    def _add_delta(self, delta):
        """
        Add a timedelta-like, Tick, or TimedeltaIndex-like object
        to self.

        Parameters
        ----------
        delta : {timedelta, np.timedelta64, Tick, TimedeltaIndex}

        Returns
        -------
        result : TimedeltaIndex

        Notes
        -----
        The result's name is set outside of _add_delta by the calling
        method (__add__ or __sub__)
        """
        if isinstance(delta, (Tick, timedelta, np.timedelta64)):
            new_values = self._add_delta_td(delta)
        elif isinstance(delta, TimedeltaIndex):
            new_values = self._add_delta_tdi(delta)
        elif is_timedelta64_dtype(delta):
            # ndarray[timedelta64] --> wrap in TimedeltaIndex
            delta = TimedeltaIndex(delta)
            new_values = self._add_delta_tdi(delta)
        else:
            raise TypeError("cannot add the type {0} to a TimedeltaIndex"
                            .format(type(delta)))

        return TimedeltaIndex(new_values, freq='infer')
