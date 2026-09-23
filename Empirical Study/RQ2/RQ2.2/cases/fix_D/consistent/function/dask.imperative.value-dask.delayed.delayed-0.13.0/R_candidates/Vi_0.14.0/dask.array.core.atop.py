def atop(func, out_ind, *args, **kwargs):
    """ Tensor operation: Generalized inner and outer products

    A broad class of blocked algorithms and patterns can be specified with a
    concise multi-index notation.  The ``atop`` function applies an in-memory
    function across multiple blocks of multiple inputs in a variety of ways.
    Many dask.array operations are special cases of atop including elementwise,
    broadcasting, reductions, tensordot, and transpose.

    Parameters
    ----------
    func : callable
        Function to apply to individual tuples of blocks
    out_ind : iterable
        Block pattern of the output, something like 'ijk' or (1, 2, 3)
    *args : sequence of Array, index pairs
        Sequence like (x, 'ij', y, 'jk', z, 'i')
    **kwargs : dict
        Extra keyword arguments to pass to function
    dtype : np.dtype
        Datatype of resulting array.
    concatenate : bool, keyword only
        If true concatenate arrays along dummy indices, else provide lists
    adjust_chunks : dict
        Dictionary mapping index to function to be applied to chunk sizes
    new_axes : dict, keyword only
        New indexes and their dimension lengths

    Examples
    --------
    2D embarrassingly parallel operation from two arrays, x, and y.

    >>> z = atop(operator.add, 'ij', x, 'ij', y, 'ij', dtype='f8')  # z = x + y  # doctest: +SKIP

    Outer product multiplying x by y, two 1-d vectors

    >>> z = atop(operator.mul, 'ij', x, 'i', y, 'j', dtype='f8')  # doctest: +SKIP

    z = x.T

    >>> z = atop(np.transpose, 'ji', x, 'ij', dtype=x.dtype)  # doctest: +SKIP

    The transpose case above is illustrative because it does same transposition
    both on each in-memory block by calling ``np.transpose`` and on the order
    of the blocks themselves, by switching the order of the index ``ij -> ji``.

    We can compose these same patterns with more variables and more complex
    in-memory functions

    z = X + Y.T

    >>> z = atop(lambda x, y: x + y.T, 'ij', x, 'ij', y, 'ji', dtype='f8')  # doctest: +SKIP

    Any index, like ``i`` missing from the output index is interpreted as a
    contraction (note that this differs from Einstein convention; repeated
    indices do not imply contraction.)  In the case of a contraction the passed
    function should expect an iterable of blocks on any array that holds that
    index.  To receive arrays concatenated along contracted dimensions instead
    pass ``concatenate=True``.

    Inner product multiplying x by y, two 1-d vectors

    >>> def sequence_dot(x_blocks, y_blocks):
    ...     result = 0
    ...     for x, y in zip(x_blocks, y_blocks):
    ...         result += x.dot(y)
    ...     return result

    >>> z = atop(sequence_dot, '', x, 'i', y, 'i', dtype='f8')  # doctest: +SKIP

    Add new single-chunk dimensions with the ``new_axes=`` keyword, including
    the length of the new dimension.  New dimensions will always be in a single
    chunk.

    >>> def f(x):
    ...     return x[:, None] * np.ones((1, 5))

    >>> z = atop(f, 'az', x, 'a', new_axes={'z': 5}, dtype=x.dtype)  # doctest: +SKIP

    If the applied function changes the size of each chunk you can specify this
    with a ``adjust_chunks={...}`` dictionary holding a function for each index
    that modifies the dimension size in that index.

    >>> def double(x):
    ...     return np.concatenate([x, x])

    >>> y = atop(double, 'ij', x, 'ij',
    ...          adjust_chunks={'i': lambda n: 2 * n}, dtype=x.dtype)  # doctest: +SKIP

    See Also
    --------
    top - dict formulation of this function, contains most logic
    """
    out = kwargs.pop('name', None)      # May be None at this point
    token = kwargs.pop('token', None)
    dtype = kwargs.pop('dtype', None)
    adjust_chunks = kwargs.pop('adjust_chunks', None)
    new_axes = kwargs.get('new_axes', {})

    if dtype is None:
        raise ValueError("Must specify dtype of output array")

    chunkss, arrays = unify_chunks(*args)
    for k, v in new_axes.items():
        chunkss[k] = (v,)
    arginds = list(zip(arrays, args[1::2]))

    numblocks = dict([(a.name, a.numblocks) for a, _ in arginds])
    argindsstr = list(concat([(a.name, ind) for a, ind in arginds]))
    # Finish up the name
    if not out:
        out = '%s-%s' % (token or funcname(func),
                         tokenize(func, out_ind, argindsstr, dtype, **kwargs))

    dsk = top(func, out, out_ind, *argindsstr, numblocks=numblocks, **kwargs)
    dsks = [a.dask for a, _ in arginds]

    chunks = [chunkss[i] for i in out_ind]
    if adjust_chunks:
        for i, ind in enumerate(out_ind):
            if ind in adjust_chunks:
                if callable(adjust_chunks[ind]):
                    chunks[i] = tuple(map(adjust_chunks[ind], chunks[i]))
                elif isinstance(adjust_chunks[ind], int):
                    chunks[i] = tuple(adjust_chunks[ind] for _ in chunks[i])
                elif isinstance(adjust_chunks[ind], (tuple, list)):
                    chunks[i] = tuple(adjust_chunks[ind])
                else:
                    raise NotImplementedError(
                        "adjust_chunks values must be callable, int, or tuple")
    chunks = tuple(chunks)

    return Array(sharedict.merge((out, dsk), *dsks), out, chunks, dtype=dtype)
