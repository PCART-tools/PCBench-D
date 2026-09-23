    def _sub_datelike(self, other):
        # subtract a datetime from myself, yielding a ndarray[timedelta64[ns]]
        if isinstance(other, (DatetimeIndex, np.ndarray)):
            # if other is an ndarray, we assume it is datetime64-dtype
            other = DatetimeIndex(other)
            # require tz compat
            if not self._has_same_tz(other):
                raise TypeError("{cls} subtraction must have the same "
                                "timezones or no timezones"
                                .format(cls=type(self).__name__))
            result = self._sub_datelike_dti(other)
        elif isinstance(other, (datetime, np.datetime64)):
            assert other is not libts.NaT
            other = Timestamp(other)
            if other is libts.NaT:
                return self - libts.NaT
            # require tz compat
            elif not self._has_same_tz(other):
                raise TypeError("Timestamp subtraction must have the same "
                                "timezones or no timezones")
            else:
                i8 = self.asi8
                result = checked_add_with_arr(i8, -other.value,
                                              arr_mask=self._isnan)
                result = self._maybe_mask_results(result,
                                                  fill_value=libts.iNaT)
        else:
            raise TypeError("cannot subtract {cls} and {typ}"
                            .format(cls=type(self).__name__,
                                    typ=type(other).__name__))
        return result.view('timedelta64[ns]')
