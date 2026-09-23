def maybe_upcast(
    values: NumpyArrayT,
    fill_value: Scalar = np.nan,
    copy: bool = False,
) -> tuple[NumpyArrayT, Scalar]:
    """
    Provide explicit type promotion and coercion.

    Parameters
    ----------
    values : np.ndarray
        The array that we may want to upcast.
    fill_value : what we want to fill with
    copy : bool, default True
        If True always make a copy even if no upcast is required.

    Returns
    -------
    values: np.ndarray
        the original array, possibly upcast
    fill_value:
        the fill value, possibly upcast
    """
    new_dtype, fill_value = maybe_promote(values.dtype, fill_value)
    # We get a copy in all cases _except_ (values.dtype == new_dtype and not copy)
    values = values.astype(new_dtype, copy=copy)

    return values, fill_value
