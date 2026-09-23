    @final
    def _should_compare(self, other: Index) -> bool:
        """
        Check if `self == other` can ever have non-False entries.
        """

        if (other.is_boolean() and self.is_numeric()) or (
            self.is_boolean() and other.is_numeric()
        ):
            # GH#16877 Treat boolean labels passed to a numeric index as not
            #  found. Without this fix False and True would be treated as 0 and 1
            #  respectively.
            return False

        other = unpack_nested_dtype(other)
        dtype = other.dtype
        return self._is_comparable_dtype(dtype) or is_object_dtype(dtype)
