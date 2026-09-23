def backfill_1d(values, limit=None, mask=None, dtype=None):

    if dtype is None:
        dtype = values.dtype
    _method = None
    if is_float_dtype(values):
        _method = getattr(algos, 'backfill_inplace_%s' % dtype.name, None)
    elif dtype in _DATELIKE_DTYPES or is_datetime64_dtype(values):
        _method = _backfill_1d_datetime
    elif is_integer_dtype(values):
        values = _ensure_float64(values)
        _method = algos.backfill_inplace_float64
    elif values.dtype == np.object_:
        _method = algos.backfill_inplace_object

    if _method is None:
        raise ValueError('Invalid dtype for backfill_1d [%s]' % dtype.name)

    if mask is None:
        mask = isnull(values)
    mask = mask.view(np.uint8)

    _method(values, mask, limit=limit)
    return values
