def numpy_values_and_dtype(
    values: np.ndarray[Any, Any]
) -> tuple[np.ndarray[Any, Any], type]:
    """Return numpy values and their associated dtype, adjusting if required."""
    # Create new dtype object from dtype base name so architecture specific
    # dtypes (np.longlong np.ulonglong np.intc np.uintc np.longdouble, ...)
    # get converted to their normalized dtype (np.int*, np.uint*, np.float*).
    dtype = (
        np.dtype(values.dtype.base.name).type
        if values.dtype.kind in ("i", "u", "f")
        else values.dtype.type
    )

    if dtype == np.float16:
        values = values.astype(np.float32)
        dtype = values.dtype.type
    elif dtype == np.datetime64:
        time_unit = np.datetime_data(values.dtype)[0]
        if time_unit in dt.DTYPE_TEMPORAL_UNITS or time_unit == "D":
            values = values.astype(np.int64)
        else:
            raise ValueError(
                "only 'D', 'ms', 'us', and 'ns' resolutions are supported when converting from numpy.datetime64."
                "\n\nPlease cast to the closest supported unit before converting"
            )
    return values, dtype
