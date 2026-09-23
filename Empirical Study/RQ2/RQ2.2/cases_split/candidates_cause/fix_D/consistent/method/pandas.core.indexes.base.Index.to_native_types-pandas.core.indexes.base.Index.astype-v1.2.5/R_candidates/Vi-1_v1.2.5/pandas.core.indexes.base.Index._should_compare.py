    def _should_compare(self, other: "Index") -> bool:
        """
        Check if `self == other` can ever have non-False entries.
        """
        other = unpack_nested_dtype(other)
        dtype = other.dtype
        return self._is_comparable_dtype(dtype) or is_object_dtype(dtype)
