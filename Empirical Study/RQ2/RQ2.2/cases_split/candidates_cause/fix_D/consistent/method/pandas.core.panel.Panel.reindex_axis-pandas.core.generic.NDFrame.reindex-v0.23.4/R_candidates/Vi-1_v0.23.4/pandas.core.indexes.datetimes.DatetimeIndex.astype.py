    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if (is_datetime64_ns_dtype(dtype) and
                not is_dtype_equal(dtype, self.dtype)):
            # GH 18951: datetime64_ns dtype but not equal means different tz
            new_tz = getattr(dtype, 'tz', None)
            if getattr(self.dtype, 'tz', None) is None:
                return self.tz_localize(new_tz)
            return self.tz_convert(new_tz)
        elif is_period_dtype(dtype):
            return self.to_period(freq=dtype.freq)
        return super(DatetimeIndex, self).astype(dtype, copy=copy)
