def maybe_upcast(
    values: ArrayLike,
    fill_value: Scalar = np.nan,
    dtype: Dtype = None,
    copy: bool = False,
) -> Tuple[ArrayLike, Scalar]:
    """
    Provide explicit type promotion and coercion.

    Parameters
    ----------
    values : ndarray or ExtensionArray
        The array that we want to maybe upcast.
    fill_value : what we want to fill with
    dtype : if None, then use the dtype of the values, else coerce to this type
    copy : bool, default True
        If True always make a copy even if no upcast is required.

    Returns
    -------
    values: ndarray or ExtensionArray
        the original array, possibly upcast
    fill_value:
        the fill value, possibly upcast
    """
    if not is_scalar(fill_value) and not is_object_dtype(values.dtype):
        # We allow arbitrary fill values for object dtype
        raise ValueError("fill_value must be a scalar")

    if is_extension_array_dtype(values):
        if copy:
            values = values.copy()
    else:
        if dtype is None:
            dtype = values.dtype
        new_dtype, fill_value = maybe_promote(dtype, fill_value)
        if new_dtype != values.dtype:
            values = values.astype(new_dtype)
        elif copy:
            values = values.copy()

    return values, fill_value
