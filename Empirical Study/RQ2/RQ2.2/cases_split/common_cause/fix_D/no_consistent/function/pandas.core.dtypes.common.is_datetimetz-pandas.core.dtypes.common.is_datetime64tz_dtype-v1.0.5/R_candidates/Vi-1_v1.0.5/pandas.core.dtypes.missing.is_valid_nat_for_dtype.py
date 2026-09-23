def is_valid_nat_for_dtype(obj, dtype) -> bool:
    """
    isna check that excludes incompatible dtypes

    Parameters
    ----------
    obj : object
    dtype : np.datetime64, np.timedelta64, DatetimeTZDtype, or PeriodDtype

    Returns
    -------
    bool
    """
    if not lib.is_scalar(obj) or not isna(obj):
        return False
    if dtype.kind == "M":
        return not isinstance(obj, np.timedelta64)
    if dtype.kind == "m":
        return not isinstance(obj, np.datetime64)

    # must be PeriodDType
    return not isinstance(obj, (np.datetime64, np.timedelta64))
