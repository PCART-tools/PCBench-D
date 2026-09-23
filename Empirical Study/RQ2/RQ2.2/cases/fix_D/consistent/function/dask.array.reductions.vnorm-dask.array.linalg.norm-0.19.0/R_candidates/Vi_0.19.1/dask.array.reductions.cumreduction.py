def cumreduction(func, binop, ident, x, axis=None, dtype=None, out=None):
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
    if axis is None:
        x = x.flatten()
        axis = 0
    if dtype is None:
        dtype = getattr(func(np.empty((0,), dtype=x.dtype)), 'dtype', object)
    assert isinstance(axis, int)
    axis = validate_axis(axis, x.ndim)

    m = x.map_blocks(func, axis=axis, dtype=dtype)

    name = '{0}-{1}'.format(func.__name__, tokenize(func, axis, binop,
                                                    ident, x, dtype))
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

    result = Array(sharedict.merge(m.dask, (name, dsk)), name, x.chunks, m.dtype)
    return handle_out(out, result)
