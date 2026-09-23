def slice_with_dask_array(x, index):
    y = elemwise(getitem, x, index, dtype=x.dtype)

    name = 'getitem-' + tokenize(x, index)

    dsk = {(name, i): k
           for i, k in enumerate(core.flatten(y._keys()))}
    chunks = ((np.nan,) * y.npartitions,)

    return Array(merge(y.dask, dsk), name, chunks, x.dtype)
