    @final
    def _should_compare(self, other: Index) -> bool:
        """
        Check if `self == other` can ever have non-False entries.
        """

        # NB: we use inferred_type rather than is_bool_dtype to catch
        #  object_dtype_of_bool and categorical[object_dtype_of_bool] cases
        if (
            other.inferred_type == "boolean" and is_any_real_numeric_dtype(self.dtype)
        ) or (
            self.inferred_type == "boolean" and is_any_real_numeric_dtype(other.dtype)
        ):
            # GH#16877 Treat boolean labels passed to a numeric index as not
            #  found. Without this fix False and True would be treated as 0 and 1
            #  respectively.
            return False

        other = _unpack_nested_dtype(other)
        dtype = other.dtype
        return self._is_comparable_dtype(dtype) or is_object_dtype(dtype)
