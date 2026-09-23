def _array_equivalent_object(left, right, strict_nan):
    if not strict_nan:
        # isna considers NaN and None to be equivalent.
        return lib.array_equivalent_object(
            ensure_object(left.ravel()), ensure_object(right.ravel())
        )

    for left_value, right_value in zip(left, right):
        if left_value is NaT and right_value is not NaT:
            return False

        elif left_value is libmissing.NA and right_value is not libmissing.NA:
            return False

        elif isinstance(left_value, float) and np.isnan(left_value):
            if not isinstance(right_value, float) or not np.isnan(right_value):
                return False
        else:
            try:
                if np.any(np.asarray(left_value != right_value)):
                    return False
            except TypeError as err:
                if "Cannot compare tz-naive" in str(err):
                    # tzawareness compat failure, see GH#28507
                    return False
                elif "boolean value of NA is ambiguous" in str(err):
                    return False
                raise
    return True
