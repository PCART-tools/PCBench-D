    def _add_datelike(self, other):
        # adding a timedeltaindex to a datetimelike
        from pandas import Timestamp, DatetimeIndex
        if isinstance(other, (DatetimeIndex, np.ndarray)):
            # if other is an ndarray, we assume it is datetime64-dtype
            # defer to implementation in DatetimeIndex
            other = DatetimeIndex(other)
            return other + self
        else:
            assert other is not NaT
            other = Timestamp(other)
            i8 = self.asi8
            result = checked_add_with_arr(i8, other.value,
                                          arr_mask=self._isnan)
            result = self._maybe_mask_results(result, fill_value=iNaT)
            return DatetimeIndex(result)
