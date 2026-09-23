def upcast(func):
    """NumPy fft casts inputs to 64 bit and *returns 64-bit results*."""

    @functools.wraps(func)
    def wrapped(tensor, *args, **kwds):
        target_dtype = (
            _dtypes_impl.default_dtypes().complex_dtype
            if tensor.is_complex()
            else _dtypes_impl.default_dtypes().float_dtype
        )
        tensor = _util.cast_if_needed(tensor, target_dtype)
        return func(tensor, *args, **kwds)

    return wrapped
