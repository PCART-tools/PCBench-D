    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if needs_i8_conversion(dtype):
            msg = ('Cannot convert Float64Index to dtype {dtype}; integer '
                   'values are required for conversion').format(dtype=dtype)
            raise TypeError(msg)
        elif is_integer_dtype(dtype) and self.hasnans:
            # GH 13149
            raise ValueError('Cannot convert NA to integer')
        return super(Float64Index, self).astype(dtype, copy=copy)
