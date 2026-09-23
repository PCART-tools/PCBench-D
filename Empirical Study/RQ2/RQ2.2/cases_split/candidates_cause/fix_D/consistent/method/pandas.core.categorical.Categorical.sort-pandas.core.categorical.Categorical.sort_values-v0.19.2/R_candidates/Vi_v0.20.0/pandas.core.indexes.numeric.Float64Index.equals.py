    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if self is other:
            return True

        if not isinstance(other, Index):
            return False

        # need to compare nans locations and make sure that they are the same
        # since nans don't compare equal this is a bit tricky
        try:
            if not isinstance(other, Float64Index):
                other = self._constructor(other)
            if (not is_dtype_equal(self.dtype, other.dtype) or
                    self.shape != other.shape):
                return False
            left, right = self._values, other._values
            return ((left == right) | (self._isnan & other._isnan)).all()
        except (TypeError, ValueError):
            return False
