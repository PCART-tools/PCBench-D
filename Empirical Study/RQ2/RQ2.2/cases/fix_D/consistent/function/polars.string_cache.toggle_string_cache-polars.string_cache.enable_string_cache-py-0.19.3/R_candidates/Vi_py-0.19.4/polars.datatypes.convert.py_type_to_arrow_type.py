def py_type_to_arrow_type(dtype: PythonDataType) -> pa.lib.DataType:
    """Convert a Python dtype to an Arrow dtype."""
    try:
        return DataTypeMappings.PY_TYPE_TO_ARROW_TYPE[dtype]
    except KeyError:  # pragma: no cover
        raise ValueError(
            f"cannot parse Python data type {dtype!r} into Arrow data type"
        ) from None
