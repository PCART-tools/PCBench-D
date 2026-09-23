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
    warn = kwargs.get('warn', True)
    arginds = list(partition(2, args)) # [x, ij, y, jk] -> [(x, ij), (y, jk)]

    nameinds = [(a.name, i) for a, i in arginds]
    blockdim_dict = dict((a.name, a.chunks) for a, _ in arginds)

    chunkss = broadcast_dimensions(nameinds, blockdim_dict,
                                   consolidate=common_blockdim)
    max_parts = max(arg.npartitions for arg in args[::2])
    nparts = np.prod(list(map(len, chunkss.values())))

    if warn and nparts and nparts >= max_parts * 10:
        warnings.warn("Increasing number of chunks by factor of %d" %
                      (nparts / max_parts))

    arrays = []
    for a, i in arginds:
        chunks = tuple(chunkss[j] if a.shape[n] > 1 else a.shape[n]
                       if not np.isnan(sum(chunkss[j])) else None
                       for n, j in enumerate(i))
        if chunks != a.chunks and all(a.chunks):
            arrays.append(a.rechunk(chunks))
        else:
            arrays.append(a)
    return chunkss, arrays
