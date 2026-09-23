def infer_dtype_from_object(dtype) -> DtypeObj:
    """
    Get a numpy dtype.type-style object for a dtype object.

    This methods also includes handling of the datetime64[ns] and
    datetime64[ns, TZ] objects.

    If no dtype can be found, we return ``object``.

    Parameters
    ----------
    dtype : dtype, type
        The dtype object whose numpy dtype.type-style
        object we want to extract.

    Returns
    -------
    dtype_object : The extracted numpy dtype.type-style object.
    """
    if isinstance(dtype, type) and issubclass(dtype, np.generic):
        # Type object from a dtype

        # error: Incompatible return value type (got "Type[generic]", expected
        # "Union[dtype[Any], ExtensionDtype]")
        return dtype  # type: ignore[return-value]
    elif isinstance(dtype, (np.dtype, ExtensionDtype)):
        # dtype object
        try:
            _validate_date_like_dtype(dtype)
        except TypeError:
            # Should still pass if we don't have a date-like
            pass
        # error: Incompatible return value type (got "Union[Type[generic], Type[Any]]",
        # expected "Union[dtype[Any], ExtensionDtype]")
        return dtype.type  # type: ignore[return-value]

    try:
        dtype = pandas_dtype(dtype)
    except TypeError:
        pass

    if is_extension_array_dtype(dtype):
        return dtype.type
    elif isinstance(dtype, str):

        # TODO(jreback)
        # should deprecate these
        if dtype in ["datetimetz", "datetime64tz"]:
            # error: Incompatible return value type (got "Type[Any]", expected
            # "Union[dtype[Any], ExtensionDtype]")
            return DatetimeTZDtype.type  # type: ignore[return-value]
        elif dtype in ["period"]:
            raise NotImplementedError

        if dtype in ["datetime", "timedelta"]:
            dtype += "64"
        try:
            return infer_dtype_from_object(getattr(np, dtype))
        except (AttributeError, TypeError):
            # Handles cases like get_dtype(int) i.e.,
            # Python objects that are valid dtypes
            # (unlike user-defined types, in general)
            #
            # TypeError handles the float16 type code of 'e'
            # further handle internal types
            pass

    return infer_dtype_from_object(np.dtype(dtype))
