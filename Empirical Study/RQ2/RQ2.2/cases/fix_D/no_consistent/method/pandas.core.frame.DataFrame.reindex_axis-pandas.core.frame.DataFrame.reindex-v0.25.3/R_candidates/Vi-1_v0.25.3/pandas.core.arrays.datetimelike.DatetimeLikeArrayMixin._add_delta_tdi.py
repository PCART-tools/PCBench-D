    def _add_delta_tdi(self, other):
        """
        Add a delta of a TimedeltaIndex
        return the i8 result view
        """
        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        if isinstance(other, np.ndarray):
            # ndarray[timedelta64]; wrap in TimedeltaIndex for op
            from pandas import TimedeltaIndex

            other = TimedeltaIndex(other)

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = checked_add_with_arr(
            self_i8, other_i8, arr_mask=self._isnan, b_mask=other._isnan
        )
        if self._hasnans or other._hasnans:
            mask = (self._isnan) | (other._isnan)
            new_values[mask] = iNaT
        return new_values.view("i8")
