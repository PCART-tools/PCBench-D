    @doc(Index.astype)
    def astype(self, dtype, copy=True):
        if is_float_dtype(self.dtype):
            dtype = pandas_dtype(dtype)
            if needs_i8_conversion(dtype):
                raise TypeError(
                    f"Cannot convert Float64Index to dtype {dtype}; integer "
                    "values are required for conversion"
                )
            elif is_integer_dtype(dtype) and not is_extension_array_dtype(dtype):
                # TODO(jreback); this can change once we have an EA Index type
                # GH 13149
                arr = astype_nansafe(self._values, dtype=dtype)
                return Int64Index(arr, name=self.name)

        return super().astype(dtype, copy=copy)
