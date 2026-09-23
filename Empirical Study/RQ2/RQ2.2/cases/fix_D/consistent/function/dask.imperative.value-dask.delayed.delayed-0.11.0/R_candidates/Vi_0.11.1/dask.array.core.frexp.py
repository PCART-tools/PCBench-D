def frexp(x):
    tmp = elemwise(np.frexp, x)
    left = 'mantissa-' + tmp.name
    right = 'exponent-' + tmp.name
    ldsk = dict(((left,) + key[1:], (getitem, key, 0))
                for key in core.flatten(tmp._keys()))
    rdsk = dict(((right,) + key[1:], (getitem, key, 1))
                for key in core.flatten(tmp._keys()))

    if x._dtype is not None:
        a = np.empty((1,), dtype=x._dtype)
        l, r = np.frexp(a)
        ldt = l.dtype
        rdt = r.dtype
    else:
        ldt = None
        rdt = None

    L = Array(merge(tmp.dask, ldsk), left, chunks=tmp.chunks, dtype=ldt)

    R = Array(merge(tmp.dask, rdsk), right, chunks=tmp.chunks, dtype=rdt)

    return L, R
