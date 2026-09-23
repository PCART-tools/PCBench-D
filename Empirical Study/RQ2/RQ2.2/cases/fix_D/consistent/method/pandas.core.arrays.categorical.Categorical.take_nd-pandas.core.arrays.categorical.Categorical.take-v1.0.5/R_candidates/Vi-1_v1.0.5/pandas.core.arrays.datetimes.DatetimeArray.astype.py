    def astype(self, dtype, copy=True):
        # We handle
        #   --> datetime
        #   --> period
        # DatetimeLikeArrayMixin Super handles the rest.
        dtype = pandas_dtype(dtype)

        if is_datetime64_ns_dtype(dtype) and not is_dtype_equal(dtype, self.dtype):
            # GH#18951: datetime64_ns dtype but not equal means different tz
            new_tz = getattr(dtype, "tz", None)
            if getattr(self.dtype, "tz", None) is None:
                return self.tz_localize(new_tz)
            result = self.tz_convert(new_tz)
            if copy:
                result = result.copy()
            if new_tz is None:
                # Do we want .astype('datetime64[ns]') to be an ndarray.
                # The astype in Block._astype expects this to return an
                # ndarray, but we could maybe work around it there.
                result = result._data
            return result
        elif is_datetime64tz_dtype(self.dtype) and is_dtype_equal(self.dtype, dtype):
            if copy:
                return self.copy()
            return self
        elif is_period_dtype(dtype):
            return self.to_period(freq=dtype.freq)
        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy)
