def interpolate_2d(values, method='pad', axis=0, limit=None, fill_value=None, dtype=None):
    """ perform an actual interpolation of values, values will be make 2-d if
    needed fills inplace, returns the result
    """

    transf = (lambda x: x) if axis == 0 else (lambda x: x.T)

    # reshape a 1 dim if needed
    ndim = values.ndim
    if values.ndim == 1:
        if axis != 0:  # pragma: no cover
            raise AssertionError("cannot interpolate on a ndim == 1 with "
                                 "axis != 0")
        values = values.reshape(tuple((1,) + values.shape))

    if fill_value is None:
        mask = None
    else:  # todo create faster fill func without masking
        mask = mask_missing(transf(values), fill_value)

    method = _clean_fill_method(method)
    if method == 'pad':
        values = transf(pad_2d(transf(values), limit=limit, mask=mask, dtype=dtype))
    else:
        values = transf(backfill_2d(transf(values), limit=limit, mask=mask, dtype=dtype))

    # reshape back
    if ndim == 1:
        values = values[0]

    return values
