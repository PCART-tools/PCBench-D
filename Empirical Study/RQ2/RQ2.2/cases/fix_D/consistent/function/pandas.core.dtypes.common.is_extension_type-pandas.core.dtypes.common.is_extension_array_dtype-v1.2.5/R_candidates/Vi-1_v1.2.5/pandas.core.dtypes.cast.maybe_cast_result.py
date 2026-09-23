def maybe_cast_result(
    result: ArrayLike, obj: "Series", numeric_only: bool = False, how: str = ""
) -> ArrayLike:
    """
    Try casting result to a different type if appropriate

    Parameters
    ----------
    result : array-like
        Result to cast.
    obj : Series
        Input Series from which result was calculated.
    numeric_only : bool, default False
        Whether to cast only numerics or datetimes as well.
    how : str, default ""
        How the result was computed.

    Returns
    -------
    result : array-like
        result maybe casted to the dtype.
    """
    dtype = obj.dtype
    dtype = maybe_cast_result_dtype(dtype, how)

    assert not is_scalar(result)

    if (
        is_extension_array_dtype(dtype)
        and not is_categorical_dtype(dtype)
        and dtype.kind != "M"
    ):
        # We have to special case categorical so as not to upcast
        # things like counts back to categorical
        cls = dtype.construct_array_type()
        result = maybe_cast_to_extension_array(cls, result, dtype=dtype)

    elif numeric_only and is_numeric_dtype(dtype) or not numeric_only:
        result = maybe_downcast_to_dtype(result, dtype)

    return result
