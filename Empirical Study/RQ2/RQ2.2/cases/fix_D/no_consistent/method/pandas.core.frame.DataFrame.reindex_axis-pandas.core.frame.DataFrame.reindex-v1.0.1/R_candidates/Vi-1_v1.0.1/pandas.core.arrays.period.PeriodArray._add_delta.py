    def _add_delta(self, other):
        """
        Add a timedelta-like, Tick, or TimedeltaIndex-like object
        to self, yielding a new PeriodArray

        Parameters
        ----------
        other : {timedelta, np.timedelta64, Tick,
                 TimedeltaIndex, ndarray[timedelta64]}

        Returns
        -------
        result : PeriodArray
        """
        if not isinstance(self.freq, Tick):
            # We cannot add timedelta-like to non-tick PeriodArray
            raise raise_on_incompatible(self, other)

        new_ordinals = super()._add_delta(other)
        return type(self)(new_ordinals, freq=self.freq)
