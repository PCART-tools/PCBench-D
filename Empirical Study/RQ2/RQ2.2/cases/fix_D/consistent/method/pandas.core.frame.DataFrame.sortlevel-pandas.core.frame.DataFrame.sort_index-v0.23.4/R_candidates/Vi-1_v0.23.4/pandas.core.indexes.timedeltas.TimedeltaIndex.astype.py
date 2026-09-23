    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_timedelta64_dtype(dtype) and not is_timedelta64_ns_dtype(dtype):
            # return an index (essentially this is division)
            result = self.values.astype(dtype, copy=copy)
            if self.hasnans:
                values = self._maybe_mask_results(result, convert='float64')
                return Index(values, name=self.name)
            return Index(result.astype('i8'), name=self.name)
        return super(TimedeltaIndex, self).astype(dtype, copy=copy)
