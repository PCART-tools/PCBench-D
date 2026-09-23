    def _sub_period_array(self, other):
        """
        Subtract a Period Array/Index from self.  This is only valid if self
        is itself a Period Array/Index, raises otherwise.  Both objects must
        have the same frequency.

        Parameters
        ----------
        other : PeriodIndex or PeriodArray

        Returns
        -------
        result : np.ndarray[object]
            Array of DateOffset objects; nulls represented by NaT.
        """
        self._require_matching_freq(other)

        new_values = algos.checked_add_with_arr(
            self.asi8, -other.asi8, arr_mask=self._isnan, b_mask=other._isnan
        )

        new_values = np.array([self.freq.base * x for x in new_values])
        if self._hasna or other._hasna:
            mask = self._isnan | other._isnan
            new_values[mask] = NaT
        return new_values
