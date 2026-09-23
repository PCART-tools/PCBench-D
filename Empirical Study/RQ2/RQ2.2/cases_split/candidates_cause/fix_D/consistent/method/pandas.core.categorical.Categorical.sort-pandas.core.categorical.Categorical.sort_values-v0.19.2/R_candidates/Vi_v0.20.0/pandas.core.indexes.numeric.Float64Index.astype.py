    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_float_dtype(dtype):
            values = self._values.astype(dtype, copy=copy)
        elif is_integer_dtype(dtype):
            if self.hasnans:
                raise ValueError('cannot convert float NaN to integer')
            values = self._values.astype(dtype, copy=copy)
        elif is_object_dtype(dtype):
            values = self._values.astype('object', copy=copy)
        else:
            raise TypeError('Setting %s dtype to anything other than '
                            'float64 or object is not supported' %
                            self.__class__)
        return Index(values, name=self.name, dtype=dtype)
