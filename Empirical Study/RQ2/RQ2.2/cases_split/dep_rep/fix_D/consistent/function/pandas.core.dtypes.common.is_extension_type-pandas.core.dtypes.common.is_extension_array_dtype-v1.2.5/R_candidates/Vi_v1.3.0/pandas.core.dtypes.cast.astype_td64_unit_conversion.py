def astype_td64_unit_conversion(
    values: np.ndarray, dtype: np.dtype, copy: bool
) -> np.ndarray:
    """
    By pandas convention, converting to non-nano timedelta64
    returns an int64-dtyped array with ints representing multiples
    of the desired timedelta unit.  This is essentially division.

    Parameters
    ----------
    values : np.ndarray[timedelta64[ns]]
    dtype : np.dtype
        timedelta64 with unit not-necessarily nano
    copy : bool

    Returns
    -------
    np.ndarray
    """
    if is_dtype_equal(values.dtype, dtype):
        if copy:
            return values.copy()
        return values

    # otherwise we are converting to non-nano
    result = values.astype(dtype, copy=False)  # avoid double-copying
    result = result.astype(np.float64)

    mask = isna(values)
    np.putmask(result, mask, np.nan)
    return result
