def _get_dtype_from_object(dtype):
    """Get a numpy dtype.type-style object.

    Notes
    -----
    If nothing can be found, returns ``object``.
    """
    # type object from a dtype
    if isinstance(dtype, type) and issubclass(dtype, np.generic):
        return dtype
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
        elif dtype == 'category':
            return CategoricalDtypeType
        try:
            return _get_dtype_from_object(getattr(np, dtype))
        except AttributeError:
            # handles cases like _get_dtype(int)
            # i.e., python objects that are valid dtypes (unlike user-defined
            # types, in general)
            pass
    return _get_dtype_from_object(np.dtype(dtype))
