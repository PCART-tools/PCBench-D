    @final
    def _should_compare(self, other: Index) -> bool:
        """
        Check if `self == other` can ever have non-False entries.
        """

        if (is_bool_dtype(other) and is_any_real_numeric_dtype(self)) or (
            is_bool_dtype(self) and is_any_real_numeric_dtype(other)
        ):
            # GH#16877 Treat boolean labels passed to a numeric index as not
            #  found. Without this fix False and True would be treated as 0 and 1
            #  respectively.
            return False

        other = _unpack_nested_dtype(other)
        dtype = other.dtype
        return self._is_comparable_dtype(dtype) or is_object_dtype(dtype)
