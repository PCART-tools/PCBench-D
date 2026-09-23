def frexp(x):
    # Not actually object dtype, just need to specify something
    tmp = elemwise(np.frexp, x, dtype=object)
    left = 'mantissa-' + tmp.name
    right = 'exponent-' + tmp.name
    ldsk = dict(((left,) + key[1:], (getitem, key, 0))
                for key in core.flatten(tmp._keys()))
    rdsk = dict(((right,) + key[1:], (getitem, key, 1))
                for key in core.flatten(tmp._keys()))

    a = np.empty((1, ), dtype=x.dtype)
    l, r = np.frexp(a)
    ldt = l.dtype
    rdt = r.dtype

    L = Array(merge(tmp.dask, ldsk), left, chunks=tmp.chunks, dtype=ldt)
    R = Array(merge(tmp.dask, rdsk), right, chunks=tmp.chunks, dtype=rdt)
    return L, R
