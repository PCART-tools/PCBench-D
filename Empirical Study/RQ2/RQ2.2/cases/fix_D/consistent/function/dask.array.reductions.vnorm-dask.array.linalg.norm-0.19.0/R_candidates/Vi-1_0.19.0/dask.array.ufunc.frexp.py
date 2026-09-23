@copy_docstring(source=np.frexp)
def frexp(x):
    # Not actually object dtype, just need to specify something
    tmp = elemwise(np.frexp, x, dtype=object)
    left = 'mantissa-' + tmp.name
    right = 'exponent-' + tmp.name
    ldsk = {(left,) + key[1:]: (getitem, key, 0)
            for key in core.flatten(tmp.__dask_keys__())}
    rdsk = {(right,) + key[1:]: (getitem, key, 1)
            for key in core.flatten(tmp.__dask_keys__())}

    a = np.empty((1, ), dtype=x.dtype)
    l, r = np.frexp(a)
    ldt = l.dtype
    rdt = r.dtype

    L = Array(sharedict.merge(tmp.dask, (left, ldsk)), left, chunks=tmp.chunks, dtype=ldt)
    R = Array(sharedict.merge(tmp.dask, (right, rdsk)), right, chunks=tmp.chunks, dtype=rdt)
    return L, R
