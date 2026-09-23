def numpy_char_code_to_dtype(dtype_char: str) -> PolarsDataType:
    """Convert a numpy character dtype to a Polars dtype."""
    dtype = np.dtype(dtype_char)
    if dtype.kind == "U":
        return Utf8
    try:
        return DataTypeMappings.NUMPY_KIND_AND_ITEMSIZE_TO_DTYPE[
            (dtype.kind, dtype.itemsize)
        ]
    except KeyError:  # pragma: no cover
        raise ValueError(
            f"cannot parse numpy data type {dtype!r} into Polars data type"
        ) from None
