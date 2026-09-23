def _chk2_asarray(a, b, axis):
    if axis is None:
        a = ma.ravel(a)
        b = ma.ravel(b)
        outaxis = 0
    else:
        a = ma.asanyarray(a)
        b = ma.asanyarray(b)
        outaxis = axis
    return a, b, outaxis
