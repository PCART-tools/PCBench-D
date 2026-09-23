def polars_dtype_to_dtype(dtype: PolarsDataType) -> Dtype:
    """Convert Polars data type to interchange protocol data type."""
    try:
        result = dtype_map[dtype.base_type()]
    except KeyError as exc:
        raise ValueError(
            f"data type {dtype!r} not supported by the interchange protocol"
        ) from exc

    # Handle instantiated data types
    if isinstance(dtype, Datetime):
        return _datetime_to_dtype(dtype)
    elif isinstance(dtype, Duration):
        return _duration_to_dtype(dtype)

    return result
