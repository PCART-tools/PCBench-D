def cast_scalar_to_array(shape, value, dtype: Optional[DtypeObj] = None) -> np.ndarray:
    """
    Create np.ndarray of specified shape and dtype, filled with values.

    Parameters
    ----------
    shape : tuple
    value : scalar value
    dtype : np.dtype, optional
        dtype to coerce

    Returns
    -------
    ndarray of shape, filled with value, of specified / inferred dtype

    """
    if dtype is None:
        dtype, fill_value = infer_dtype_from_scalar(value)
    else:
        fill_value = value

    values = np.empty(shape, dtype=dtype)
    values.fill(fill_value)

    return values
