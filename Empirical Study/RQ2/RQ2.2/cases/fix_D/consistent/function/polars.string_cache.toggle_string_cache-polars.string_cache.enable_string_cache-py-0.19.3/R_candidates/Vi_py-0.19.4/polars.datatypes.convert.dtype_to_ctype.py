def dtype_to_ctype(dtype: PolarsDataType) -> Any:
    """Convert a Polars dtype to a ctype."""
    try:
        dtype = dtype.base_type()
        return DataTypeMappings.DTYPE_TO_CTYPE[dtype]
    except KeyError:  # pragma: no cover
        raise NotImplementedError(
            f"conversion of polars data type {dtype!r} to C-type not implemented"
        ) from None
