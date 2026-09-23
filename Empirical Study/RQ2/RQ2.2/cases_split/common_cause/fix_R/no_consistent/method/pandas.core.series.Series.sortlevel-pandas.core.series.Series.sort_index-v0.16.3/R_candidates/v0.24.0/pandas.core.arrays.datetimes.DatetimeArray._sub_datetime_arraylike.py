    def _sub_datetime_arraylike(self, other):
        """subtract DatetimeArray/Index or ndarray[datetime64]"""
        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        if isinstance(other, np.ndarray):
            assert is_datetime64_dtype(other)
            other = type(self)(other)

        if not self._has_same_tz(other):
            # require tz compat
            raise TypeError("{cls} subtraction must have the same "
                            "timezones or no timezones"
                            .format(cls=type(self).__name__))

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = checked_add_with_arr(self_i8, -other_i8,
                                          arr_mask=self._isnan)
        if self._hasnans or other._hasnans:
            mask = (self._isnan) | (other._isnan)
            new_values[mask] = iNaT
        return new_values.view('timedelta64[ns]')
