def dtype_to_ffiname(dtype: PolarsDataType) -> str:
    """Return FFI function name associated with the given Polars dtype."""
    try:
        dtype = dtype.base_type()
        return DataTypeMappings.DTYPE_TO_FFINAME[dtype]
    except KeyError:  # pragma: no cover
        raise NotImplementedError(
            f"conversion of polars data type {dtype!r} to FFI not implemented"
        ) from None
