def supported_numpy_char_code(dtype_char: str) -> bool:
    """Check if the input can be mapped to a Polars dtype."""
    dtype = np.dtype(dtype_char)
    return (
        dtype.kind,
        dtype.itemsize,
    ) in DataTypeMappings.NUMPY_KIND_AND_ITEMSIZE_TO_DTYPE
