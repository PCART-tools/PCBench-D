    def _add_delta(self, delta):
        """
        Add a timedelta-like, Tick, or TimedeltaIndex-like object
        to self, yielding a new TimedeltaArray.

        Parameters
        ----------
        other : {timedelta, np.timedelta64, Tick,
                 TimedeltaIndex, ndarray[timedelta64]}

        Returns
        -------
        result : TimedeltaArray
        """
        new_values = super()._add_delta(delta)
        return type(self)._from_sequence(new_values, freq="infer")
