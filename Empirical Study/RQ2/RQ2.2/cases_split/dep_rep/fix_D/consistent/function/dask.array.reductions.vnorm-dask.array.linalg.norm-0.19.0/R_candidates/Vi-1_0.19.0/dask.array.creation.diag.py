@wraps(np.diag)
def diag(v):
    name = 'diag-' + tokenize(v)
    if isinstance(v, np.ndarray):
        if v.ndim == 1:
            chunks = ((v.shape[0],), (v.shape[0],))
            dsk = {(name, 0, 0): (np.diag, v)}
        elif v.ndim == 2:
            chunks = ((min(v.shape),),)
            dsk = {(name, 0): (np.diag, v)}
        else:
            raise ValueError("Array must be 1d or 2d only")
        return Array(dsk, name, chunks, dtype=v.dtype)
    if not isinstance(v, Array):
        raise TypeError("v must be a dask array or numpy array, "
                        "got {0}".format(type(v)))
    if v.ndim != 1:
        if v.chunks[0] == v.chunks[1]:
            dsk = {(name, i): (np.diag, row[i])
                   for i, row in enumerate(v.__dask_keys__())}
            return Array(sharedict.merge(v.dask, (name, dsk)), name, (v.chunks[0],), dtype=v.dtype)
        else:
            raise NotImplementedError("Extracting diagonals from non-square "
                                      "chunked arrays")
    chunks_1d = v.chunks[0]
    blocks = v.__dask_keys__()
    dsk = {}
    for i, m in enumerate(chunks_1d):
        for j, n in enumerate(chunks_1d):
            key = (name, i, j)
            if i == j:
                dsk[key] = (np.diag, blocks[i])
            else:
                dsk[key] = (np.zeros, (m, n))

    return Array(sharedict.merge(v.dask, (name, dsk)), name, (chunks_1d, chunks_1d),
                 dtype=v.dtype)
