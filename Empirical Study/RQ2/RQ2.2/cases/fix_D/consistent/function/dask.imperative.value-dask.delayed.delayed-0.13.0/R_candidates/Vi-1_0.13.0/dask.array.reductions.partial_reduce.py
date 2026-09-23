def partial_reduce(func, x, split_every, keepdims=False, dtype=None, name=None):
    """Partial reduction across multiple axes.

    Parameters
    ----------
    func : function
    x : Array
    split_every : dict
        Maximum reduction block sizes in each dimension.

    Examples
    --------
    Reduce across axis 0 and 2, merging a maximum of 1 block in the 0th
    dimension, and 3 blocks in the 2nd dimension:

    >>> partial_reduce(np.min, x, {0: 1, 2: 3})    # doctest: +SKIP
    """
    name = (name or funcname(func)) + '-' + tokenize(func, x, split_every,
                                                     keepdims, dtype)
    parts = [list(partition_all(split_every.get(i, 1), range(n))) for (i, n)
             in enumerate(x.numblocks)]
    keys = product(*map(range, map(len, parts)))
    out_chunks = [tuple(1 for p in partition_all(split_every[i], c)) if i
                  in split_every else c for (i, c) in enumerate(x.chunks)]
    if not keepdims:
        out_axis = [i for i in range(x.ndim) if i not in split_every]
        getter = lambda k: get(out_axis, k)
        keys = map(getter, keys)
        out_chunks = list(getter(out_chunks))
    dsk = {}
    for k, p in zip(keys, product(*parts)):
        decided = dict((i, j[0]) for (i, j) in enumerate(p) if len(j) == 1)
        dummy = dict(i for i in enumerate(p) if i[0] not in decided)
        g = lol_tuples((x.name,), range(x.ndim), decided, dummy)
        dsk[(name,) + k] = (func, g)
    return Array(merge(dsk, x.dask), name, out_chunks, dtype=dtype)
