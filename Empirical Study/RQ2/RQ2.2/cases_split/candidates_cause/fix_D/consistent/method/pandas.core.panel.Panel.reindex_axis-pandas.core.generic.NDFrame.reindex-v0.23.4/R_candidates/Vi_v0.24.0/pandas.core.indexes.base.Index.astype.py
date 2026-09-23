    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        if is_dtype_equal(self.dtype, dtype):
            return self.copy() if copy else self

        elif is_categorical_dtype(dtype):
            from .category import CategoricalIndex
            return CategoricalIndex(self.values, name=self.name, dtype=dtype,
                                    copy=copy)
        elif is_datetime64tz_dtype(dtype):
            # TODO(GH-24559): Remove this block, use the following elif.
            # avoid FutureWarning from DatetimeIndex constructor.
            from pandas import DatetimeIndex
            tz = pandas_dtype(dtype).tz
            return (DatetimeIndex(np.asarray(self))
                    .tz_localize("UTC").tz_convert(tz))

        elif is_extension_array_dtype(dtype):
            return Index(np.asarray(self), dtype=dtype, copy=copy)

        try:
            if is_datetime64tz_dtype(dtype):
                from pandas import DatetimeIndex
                return DatetimeIndex(self.values, name=self.name, dtype=dtype,
                                     copy=copy)
            return Index(self.values.astype(dtype, copy=copy), name=self.name,
                         dtype=dtype)
        except (TypeError, ValueError):
            msg = 'Cannot cast {name} to dtype {dtype}'
            raise TypeError(msg.format(name=type(self).__name__, dtype=dtype))
