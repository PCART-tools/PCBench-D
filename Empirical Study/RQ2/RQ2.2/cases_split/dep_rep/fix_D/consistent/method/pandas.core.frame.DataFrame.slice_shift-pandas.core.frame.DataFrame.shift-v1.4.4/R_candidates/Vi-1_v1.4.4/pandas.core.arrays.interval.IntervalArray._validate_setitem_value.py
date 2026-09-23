    def _validate_setitem_value(self, value):
        needs_float_conversion = False

        if is_valid_na_for_dtype(value, self.left.dtype):
            # na value: need special casing to set directly on numpy arrays
            if is_integer_dtype(self.dtype.subtype):
                # can't set NaN on a numpy integer array
                needs_float_conversion = True
            elif is_datetime64_dtype(self.dtype.subtype):
                # need proper NaT to set directly on the numpy array
                value = np.datetime64("NaT")
            elif is_datetime64tz_dtype(self.dtype.subtype):
                # need proper NaT to set directly on the DatetimeArray array
                value = NaT
            elif is_timedelta64_dtype(self.dtype.subtype):
                # need proper NaT to set directly on the numpy array
                value = np.timedelta64("NaT")
            value_left, value_right = value, value

        elif isinstance(value, Interval):
            # scalar interval
            self._check_closed_matches(value, name="value")
            value_left, value_right = value.left, value.right
            self.left._validate_fill_value(value_left)
            self.left._validate_fill_value(value_right)

        else:
            return self._validate_listlike(value)

        if needs_float_conversion:
            raise ValueError("Cannot set float NaN to integer-backed IntervalArray")
        return value_left, value_right
