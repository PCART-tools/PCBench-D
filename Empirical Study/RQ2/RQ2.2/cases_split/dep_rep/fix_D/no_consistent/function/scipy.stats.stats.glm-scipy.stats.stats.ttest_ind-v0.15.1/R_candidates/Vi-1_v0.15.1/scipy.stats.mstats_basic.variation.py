def variation(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    return a.std(axis)/a.mean(axis)
