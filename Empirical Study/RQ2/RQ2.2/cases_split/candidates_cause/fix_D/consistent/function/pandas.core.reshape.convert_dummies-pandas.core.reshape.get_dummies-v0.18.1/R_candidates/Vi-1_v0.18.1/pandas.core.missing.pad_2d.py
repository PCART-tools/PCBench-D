def pad_2d(values, limit=None, mask=None, dtype=None):

    if dtype is None:
        dtype = values.dtype
    _method = None
    if com.is_float_dtype(values):
        _method = getattr(algos, 'pad_2d_inplace_%s' % dtype.name, None)
    elif dtype in com._DATELIKE_DTYPES or com.is_datetime64_dtype(values):
        _method = _pad_2d_datetime
    elif com.is_integer_dtype(values):
        values = com._ensure_float64(values)
        _method = algos.pad_2d_inplace_float64
    elif values.dtype == np.object_:
        _method = algos.pad_2d_inplace_object

    if _method is None:
        raise ValueError('Invalid dtype for pad_2d [%s]' % dtype.name)

    if mask is None:
        mask = com.isnull(values)
    mask = mask.view(np.uint8)

    if np.all(values.shape):
        _method(values, mask, limit=limit)
    else:
        # for test coverage
        pass
    return values
