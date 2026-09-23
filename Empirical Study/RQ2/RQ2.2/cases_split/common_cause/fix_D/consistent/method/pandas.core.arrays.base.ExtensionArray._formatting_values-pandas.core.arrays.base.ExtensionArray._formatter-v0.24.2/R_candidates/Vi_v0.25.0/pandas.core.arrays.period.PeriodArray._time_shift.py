    def _time_shift(self, periods, freq=None):
        """
        Shift each value by `periods`.

        Note this is different from ExtensionArray.shift, which
        shifts the *position* of each element, padding the end with
        missing values.

        Parameters
        ----------
        periods : int
            Number of periods to shift by.
        freq : pandas.DateOffset, pandas.Timedelta, or string
            Frequency increment to shift by.
        """
        if freq is not None:
            raise TypeError(
                "`freq` argument is not supported for "
                "{cls}._time_shift".format(cls=type(self).__name__)
            )
        values = self.asi8 + periods * self.freq.n
        if self._hasnans:
            values[self._isnan] = iNaT
        return type(self)(values, freq=self.freq)
