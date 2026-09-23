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
            Array of DateOffset objects; nulls represented by NaT
        """
        if not is_period_dtype(self):
            raise TypeError("cannot subtract {dtype}-dtype from {cls}"
                            .format(dtype=other.dtype,
                                    cls=type(self).__name__))

        if len(self) != len(other):
            raise ValueError("cannot subtract arrays/indices of "
                             "unequal length")
        if self.freq != other.freq:
            msg = DIFFERENT_FREQ.format(cls=type(self).__name__,
                                        own_freq=self.freqstr,
                                        other_freq=other.freqstr)
            raise IncompatibleFrequency(msg)

        new_values = checked_add_with_arr(self.asi8, -other.asi8,
                                          arr_mask=self._isnan,
                                          b_mask=other._isnan)

        new_values = np.array([self.freq.base * x for x in new_values])
        if self._hasnans or other._hasnans:
            mask = (self._isnan) | (other._isnan)
            new_values[mask] = NaT
        return new_values
