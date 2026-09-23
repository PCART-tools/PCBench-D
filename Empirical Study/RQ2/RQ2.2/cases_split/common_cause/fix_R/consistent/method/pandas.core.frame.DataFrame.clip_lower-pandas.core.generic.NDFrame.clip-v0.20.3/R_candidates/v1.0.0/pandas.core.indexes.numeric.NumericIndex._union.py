    def _union(self, other, sort):
        # Right now, we treat union(int, float) a bit special.
        # See https://github.com/pandas-dev/pandas/issues/26778 for discussion
        # We may change union(int, float) to go to object.
        # float | [u]int -> float  (the special case)
        # <T>   | <T>    -> T
        # <T>   | <U>    -> object
        needs_cast = (is_integer_dtype(self.dtype) and is_float_dtype(other.dtype)) or (
            is_integer_dtype(other.dtype) and is_float_dtype(self.dtype)
        )
        if needs_cast:
            first = self.astype("float")
            second = other.astype("float")
            return first._union(second, sort)
        else:
            return super()._union(other, sort)
