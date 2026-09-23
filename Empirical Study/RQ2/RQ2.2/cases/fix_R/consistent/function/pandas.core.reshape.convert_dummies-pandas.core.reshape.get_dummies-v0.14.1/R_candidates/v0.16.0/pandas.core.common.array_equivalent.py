def array_equivalent(left, right, strict_nan=False):
    """
    True if two arrays, left and right, have equal non-NaN elements, and NaNs in
    corresponding locations.  False otherwise. It is assumed that left and right
    are NumPy arrays of the same dtype. The behavior of this function
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
    if left.shape != right.shape: return False

    # Object arrays can contain None, NaN and NaT.
    if issubclass(left.dtype.type, np.object_) or issubclass(right.dtype.type, np.object_):

        if not strict_nan:
            # pd.isnull considers NaN and None to be equivalent.
            return lib.array_equivalent_object(_ensure_object(left.ravel()),
                                               _ensure_object(right.ravel()))

        for left_value, right_value in zip(left, right):
            if left_value is tslib.NaT and right_value is not tslib.NaT:
                return False

            elif isinstance(left_value, float) and np.isnan(left_value):
                if not isinstance(right_value, float) or not np.isnan(right_value):
                    return False
            else:
                if left_value != right_value:
                    return False
        return True

    # NaNs can occur in float and complex arrays.
    if issubclass(left.dtype.type, (np.floating, np.complexfloating)):
        return ((left == right) | (np.isnan(left) & np.isnan(right))).all()

    # NaNs cannot occur otherwise.
    return np.array_equal(left, right)
