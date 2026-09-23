def dtype_to_py_type(dtype: PolarsDataType) -> PythonDataType:
    """Convert a Polars dtype to a Python dtype."""
    try:
        dtype = dtype.base_type()
        return DataTypeMappings.DTYPE_TO_PY_TYPE[dtype]
    except KeyError:  # pragma: no cover
        raise NotImplementedError(
            f"conversion of polars data type {dtype!r} to Python type not implemented"
        ) from None
