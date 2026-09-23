    def _validate_setitem_value(self, value):

        if is_valid_na_for_dtype(value, self.left.dtype):
            # na value: need special casing to set directly on numpy arrays
            value = self.left._na_value
            if is_integer_dtype(self.dtype.subtype):
                # can't set NaN on a numpy integer array
                # GH#45484 TypeError, not ValueError, matches what we get with
                #  non-NA un-holdable value.
                raise TypeError("Cannot set float NaN to integer-backed IntervalArray")
            value_left, value_right = value, value

        elif isinstance(value, Interval):
            # scalar interval
            self._check_closed_matches(value, name="value")
            value_left, value_right = value.left, value.right
            self.left._validate_fill_value(value_left)
            self.left._validate_fill_value(value_right)

        else:
            return self._validate_listlike(value)

        return value_left, value_right
