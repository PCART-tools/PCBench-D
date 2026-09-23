def hmean(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    if isinstance(a, MaskedArray):
        size = a.count(axis)
    else:
        size = a.shape[axis]
    return size / (1.0/a).sum(axis)
