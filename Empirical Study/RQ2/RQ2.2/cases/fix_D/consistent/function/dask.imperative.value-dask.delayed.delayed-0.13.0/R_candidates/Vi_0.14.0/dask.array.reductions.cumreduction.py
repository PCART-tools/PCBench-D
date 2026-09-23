def cumreduction(func, binop, ident, x, axis, dtype=None):
    """ Generic function for cumulative reduction

    Parameters
    ----------
    func: callable
        Cumulative function like np.cumsum or np.cumprod
    binop: callable
        Associated binary operator like ``np.cumsum->add`` or ``np.cumprod->mul``
    ident: Number
        Associated identity like ``np.cumsum->0`` or ``np.cumprod->1``
    x: dask Array
    axis: int
    dtype: dtype

    Returns
    -------
    dask array

    See also
    --------
    cumsum
    cumprod
    """
    if dtype is None:
        dtype = func(np.empty((0,), dtype=x.dtype)).dtype
    assert isinstance(axis, int)
    axis = validate_axis(x.ndim, axis)

    m = x.map_blocks(func, axis=axis, dtype=dtype)

    name = '%s-axis=%d-%s' % (func.__name__, axis, tokenize(x, dtype))
    n = x.numblocks[axis]
    full = slice(None, None, None)
    slc = (full,) * axis + (slice(-1, None),) + (full,) * (x.ndim - axis - 1)

    indices = list(product(*[range(nb) if i != axis else [0]
                             for i, nb in enumerate(x.numblocks)]))
    dsk = dict()
    for ind in indices:
        shape = tuple(x.chunks[i][ii] if i != axis else 1
                      for i, ii in enumerate(ind))
        dsk[(name, 'extra') + ind] = (np.full, shape, ident, m.dtype)
        dsk[(name,) + ind] = (m.name,) + ind

    for i in range(1, n):
        last_indices = indices
        indices = list(product(*[range(nb) if ii != axis else [i]
                                 for ii, nb in enumerate(x.numblocks)]))
        for old, ind in zip(last_indices, indices):
            this_slice = (name, 'extra') + ind
            dsk[this_slice] = (binop, (name, 'extra') + old,
                                      (operator.getitem, (m.name,) + old, slc))
            dsk[(name,) + ind] = (binop, this_slice, (m.name,) + ind)

    return Array(sharedict.merge(m.dask, (name, dsk)), name, x.chunks, m.dtype)
