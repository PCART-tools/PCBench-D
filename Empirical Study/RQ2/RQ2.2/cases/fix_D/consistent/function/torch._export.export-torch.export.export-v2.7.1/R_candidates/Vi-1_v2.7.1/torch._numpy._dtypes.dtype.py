def dtype(arg):
    if arg is None:
        arg = _dtypes_impl.default_dtypes().float_dtype
    return DType(arg)
