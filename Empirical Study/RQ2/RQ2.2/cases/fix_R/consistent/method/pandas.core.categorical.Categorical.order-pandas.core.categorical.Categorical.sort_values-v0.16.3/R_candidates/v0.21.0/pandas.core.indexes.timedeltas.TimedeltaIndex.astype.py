    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = np.dtype(dtype)

        if is_object_dtype(dtype):
            return self.asobject
        elif is_timedelta64_ns_dtype(dtype):
            if copy is True:
                return self.copy()
            return self
        elif is_timedelta64_dtype(dtype):
            # return an index (essentially this is division)
            result = self.values.astype(dtype, copy=copy)
            if self.hasnans:
                return Index(self._maybe_mask_results(result,
                                                      convert='float64'),
                             name=self.name)
            return Index(result.astype('i8'), name=self.name)
        elif is_integer_dtype(dtype):
            return Index(self.values.astype('i8', copy=copy), dtype='i8',
                         name=self.name)
        raise ValueError('Cannot cast TimedeltaIndex to dtype %s' % dtype)
