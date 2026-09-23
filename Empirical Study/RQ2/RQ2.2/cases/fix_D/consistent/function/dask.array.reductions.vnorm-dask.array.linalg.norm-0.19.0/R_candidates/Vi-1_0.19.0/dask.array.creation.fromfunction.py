@wraps(np.fromfunction)
def fromfunction(func, chunks=None, shape=None, dtype=None):
    if chunks:
        chunks = normalize_chunks(chunks, shape)
    name = 'fromfunction-' + tokenize(func, chunks, shape, dtype)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))
    aggdims = [list(accumulate(add, (0,) + bd[:-1])) for bd in chunks]
    offsets = list(product(*aggdims))
    shapes = list(product(*chunks))

    values = [(np.fromfunction, offset_func(func, offset), shp)
              for offset, shp in zip(offsets, shapes)]

    dsk = dict(zip(keys, values))

    return Array(dsk, name, chunks, dtype=dtype)
