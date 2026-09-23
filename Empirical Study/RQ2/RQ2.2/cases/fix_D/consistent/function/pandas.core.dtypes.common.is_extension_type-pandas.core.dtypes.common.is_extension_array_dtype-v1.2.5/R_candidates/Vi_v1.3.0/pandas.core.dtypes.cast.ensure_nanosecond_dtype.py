def ensure_nanosecond_dtype(dtype: DtypeObj) -> DtypeObj:
    """
    Convert dtypes with granularity less than nanosecond to nanosecond

    >>> ensure_nanosecond_dtype(np.dtype("M8[s]"))
    dtype('<M8[ns]')

    >>> ensure_nanosecond_dtype(np.dtype("m8[ps]"))
    Traceback (most recent call last):
        ...
    TypeError: cannot convert timedeltalike to dtype [timedelta64[ps]]
    """
    msg = (
        f"The '{dtype.name}' dtype has no unit. "
        f"Please pass in '{dtype.name}[ns]' instead."
    )

    # unpack e.g. SparseDtype
    dtype = getattr(dtype, "subtype", dtype)

    if not isinstance(dtype, np.dtype):
        # i.e. datetime64tz
        pass

    elif dtype.kind == "M" and dtype != DT64NS_DTYPE:
        # pandas supports dtype whose granularity is less than [ns]
        # e.g., [ps], [fs], [as]
        if dtype <= np.dtype("M8[ns]"):
            if dtype.name == "datetime64":
                raise ValueError(msg)
            dtype = DT64NS_DTYPE
        else:
            raise TypeError(f"cannot convert datetimelike to dtype [{dtype}]")

    elif dtype.kind == "m" and dtype != TD64NS_DTYPE:
        # pandas supports dtype whose granularity is less than [ns]
        # e.g., [ps], [fs], [as]
        if dtype <= np.dtype("m8[ns]"):
            if dtype.name == "timedelta64":
                raise ValueError(msg)
            dtype = TD64NS_DTYPE
        else:
            raise TypeError(f"cannot convert timedeltalike to dtype [{dtype}]")
    return dtype
