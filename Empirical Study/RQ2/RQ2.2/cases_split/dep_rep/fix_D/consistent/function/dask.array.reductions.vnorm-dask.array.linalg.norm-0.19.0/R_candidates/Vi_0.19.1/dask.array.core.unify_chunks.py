def unify_chunks(*args, **kwargs):
    """
    Unify chunks across a sequence of arrays

    Parameters
    ----------
    *args: sequence of Array, index pairs
        Sequence like (x, 'ij', y, 'jk', z, 'i')

    Examples
    --------
    >>> import dask.array as da
    >>> x = da.ones(10, chunks=((5, 2, 3),))
    >>> y = da.ones(10, chunks=((2, 3, 5),))
    >>> chunkss, arrays = unify_chunks(x, 'i', y, 'i')
    >>> chunkss
    {'i': (2, 3, 2, 3)}

    >>> x = da.ones((100, 10), chunks=(20, 5))
    >>> y = da.ones((10, 100), chunks=(4, 50))
    >>> chunkss, arrays = unify_chunks(x, 'ij', y, 'jk')
    >>> chunkss  # doctest: +SKIP
    {'k': (50, 50), 'i': (20, 20, 20, 20, 20), 'j': (4, 1, 3, 2)}

    Returns
    -------
    chunkss : dict
        Map like {index: chunks}.
    arrays : list
        List of rechunked arrays.

    See Also
    --------
    common_blockdim
    """
    if not args:
        return {}, []

    arginds = [(asarray(a) if ind is not None else a, ind)
               for a, ind in partition(2, args)]  # [x, ij, y, jk]
    args = list(concat(arginds))  # [(x, ij), (y, jk)]
    warn = kwargs.get('warn', True)

    arrays, inds = zip(*arginds)
    if all(ind == inds[0] for ind in inds) and all(a.chunks == arrays[0].chunks for a in arrays):
        return dict(zip(inds[0], arrays[0].chunks)), arrays

    nameinds = [(a.name if i is not None else a, i) for a, i in arginds]
    blockdim_dict = {a.name: a.chunks
                     for a, ind in arginds
                     if ind is not None}

    chunkss = broadcast_dimensions(nameinds, blockdim_dict,
                                   consolidate=common_blockdim)
    max_parts = max(arg.npartitions for arg, ind in arginds if ind is not None)
    nparts = np.prod(list(map(len, chunkss.values())))

    if warn and nparts and nparts >= max_parts * 10:
        warnings.warn("Increasing number of chunks by factor of %d" %
                      (nparts / max_parts), PerformanceWarning, stacklevel=3)

    arrays = []
    for a, i in arginds:
        if i is None:
            arrays.append(a)
        else:
            chunks = tuple(chunkss[j] if a.shape[n] > 1 else a.shape[n]
                           if not np.isnan(sum(chunkss[j])) else None
                           for n, j in enumerate(i))
            if chunks != a.chunks and all(a.chunks):
                arrays.append(a.rechunk(chunks))
            else:
                arrays.append(a)
    return chunkss, arrays
