def _get_dtype_from_object(dtype):
    """Get a numpy dtype.type-style object. This handles the datetime64[ns]
    and datetime64[ns, TZ] compat

    Notes
    -----
    If nothing can be found, returns ``object``.
    """
    # type object from a dtype
    if isinstance(dtype, type) and issubclass(dtype, np.generic):
        return dtype
    elif is_categorical(dtype):
        return gt.CategoricalDtype().type
    elif is_datetimetz(dtype):
        return gt.DatetimeTZDtype(dtype).type
    elif isinstance(dtype, np.dtype):  # dtype object
        try:
            _validate_date_like_dtype(dtype)
        except TypeError:
            # should still pass if we don't have a datelike
            pass
        return dtype.type
    elif isinstance(dtype, compat.string_types):
        if dtype == 'datetime' or dtype == 'timedelta':
            dtype += '64'

        try:
            return _get_dtype_from_object(getattr(np, dtype))
        except (AttributeError, TypeError):
            # handles cases like _get_dtype(int)
            # i.e., python objects that are valid dtypes (unlike user-defined
            # types, in general)
            # TypeError handles the float16 typecode of 'e'
            # further handle internal types
            pass

    return _get_dtype_from_object(np.dtype(dtype))
