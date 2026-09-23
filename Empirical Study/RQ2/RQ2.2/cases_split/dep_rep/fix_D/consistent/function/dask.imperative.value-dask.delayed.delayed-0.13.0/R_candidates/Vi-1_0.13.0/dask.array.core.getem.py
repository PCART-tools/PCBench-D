def getem(arr, chunks, shape=None, out_name=None, fancy=True, lock=False):
    """ Dask getting various chunks from an array-like

    >>> getem('X', chunks=(2, 3), shape=(4, 6))  # doctest: +SKIP
    {('X', 0, 0): (getarray, 'X', (slice(0, 2), slice(0, 3))),
     ('X', 1, 0): (getarray, 'X', (slice(2, 4), slice(0, 3))),
     ('X', 1, 1): (getarray, 'X', (slice(2, 4), slice(3, 6))),
     ('X', 0, 1): (getarray, 'X', (slice(0, 2), slice(3, 6)))}

    >>> getem('X', chunks=((2, 2), (3, 3)))  # doctest: +SKIP
    {('X', 0, 0): (getarray, 'X', (slice(0, 2), slice(0, 3))),
     ('X', 1, 0): (getarray, 'X', (slice(2, 4), slice(0, 3))),
     ('X', 1, 1): (getarray, 'X', (slice(2, 4), slice(3, 6))),
     ('X', 0, 1): (getarray, 'X', (slice(0, 2), slice(3, 6)))}
    """
    out_name = out_name or arr
    chunks = normalize_chunks(chunks, shape)

    keys = list(product([out_name], *[range(len(bds)) for bds in chunks]))
    slices = slices_from_chunks(chunks)
    getter = getarray if fancy else getarray_nofancy

    if lock:
        values = [(getter, arr, x, lock) for x in slices]
    else:
        values = [(getter, arr, x) for x in slices]

    return dict(zip(keys, values))
