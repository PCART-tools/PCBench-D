    def __setitem__(self, key, value):
        # na value: need special casing to set directly on numpy arrays
        needs_float_conversion = False
        if is_scalar(value) and isna(value):
            if is_integer_dtype(self.dtype.subtype):
                # can't set NaN on a numpy integer array
                needs_float_conversion = True
            elif is_datetime64_any_dtype(self.dtype.subtype):
                # need proper NaT to set directly on the numpy array
                value = np.datetime64("NaT")
            elif is_timedelta64_dtype(self.dtype.subtype):
                # need proper NaT to set directly on the numpy array
                value = np.timedelta64("NaT")
            value_left, value_right = value, value

        # scalar interval
        elif is_interval_dtype(value) or isinstance(value, ABCInterval):
            self._check_closed_matches(value, name="value")
            value_left, value_right = value.left, value.right

        else:
            # list-like of intervals
            try:
                array = IntervalArray(value)
                value_left, value_right = array.left, array.right
            except TypeError:
                # wrong type: not interval or NA
                msg = "'value' should be an interval type, got {} instead."
                raise TypeError(msg.format(type(value)))

        # Need to ensure that left and right are updated atomically, so we're
        # forced to copy, update the copy, and swap in the new values.
        left = self.left.copy(deep=True)
        if needs_float_conversion:
            left = left.astype("float")
        left.values[key] = value_left
        self._left = left

        right = self.right.copy(deep=True)
        if needs_float_conversion:
            right = right.astype("float")
        right.values[key] = value_right
        self._right = right
