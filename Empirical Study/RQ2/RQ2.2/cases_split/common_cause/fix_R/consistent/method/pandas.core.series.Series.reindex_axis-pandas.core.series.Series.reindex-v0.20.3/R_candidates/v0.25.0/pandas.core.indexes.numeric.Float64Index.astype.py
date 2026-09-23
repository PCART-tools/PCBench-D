    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if needs_i8_conversion(dtype):
            msg = (
                "Cannot convert Float64Index to dtype {dtype}; integer "
                "values are required for conversion"
            ).format(dtype=dtype)
            raise TypeError(msg)
        elif (
            is_integer_dtype(dtype) and not is_extension_array_dtype(dtype)
        ) and self.hasnans:
            # TODO(jreback); this can change once we have an EA Index type
            # GH 13149
            raise ValueError("Cannot convert NA to integer")
        return super().astype(dtype, copy=copy)
