def arg_reduction(x, chunk, combine, agg, axis=None, split_every=None):
    """Generic function for argreduction.

    Parameters
    ----------
    x : Array
    chunk : callable
        Partialed ``arg_chunk``.
    combine : callable
        Partialed ``arg_combine``.
    agg : callable
        Partialed ``arg_agg``.
    axis : int, optional
    split_every : int or dict, optional
    """
    if axis is None:
        axis = tuple(range(x.ndim))
        ravel = True
    elif isinstance(axis, int):
        if axis < 0:
            axis += x.ndim
        if axis < 0 or axis >= x.ndim:
            raise ValueError("axis entry is out of bounds")
        axis = (axis,)
        ravel = x.ndim == 1
    else:
        raise TypeError("axis must be either `None` or int, "
                        "got '{0}'".format(axis))

    # Map chunk across all blocks
    name = 'arg-reduce-chunk-{0}'.format(tokenize(chunk, axis))
    old = x.name
    keys = list(product(*map(range, x.numblocks)))
    offsets = list(product(*(accumulate(operator.add, bd[:-1], 0)
                             for bd in x.chunks)))
    if ravel:
        offset_info = zip(offsets, repeat(x.shape))
    else:
        offset_info = pluck(axis[0], offsets)

    chunks = tuple((1, ) * len(c) if i in axis else c for (i, c)
                   in enumerate(x.chunks))
    dsk = dict(((name,) + k, (chunk, (old,) + k, axis, off)) for (k, off)
               in zip(keys, offset_info))
    # The dtype of `tmp` doesn't actually matter, just need to provide something
    tmp = Array(sharedict.merge(x.dask, (name, dsk)), name, chunks, dtype=x.dtype)
    return _tree_reduce(tmp, agg, axis, False, np.int64, split_every, combine)
