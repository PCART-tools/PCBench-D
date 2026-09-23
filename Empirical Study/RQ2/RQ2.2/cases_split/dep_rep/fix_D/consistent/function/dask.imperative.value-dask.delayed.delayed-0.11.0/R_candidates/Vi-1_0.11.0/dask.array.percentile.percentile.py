def percentile(a, q, interpolation='linear'):
    """ Approximate percentile of 1-D array

    See numpy.percentile for more information
    """
    if not a.ndim == 1:
        raise NotImplementedError(
            "Percentiles only implemented for 1-d arrays")
    q = np.array(q)
    token = tokenize(a, list(q), interpolation)
    name = 'percentile_chunk-' + token
    dsk = dict(((name, i), (_percentile, (key), q, interpolation))
            for i, key in enumerate(a._keys()))

    name2 = 'percentile-' + token
    dsk2 = {(name2, 0): (merge_percentiles, q, [q] * len(a.chunks[0]),
                         sorted(dsk), a.chunks[0], interpolation)}

    return Array(merge(a.dask, dsk, dsk2), name2, chunks=((len(q),),))
