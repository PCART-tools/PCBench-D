def maybe_cast_to_integer_array(
    arr: list | np.ndarray, dtype: np.dtype, copy: bool = False
) -> np.ndarray:
    """
    Takes any dtype and returns the casted version, raising for when data is
    incompatible with integer/unsigned integer dtypes.

    Parameters
    ----------
    arr : np.ndarray or list
        The array to cast.
    dtype : np.dtype
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
        if not isinstance(arr, np.ndarray):
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

    if is_float_dtype(arr.dtype):
        if not np.isfinite(arr).all():
            raise IntCastingNaNError(
                "Cannot convert non-finite values (NA or inf) to integer"
            )
        raise ValueError("Trying to coerce float values to integers")
    if is_object_dtype(arr.dtype):
        raise ValueError("Trying to coerce float values to integers")

    if casted.dtype < arr.dtype:
        # GH#41734 e.g. [1, 200, 923442] and dtype="int8" -> overflows
        warnings.warn(
            f"Values are too large to be losslessly cast to {dtype}. "
            "In a future version this will raise OverflowError. To retain the "
            f"old behavior, use pd.Series(values).astype({dtype})",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return casted

    if arr.dtype.kind in ["m", "M"]:
        # test_constructor_maskedarray_nonfloat
        warnings.warn(
            f"Constructing Series or DataFrame from {arr.dtype} values and "
            f"dtype={dtype} is deprecated and will raise in a future version. "
            "Use values.view(dtype) instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return casted

    # No known cases that get here, but raising explicitly to cover our bases.
    raise ValueError(f"values cannot be losslessly cast to {dtype}")
