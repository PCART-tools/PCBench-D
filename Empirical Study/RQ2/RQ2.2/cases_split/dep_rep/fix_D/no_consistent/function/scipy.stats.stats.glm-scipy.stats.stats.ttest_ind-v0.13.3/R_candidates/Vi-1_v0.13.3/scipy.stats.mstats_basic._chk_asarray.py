def _chk_asarray(a, axis):
    if axis is None:
        a = ma.ravel(a)
        outaxis = 0
    else:
        a = ma.asanyarray(a)
        outaxis = axis
    return a, outaxis
