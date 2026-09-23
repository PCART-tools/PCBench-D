    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True, how='start'):
        dtype = pandas_dtype(dtype)
        if is_integer_dtype(dtype):
            return self._int64index.copy() if copy else self._int64index
        elif is_datetime64_any_dtype(dtype):
            tz = getattr(dtype, 'tz', None)
            return self.to_timestamp(how=how).tz_localize(tz)
        elif is_period_dtype(dtype):
            return self.asfreq(freq=dtype.freq)
        return super(PeriodIndex, self).astype(dtype, copy=copy)
