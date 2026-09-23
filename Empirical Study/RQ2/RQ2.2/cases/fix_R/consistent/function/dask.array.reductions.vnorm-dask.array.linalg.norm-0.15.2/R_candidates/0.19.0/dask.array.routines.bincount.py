@wraps(np.bincount)
def bincount(x, weights=None, minlength=None):
    if minlength is None:
        raise TypeError("Must specify minlength argument in da.bincount")
    assert x.ndim == 1
    if weights is not None:
        assert weights.chunks == x.chunks

    # Call np.bincount on each block, possibly with weights
    token = tokenize(x, weights, minlength)
    name = 'bincount-' + token
    if weights is not None:
        dsk = {(name, i): (np.bincount, (x.name, i), (weights.name, i), minlength)
               for i, _ in enumerate(x.__dask_keys__())}
        dtype = np.bincount([1], weights=[1]).dtype
    else:
        dsk = {(name, i): (np.bincount, (x.name, i), None, minlength)
               for i, _ in enumerate(x.__dask_keys__())}
        dtype = np.bincount([]).dtype

    # Sum up all of the intermediate bincounts per block
    name = 'bincount-sum-' + token
    dsk[(name, 0)] = (np.sum, list(dsk), 0)

    chunks = ((minlength,),)

    dsk = sharedict.merge((name, dsk), x.dask)
    if weights is not None:
        dsk.update(weights.dask)

    return Array(dsk, name, chunks, dtype)
