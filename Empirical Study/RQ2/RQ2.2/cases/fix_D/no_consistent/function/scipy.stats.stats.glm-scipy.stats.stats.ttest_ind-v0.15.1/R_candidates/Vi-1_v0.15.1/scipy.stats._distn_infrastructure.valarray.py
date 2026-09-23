def valarray(shape, value=nan, typecode=None):
    """Return an array of all value.
    """

    out = ones(shape, dtype=bool) * value
    if typecode is not None:
        out = out.astype(typecode)
    if not isinstance(out, ndarray):
        out = asarray(out)
    return out
