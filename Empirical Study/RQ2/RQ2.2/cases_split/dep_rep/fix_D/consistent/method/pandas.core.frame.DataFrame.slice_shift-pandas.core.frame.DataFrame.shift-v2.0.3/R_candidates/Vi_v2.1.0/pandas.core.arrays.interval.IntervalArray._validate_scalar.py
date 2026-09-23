    def _validate_scalar(self, value):
        if isinstance(value, Interval):
            self._check_closed_matches(value, name="value")
            left, right = value.left, value.right
            # TODO: check subdtype match like _validate_setitem_value?
        elif is_valid_na_for_dtype(value, self.left.dtype):
            # GH#18295
            left = right = self.left._na_value
        else:
            raise TypeError(
                "can only insert Interval objects and NA into an IntervalArray"
            )
        return left, right
