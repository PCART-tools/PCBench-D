    def _add_timedelta_arraylike(self, other):
        """
        Add a delta of a TimedeltaIndex

        Returns
        -------
        Same type as self
        """
        # overridden by PeriodArray

        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        if isinstance(other, np.ndarray):
            # ndarray[timedelta64]; wrap in TimedeltaIndex for op
            from pandas.core.arrays import TimedeltaArray

            other = TimedeltaArray._from_sequence(other)

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = checked_add_with_arr(
            self_i8, other_i8, arr_mask=self._isnan, b_mask=other._isnan
        )
        if self._hasna or other._hasna:
            mask = self._isnan | other._isnan
            np.putmask(new_values, mask, iNaT)

        return type(self)(new_values, dtype=self.dtype)
