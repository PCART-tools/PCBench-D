def percentile(a, q, interpolation='linear'):
    """ Approximate percentile of 1-D array

    See :func:`numpy.percentile` for more information
    """
    if not a.ndim == 1:
        raise NotImplementedError(
            "Percentiles only implemented for 1-d arrays")
    if isinstance(q, Number):
        q = [q]
    q = np.array(q)
    token = tokenize(a, list(q), interpolation)
    name = 'percentile_chunk-' + token
    dsk = dict(((name, i), (_percentile, (key), q, interpolation))
               for i, key in enumerate(a.__dask_keys__()))

    name2 = 'percentile-' + token
    dsk2 = {(name2, 0): (merge_percentiles, q, [q] * len(a.chunks[0]),
                         sorted(dsk), interpolation)}

    dtype = a.dtype
    if np.issubdtype(dtype, np.integer):
        dtype = (np.array([], dtype=dtype) / 0.5).dtype

    dsk = merge(dsk, dsk2)
    dsk = sharedict.merge(a.dask, (name2, dsk))
    return Array(dsk, name2, chunks=((len(q),),), dtype=dtype)
