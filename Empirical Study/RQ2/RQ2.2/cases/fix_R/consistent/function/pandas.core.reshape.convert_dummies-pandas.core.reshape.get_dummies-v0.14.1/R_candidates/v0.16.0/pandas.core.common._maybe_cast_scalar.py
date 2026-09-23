def _maybe_cast_scalar(dtype, value):
    """ if we a scalar value and are casting to a dtype that needs nan -> NaT
    conversion
    """
    if np.isscalar(value) and dtype in _DATELIKE_DTYPES and isnull(value):
        return tslib.iNaT
    return value
