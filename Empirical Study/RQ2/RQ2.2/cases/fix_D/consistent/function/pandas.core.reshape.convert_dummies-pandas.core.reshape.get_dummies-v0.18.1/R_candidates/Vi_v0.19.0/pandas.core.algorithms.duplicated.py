def duplicated(values, keep='first'):
    """
    Return boolean ndarray denoting duplicate values

    .. versionadded:: 0.19.0

    Parameters
    ----------
    keep : {'first', 'last', False}, default 'first'
        - ``first`` : Mark duplicates as ``True`` except for the first
          occurrence.
        - ``last`` : Mark duplicates as ``True`` except for the last
          occurrence.
        - False : Mark all duplicates as ``True``.

    Returns
    -------
    duplicated : ndarray
    """

    dtype = values.dtype

    # no need to revert to original type
    if needs_i8_conversion(dtype):
        values = values.view(np.int64)
    elif is_period_arraylike(values):
        from pandas.tseries.period import PeriodIndex
        values = PeriodIndex(values).asi8
    elif is_categorical_dtype(dtype):
        values = values.values.codes
    elif isinstance(values, (ABCSeries, ABCIndex)):
        values = values.values

    if is_integer_dtype(dtype):
        values = _ensure_int64(values)
        duplicated = htable.duplicated_int64(values, keep=keep)
    elif is_float_dtype(dtype):
        values = _ensure_float64(values)
        duplicated = htable.duplicated_float64(values, keep=keep)
    else:
        values = _ensure_object(values)
        duplicated = htable.duplicated_object(values, keep=keep)

    return duplicated
