def sem(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    s = a.std(axis=axis,ddof=0) / ma.sqrt(n-1)
    return s
