def sem(a, axis=0, ddof=1):
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    s = a.std(axis=axis, ddof=ddof) / ma.sqrt(n)
    return s
