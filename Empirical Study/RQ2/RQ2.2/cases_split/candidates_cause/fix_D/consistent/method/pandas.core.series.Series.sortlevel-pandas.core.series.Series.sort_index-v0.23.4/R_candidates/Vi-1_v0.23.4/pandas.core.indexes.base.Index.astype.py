    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        if is_dtype_equal(self.dtype, dtype):
            return self.copy() if copy else self
        elif is_categorical_dtype(dtype):
            from .category import CategoricalIndex
            return CategoricalIndex(self.values, name=self.name, dtype=dtype,
                                    copy=copy)
        try:
            return Index(self.values.astype(dtype, copy=copy), name=self.name,
                         dtype=dtype)
        except (TypeError, ValueError):
            msg = 'Cannot cast {name} to dtype {dtype}'
            raise TypeError(msg.format(name=type(self).__name__, dtype=dtype))
