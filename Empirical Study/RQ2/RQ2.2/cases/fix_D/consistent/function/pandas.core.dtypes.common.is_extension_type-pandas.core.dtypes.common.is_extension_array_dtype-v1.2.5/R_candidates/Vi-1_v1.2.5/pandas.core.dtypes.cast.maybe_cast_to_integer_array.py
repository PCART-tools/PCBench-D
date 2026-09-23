def maybe_cast_to_integer_array(arr, dtype: Dtype, copy: bool = False):
    """
    Takes any dtype and returns the casted version, raising for when data is
    incompatible with integer/unsigned integer dtypes.

    .. versionadded:: 0.24.0

    Parameters
    ----------
    arr : array-like
        The array to cast.
    dtype : str, np.dtype
        The integer dtype to cast the array to.
    copy: bool, default False
        Whether to make a copy of the array before returning.

    Returns
    -------
    ndarray
        Array of integer or unsigned integer dtype.

    Raises
    ------
    OverflowError : the dtype is incompatible with the data
    ValueError : loss of precision has occurred during casting

    Examples
    --------
    If you try to coerce negative values to unsigned integers, it raises:

    >>> pd.Series([-1], dtype="uint64")
    Traceback (most recent call last):
        ...
    OverflowError: Trying to coerce negative values to unsigned integers

    Also, if you try to coerce float values to integers, it raises:

    >>> pd.Series([1, 2, 3.5], dtype="int64")
    Traceback (most recent call last):
        ...
    ValueError: Trying to coerce float values to integers
    """
    assert is_integer_dtype(dtype)

    try:
        if not hasattr(arr, "astype"):
            casted = np.array(arr, dtype=dtype, copy=copy)
        else:
            casted = arr.astype(dtype, copy=copy)
    except OverflowError as err:
        raise OverflowError(
            "The elements provided in the data cannot all be "
            f"casted to the dtype {dtype}"
        ) from err

    if np.array_equal(arr, casted):
        return casted

    # We do this casting to allow for proper
    # data and dtype checking.
    #
    # We didn't do this earlier because NumPy
    # doesn't handle `uint64` correctly.
    arr = np.asarray(arr)

    if is_unsigned_integer_dtype(dtype) and (arr < 0).any():
        raise OverflowError("Trying to coerce negative values to unsigned integers")

    if is_float_dtype(arr) or is_object_dtype(arr):
        raise ValueError("Trying to coerce float values to integers")
