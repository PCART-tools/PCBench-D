def tmin(a, lowerlimit=None, axis=0, inclusive=True):
    a, axis = _chk_asarray(a, axis)
    am = trima(a, (lowerlimit, None), (inclusive, False))
    return ma.minimum.reduce(am, axis)
