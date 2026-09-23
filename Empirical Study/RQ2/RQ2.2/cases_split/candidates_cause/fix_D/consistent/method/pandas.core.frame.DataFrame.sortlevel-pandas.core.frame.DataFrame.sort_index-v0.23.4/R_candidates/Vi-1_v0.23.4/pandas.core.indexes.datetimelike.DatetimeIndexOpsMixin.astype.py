    def astype(self, dtype, copy=True):
        if is_object_dtype(dtype):
            return self._box_values_as_index()
        elif is_string_dtype(dtype) and not is_categorical_dtype(dtype):
            return Index(self.format(), name=self.name, dtype=object)
        elif is_integer_dtype(dtype):
            return Index(self.values.astype('i8', copy=copy), name=self.name,
                         dtype='i8')
        elif (is_datetime_or_timedelta_dtype(dtype) and
              not is_dtype_equal(self.dtype, dtype)) or is_float_dtype(dtype):
            # disallow conversion between datetime/timedelta,
            # and conversions for any datetimelike to float
            msg = 'Cannot cast {name} to dtype {dtype}'
            raise TypeError(msg.format(name=type(self).__name__, dtype=dtype))
        return super(DatetimeIndexOpsMixin, self).astype(dtype, copy=copy)
