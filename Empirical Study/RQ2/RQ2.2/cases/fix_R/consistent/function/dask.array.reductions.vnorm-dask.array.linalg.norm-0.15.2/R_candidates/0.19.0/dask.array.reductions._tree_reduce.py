def _tree_reduce(x, aggregate, axis, keepdims, dtype, split_every=None,
                 combine=None, name=None, concatenate=True):
    """ Perform the tree reduction step of a reduction.

    Lower level, users should use ``reduction`` or ``arg_reduction`` directly.
    """
    # Normalize split_every
    split_every = split_every or config.get('split_every', 4)
    if isinstance(split_every, dict):
        split_every = dict((k, split_every.get(k, 2)) for k in axis)
    elif isinstance(split_every, int):
        n = builtins.max(int(split_every ** (1 / (len(axis) or 1))), 2)
        split_every = dict.fromkeys(axis, n)
    else:
        raise ValueError("split_every must be a int or a dict")

    # Reduce across intermediates
    depth = 1
    for i, n in enumerate(x.numblocks):
        if i in split_every and split_every[i] != 1:
            depth = int(builtins.max(depth, ceil(log(n, split_every[i]))))
    func = partial(combine or aggregate, axis=axis, keepdims=True)
    if concatenate:
        func = compose(func, partial(_concatenate2, axes=axis))
    for i in range(depth - 1):
        x = partial_reduce(func, x, split_every, True, dtype=dtype,
                           name=(name or funcname(combine or aggregate)) + '-partial')
    func = partial(aggregate, axis=axis, keepdims=keepdims)
    if concatenate:
        func = compose(func, partial(_concatenate2, axes=axis))
    return partial_reduce(func, x, split_every, keepdims=keepdims, dtype=dtype,
                          name=(name or funcname(aggregate)) + '-aggregate')
