@wraps(np.squeeze)
def squeeze(a, axis=None):
    if 1 not in a.shape:
        return a
    if axis is None:
        axis = tuple(i for i, d in enumerate(a.shape) if d == 1)
    b = a.map_blocks(partial(np.squeeze, axis=axis), dtype=a.dtype)
    chunks = tuple(bd for bd in b.chunks if bd != (1,))
    old_keys = list(product([b.name], *[range(len(bd)) for bd in b.chunks]))
    new_keys = list(product([b.name], *[range(len(bd)) for bd in chunks]))

    dsk = b.dask.copy()
    for o, n in zip(old_keys, new_keys):
        dsk[n] = dsk[o]
        del dsk[o]

    return Array(dsk, b.name, chunks, dtype=a.dtype)
