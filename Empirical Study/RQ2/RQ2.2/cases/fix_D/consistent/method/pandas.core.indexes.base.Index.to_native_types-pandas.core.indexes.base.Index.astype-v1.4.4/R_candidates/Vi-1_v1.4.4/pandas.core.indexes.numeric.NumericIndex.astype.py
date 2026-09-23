    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)
        if is_float_dtype(self.dtype):
            if needs_i8_conversion(dtype):
                raise TypeError(
                    f"Cannot convert Float64Index to dtype {dtype}; integer "
                    "values are required for conversion"
                )
            elif is_integer_dtype(dtype) and not is_extension_array_dtype(dtype):
                # TODO(ExtensionIndex); this can change once we have an EA Index type
                # GH 13149
                arr = astype_nansafe(self._values, dtype=dtype)
                if isinstance(self, Float64Index):
                    return Int64Index(arr, name=self.name)
                else:
                    return NumericIndex(arr, name=self.name, dtype=dtype)
        elif self._is_backward_compat_public_numeric_index:
            # this block is needed so e.g. NumericIndex[int8].astype("int32") returns
            # NumericIndex[int32] and not Int64Index with dtype int64.
            # When Int64Index etc. are removed from the code base, removed this also.
            if not is_extension_array_dtype(dtype) and is_numeric_dtype(dtype):
                return self._constructor(self, dtype=dtype, copy=copy)

        return super().astype(dtype, copy=copy)
