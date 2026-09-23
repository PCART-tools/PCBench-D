def maybe_downcast_to_dtype(result: ArrayLike, dtype: str | np.dtype) -> ArrayLike:
    """
    try to cast to the specified dtype (e.g. convert back to bool/int
    or could be an astype of float64->float32
    """
    do_round = False

    if isinstance(dtype, str):
        if dtype == "infer":
            inferred_type = lib.infer_dtype(result, skipna=False)
            if inferred_type == "boolean":
                dtype = "bool"
            elif inferred_type == "integer":
                dtype = "int64"
            elif inferred_type == "datetime64":
                dtype = "datetime64[ns]"
            elif inferred_type in ["timedelta", "timedelta64"]:
                dtype = "timedelta64[ns]"

            # try to upcast here
            elif inferred_type == "floating":
                dtype = "int64"
                if issubclass(result.dtype.type, np.number):
                    do_round = True

            else:
                # TODO: complex?  what if result is already non-object?
                dtype = "object"

        dtype = np.dtype(dtype)

    if not isinstance(dtype, np.dtype):
        # enforce our signature annotation
        raise TypeError(dtype)  # pragma: no cover

    converted = maybe_downcast_numeric(result, dtype, do_round)
    if converted is not result:
        return converted

    # a datetimelike
    # GH12821, iNaT is cast to float
    if dtype.kind in ["M", "m"] and result.dtype.kind in ["i", "f"]:
        result = result.astype(dtype)

    elif dtype.kind == "m" and result.dtype == _dtype_obj:
        # test_where_downcast_to_td64
        result = cast(np.ndarray, result)
        result = array_to_timedelta64(result)

    elif dtype == np.dtype("M8[ns]") and result.dtype == _dtype_obj:
        result = cast(np.ndarray, result)
        return np.asarray(maybe_cast_to_datetime(result, dtype=dtype))

    return result
