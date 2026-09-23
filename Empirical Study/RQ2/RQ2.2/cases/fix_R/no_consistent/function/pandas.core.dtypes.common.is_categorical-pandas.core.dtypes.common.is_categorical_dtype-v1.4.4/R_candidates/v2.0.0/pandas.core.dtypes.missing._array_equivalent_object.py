def _array_equivalent_object(left: np.ndarray, right: np.ndarray, strict_nan: bool):
    if not strict_nan:
        # isna considers NaN and None to be equivalent.

        return lib.array_equivalent_object(ensure_object(left), ensure_object(right))

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
                if "boolean value of NA is ambiguous" in str(err):
                    return False
                raise
            except ValueError:
                # numpy can raise a ValueError if left and right cannot be
                # compared (e.g. nested arrays)
                return False
    return True
