    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True, how='start'):
        dtype = pandas_dtype(dtype)
        if is_object_dtype(dtype):
            return self.asobject
        elif is_integer_dtype(dtype):
            if copy:
                return self._int64index.copy()
            else:
                return self._int64index
        elif is_datetime64_dtype(dtype):
            return self.to_timestamp(how=how)
        elif is_datetime64tz_dtype(dtype):
            return self.to_timestamp(how=how).tz_localize(dtype.tz)
        elif is_period_dtype(dtype):
            return self.asfreq(freq=dtype.freq)
        raise ValueError('Cannot cast PeriodIndex to dtype %s' % dtype)
