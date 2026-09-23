    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_interval_dtype(dtype) and dtype != self.dtype:
            try:
                new_left = self.left.astype(dtype.subtype)
                new_right = self.right.astype(dtype.subtype)
            except TypeError:
                msg = ('Cannot convert {dtype} to {new_dtype}; subtypes are '
                       'incompatible')
                raise TypeError(msg.format(dtype=self.dtype, new_dtype=dtype))
            return self._shallow_copy(new_left, new_right)
        return super(IntervalIndex, self).astype(dtype, copy=copy)
