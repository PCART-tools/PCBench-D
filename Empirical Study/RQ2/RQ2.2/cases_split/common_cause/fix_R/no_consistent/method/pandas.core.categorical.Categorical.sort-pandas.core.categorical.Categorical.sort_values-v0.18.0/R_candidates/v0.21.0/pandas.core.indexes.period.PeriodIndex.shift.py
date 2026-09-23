    def shift(self, n):
        """
        Specialized shift which produces an PeriodIndex

        Parameters
        ----------
        n : int
            Periods to shift by

        Returns
        -------
        shifted : PeriodIndex
        """
        values = self._values + n * self.freq.n
        if self.hasnans:
            values[self._isnan] = tslib.iNaT
        return self._shallow_copy(values=values)
