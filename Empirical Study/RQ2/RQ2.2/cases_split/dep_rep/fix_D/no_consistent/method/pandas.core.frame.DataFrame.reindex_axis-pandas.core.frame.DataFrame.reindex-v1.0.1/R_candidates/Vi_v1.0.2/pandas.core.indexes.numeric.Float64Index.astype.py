    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if needs_i8_conversion(dtype):
            raise TypeError(
                f"Cannot convert Float64Index to dtype {dtype}; integer "
                "values are required for conversion"
            )
        elif is_integer_dtype(dtype) and not is_extension_array_dtype(dtype):
            # TODO(jreback); this can change once we have an EA Index type
            # GH 13149
            arr = astype_nansafe(self.values, dtype=dtype)
            return Int64Index(arr)
        return super().astype(dtype, copy=copy)
