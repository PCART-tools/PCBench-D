    def astype(self, dtype, copy: bool = True):
        # We handle
        #   --> datetime
        #   --> period
        # DatetimeLikeArrayMixin Super handles the rest.
        dtype = pandas_dtype(dtype)

        if is_dtype_equal(dtype, self.dtype):
            if copy:
                return self.copy()
            return self

        elif is_datetime64_ns_dtype(dtype):
            return astype_dt64_to_dt64tz(self, dtype, copy, via_utc=False)

        elif self.tz is None and is_datetime64_dtype(dtype) and dtype != self.dtype:
            # unit conversion e.g. datetime64[s]
            return self._ndarray.astype(dtype)

        elif is_period_dtype(dtype):
            return self.to_period(freq=dtype.freq)
        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy)
