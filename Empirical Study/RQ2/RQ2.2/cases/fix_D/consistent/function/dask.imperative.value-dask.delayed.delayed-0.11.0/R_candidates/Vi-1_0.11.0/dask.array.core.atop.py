def atop(func, out_ind, *args, **kwargs):
    """ Tensor operation: Generalized inner and outer products

    A broad class of blocked algorithms and patterns can be specified with a
    concise multi-index notation.  The ``atop`` function applies an in-memory
    function across multiple blocks of multiple inputs in a variety of ways.

    Parameters
    ----------
    func: callable
        Function to apply to individual tuples of blocks
    out_ind: iterable
        Block pattern of the output, something like 'ijk' or (1, 2, 3)
    *args: sequence of Array, index pairs
        Sequence like (x, 'ij', y, 'jk', z, 'i')
    **kwargs: dict
        Extra keyword arguments to pass to function

    This is best explained through example.  Consider the following examples:

    Examples
    --------

    2D embarrassingly parallel operation from two arrays, x, and y.

    >>> z = atop(operator.add, 'ij', x, 'ij', y, 'ij')  # z = x + y  # doctest: +SKIP

    Outer product multiplying x by y, two 1-d vectors

    >>> z = atop(operator.mul, 'ij', x, 'i', y, 'j')  # doctest: +SKIP

    z = x.T

    >>> z = atop(np.transpose, 'ji', x, 'ij')  # doctest: +SKIP

    The transpose case above is illustrative because it does same transposition
    both on each in-memory block by calling ``np.transpose`` and on the order
    of the blocks themselves, by switching the order of the index ``ij -> ji``.

    We can compose these same patterns with more variables and more complex
    in-memory functions

    z = X + Y.T

    >>> z = atop(lambda x, y: x + y.T, 'ij', x, 'ij', y, 'ji')  # doctest: +SKIP

    Any index, like ``i`` missing from the output index is interpreted as a
    contraction (note that this differs from Einstein convention; repeated
    indices do not imply contraction.)  In the case of a contraction the passed
    function should expect an iterator of blocks on any array that holds that
    index.

    Inner product multiplying x by y, two 1-d vectors

    >>> def sequence_dot(x_blocks, y_blocks):
    ...     result = 0
    ...     for x, y in zip(x_blocks, y_blocks):
    ...         result += x.dot(y)
    ...     return result

    >>> z = atop(sequence_dot, '', x, 'i', y, 'i')  # doctest: +SKIP

    Many dask.array operations are special cases of atop.  These tensor
    operations cover a broad subset of NumPy and this function has been battle
    tested, supporting tricky concepts like broadcasting.

    See Also
    --------
    top - dict formulation of this function, contains most logic
    """
    out = kwargs.pop('name', None)      # May be None at this point
    token = kwargs.pop('token', None)
    dtype = kwargs.pop('dtype', None)

    chunkss, arrays = unify_chunks(*args)
    arginds = list(zip(arrays, args[1::2]))

    numblocks = dict([(a.name, a.numblocks) for a, _ in arginds])
    argindsstr = list(concat([(a.name, ind) for a, ind in arginds]))
    # Finish up the name
    if not out:
        out = '%s-%s' % (token or funcname(func),
                         tokenize(func, out_ind, argindsstr, dtype, **kwargs))

    dsk = top(func, out, out_ind, *argindsstr, numblocks=numblocks, **kwargs)
    dsks = [a.dask for a, _ in arginds]
    chunks = tuple(chunkss[i] for i in out_ind)

    return Array(merge(dsk, *dsks), out, chunks, dtype=dtype)
