def array_equivalent(left, right, strict_nan: bool = False) -> bool:
    """
    True if two arrays, left and right, have equal non-NaN elements, and NaNs
    in corresponding locations.  False otherwise. It is assumed that left and
    right are NumPy arrays of the same dtype. The behavior of this function
    (particularly with respect to NaNs) is not defined if the dtypes are
    different.

    Parameters
    ----------
    left, right : ndarrays
    strict_nan : bool, default False
        If True, consider NaN and None to be different.

    Returns
    -------
    b : bool
        Returns True if the arrays are equivalent.

    Examples
    --------
    >>> array_equivalent(
    ...     np.array([1, 2, np.nan]),
    ...     np.array([1, 2, np.nan]))
    True
    >>> array_equivalent(
    ...     np.array([1, np.nan, 2]),
    ...     np.array([1, 2, np.nan]))
    False
    """

    left, right = np.asarray(left), np.asarray(right)

    # shape compat
    if left.shape != right.shape:
        return False

    # Object arrays can contain None, NaN and NaT.
    # string dtypes must be come to this path for NumPy 1.7.1 compat
    if is_string_dtype(left) or is_string_dtype(right):

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

    # NaNs can occur in float and complex arrays.
    if is_float_dtype(left) or is_complex_dtype(left):

        # empty
        if not (np.prod(left.shape) and np.prod(right.shape)):
            return True
        return ((left == right) | (isna(left) & isna(right))).all()

    elif is_datetimelike_v_numeric(left, right):
        # GH#29553 avoid numpy deprecation warning
        return False

    elif needs_i8_conversion(left) or needs_i8_conversion(right):
        # datetime64, timedelta64, Period
        if not is_dtype_equal(left.dtype, right.dtype):
            return False

        left = left.view("i8")
        right = right.view("i8")

    # if we have structured dtypes, compare first
    if left.dtype.type is np.void or right.dtype.type is np.void:
        if left.dtype != right.dtype:
            return False

    return np.array_equal(left, right)
