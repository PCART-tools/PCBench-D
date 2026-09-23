def reduction(x, chunk, aggregate, axis=None, keepdims=None, dtype=None,
              split_every=None, combine=None, name=None):
    """ General version of reductions

    >>> reduction(my_array, np.sum, np.sum, axis=0, keepdims=False)  # doctest: +SKIP
    """
    if axis is None:
        axis = tuple(range(x.ndim))
    if isinstance(axis, int):
        axis = (axis,)
    axis = tuple(i if i >= 0 else x.ndim + i for i in axis)

    if dtype is not None and 'dtype' in getargspec(chunk).args:
        chunk = partial(chunk, dtype=dtype)
    if dtype is not None and 'dtype' in getargspec(aggregate).args:
        aggregate = partial(aggregate, dtype=dtype)

    # Map chunk across all blocks
    inds = tuple(range(x.ndim))
    tmp = atop(chunk, inds, x, inds, axis=axis, keepdims=True)
    tmp._chunks = tuple((1, ) * len(c) if i in axis else c for (i, c)
                        in enumerate(tmp.chunks))

    return _tree_reduce(tmp, aggregate, axis, keepdims, dtype, split_every,
                       combine, name=name)
