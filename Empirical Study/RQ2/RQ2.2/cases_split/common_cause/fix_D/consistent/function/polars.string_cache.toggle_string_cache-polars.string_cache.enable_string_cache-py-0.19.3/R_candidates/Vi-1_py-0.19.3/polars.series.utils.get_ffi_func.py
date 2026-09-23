def get_ffi_func(
    name: str, dtype: PolarsDataType, obj: PySeries
) -> Callable[..., Any] | None:
    """
    Dynamically obtain the proper FFI function/ method.

    Parameters
    ----------
    name
        function or method name where dtype is replaced by <>
        for example
            "call_foo_<>"
    dtype
        polars dtype.
    obj
        Object to find the method for.

    Returns
    -------
    callable or None
        FFI function, or None if not found.

    """
    ffi_name = dtype_to_ffiname(dtype)
    fname = name.replace("<>", ffi_name)
    return getattr(obj, fname, None)
