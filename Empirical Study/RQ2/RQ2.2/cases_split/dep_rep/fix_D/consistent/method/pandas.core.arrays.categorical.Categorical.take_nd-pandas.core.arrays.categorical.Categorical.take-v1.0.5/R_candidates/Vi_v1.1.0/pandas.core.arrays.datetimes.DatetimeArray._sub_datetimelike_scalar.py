    def _sub_datetimelike_scalar(self, other):
        # subtract a datetime from myself, yielding a ndarray[timedelta64[ns]]
        assert isinstance(other, (datetime, np.datetime64))
        assert other is not NaT
        other = Timestamp(other)
        if other is NaT:
            return self - NaT

        if not self._has_same_tz(other):
            # require tz compat
            raise TypeError(
                "Timestamp subtraction must have the same timezones or no timezones"
            )

        i8 = self.asi8
        result = checked_add_with_arr(i8, -other.value, arr_mask=self._isnan)
        result = self._maybe_mask_results(result)
        return result.view("timedelta64[ns]")
