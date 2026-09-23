    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_object_dtype(dtype):
            return self.asobject
        elif is_integer_dtype(dtype):
            return Index(self.values.astype('i8', copy=copy), name=self.name,
                         dtype='i8')
        elif is_datetime64_ns_dtype(dtype):
            if self.tz is not None:
                return self.tz_convert('UTC').tz_localize(None)
            elif copy is True:
                return self.copy()
            return self
        elif is_string_dtype(dtype):
            return Index(self.format(), name=self.name, dtype=object)
        elif is_period_dtype(dtype):
            return self.to_period(freq=dtype.freq)
        raise ValueError('Cannot cast DatetimeIndex to dtype %s' % dtype)
