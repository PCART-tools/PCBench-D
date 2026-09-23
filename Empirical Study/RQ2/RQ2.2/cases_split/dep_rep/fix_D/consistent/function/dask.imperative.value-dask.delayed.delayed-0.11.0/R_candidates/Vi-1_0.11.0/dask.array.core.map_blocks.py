def map_blocks(func, *args, **kwargs):
    """ Map a function across all blocks of a dask array

    Parameters
    ----------
    func: callable
        Function to apply to every block in the array
    args: dask arrays or constants
    dtype: np.dtype
        Datatype of resulting array
    chunks: tuple (optional)
        chunk shape of resulting blocks if the function does not preserve shape
    drop_axis: number or iterable (optional)
        Dimensions lost by the function
    new_axis: number or iterable (optional)
        New dimensions created by the function
    **kwargs:
        Other keyword arguments to pass to function.
        Values must be constants (not dask.arrays)

    You must also specify the chunks and dtype of the resulting array.  If you
    don't then we assume that the resulting array has the same block structure
    as the input.

    Examples
    --------

    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)

    >>> x.map_blocks(lambda x: x * 2).compute()
    array([ 0,  2,  4,  6,  8, 10])

    The ``da.map_blocks`` function can also accept multiple arrays

    >>> d = da.arange(5, chunks=2)
    >>> e = da.arange(5, chunks=2)

    >>> f = map_blocks(lambda a, b: a + b**2, d, e)
    >>> f.compute()
    array([ 0,  2,  6, 12, 20])

    If function changes shape of the blocks then please provide chunks
    explicitly.

    >>> y = x.map_blocks(lambda x: x[::2], chunks=((2, 2),))

    You have a bit of freedom in specifying chunks.  If all of the output chunk
    sizes are the same, you can provide just that chunk size as a single tuple.

    >>> a = da.arange(18, chunks=(6,))
    >>> b = a.map_blocks(lambda x: x[:3], chunks=(3,))

    If the function changes the dimension of the blocks you must specify the
    created or destroyed dimensions.

    >>> b = a.map_blocks(lambda x: x[None, :, None], chunks=(1, 6, 1),
    ...                  new_axis=[0, 2])


    Map_blocks aligns blocks by block positions without regard to shape.  In
    the following example we have two arrays with the same number of blocks but
    with different shape and chunk sizes.

    >>> x = da.arange(1000, chunks=(100,))
    >>> y = da.arange(100, chunks=(10,))

    The relevant attribute to match is numblocks

    >>> x.numblocks
    (10,)
    >>> y.numblocks
    (10,)

    If these must match (up to broadcasting rules) then we can map arbitrary
    functions across blocks

    >>> def func(a, b):
    ...     return np.array([a.max(), b.max()])

    >>> da.map_blocks(func, x, y, chunks=(2,), dtype='i8')
    dask.array<..., shape=(20,), dtype=int64, chunksize=(2,)>

    >>> _.compute()
    array([ 99,   9, 199,  19, 299,  29, 399,  39, 499,  49, 599,  59, 699,
            69, 799,  79, 899,  89, 999,  99])

    Your block function can learn where in the array it is if it supports a
    ``block_id`` keyword argument.  This will receive entries like (2, 0, 1),
    the position of the block in the dask array.

    >>> def func(block, block_id=None):
    ...     pass

    You may specify the name of the resulting task in the graph with the
    optional ``name`` keyword argument.

    >>> y = x.map_blocks(lambda x: x + 1, name='increment')
    """
    if not callable(func):
        raise TypeError("First argument must be callable function, not %s\n"
                "Usage:   da.map_blocks(function, x)\n"
                "   or:   da.map_blocks(function, x, y, z)" %
                type(func).__name__)
    name = kwargs.pop('name', None)
    name = name or '%s-%s' % (funcname(func), tokenize(func, args, **kwargs))
    dtype = kwargs.pop('dtype', None)
    chunks = kwargs.pop('chunks', None)
    drop_axis = kwargs.pop('drop_axis', [])
    new_axis = kwargs.pop('new_axis', [])
    if isinstance(drop_axis, Number):
        drop_axis = [drop_axis]
    if isinstance(new_axis, Number):
        new_axis = [new_axis]

    arrs = [a for a in args if isinstance(a, Array)]
    args = [(i, a) for i, a in enumerate(args) if not isinstance(a, Array)]

    arginds = [(a, tuple(range(a.ndim))[::-1]) for a in arrs]

    numblocks = dict([(a.name, a.numblocks) for a, _ in arginds])
    argindsstr = list(concat([(a.name, ind) for a, ind in arginds]))
    out_ind = tuple(range(max(a.ndim for a in arrs)))[::-1]

    if args:
        dsk = top(partial_by_order, name, out_ind, *argindsstr,
                numblocks=numblocks, function=func, other=args,
                **kwargs)
    else:
        dsk = top(func, name, out_ind, *argindsstr, numblocks=numblocks,
                **kwargs)

    # If func has block_id as an argument then swap out func
    # for func with block_id partialed in
    try:
        spec = getargspec(func)
    except:
        spec = None
    if spec:
        args = spec.args
        try:
            args += spec.kwonlyargs
        except AttributeError:
            pass
        if 'block_id' in args:
            for k in dsk.keys():
                dsk[k] = (partial(func, block_id=k[1:]),) + dsk[k][1:]

    numblocks = list(arrs[0].numblocks)

    if drop_axis:
        dsk = dict((tuple(k for i, k in enumerate(k)
                             if i - 1 not in drop_axis), v)
                    for k, v in dsk.items())
        numblocks = [n for i, n in enumerate(numblocks) if i not in drop_axis]

    if new_axis:
        dsk, old_dsk = dict(), dsk
        for key in old_dsk:
            new_key = list(key)
            for i in new_axis:
                new_key.insert(i + 1, 0)
            dsk[tuple(new_key)] = old_dsk[key]
        for i in sorted(new_axis, reverse=False):
            numblocks.insert(i, 1)

    if chunks is not None and chunks and not isinstance(chunks[0], tuple):
        chunks = [nb * (bs,) for nb, bs in zip(numblocks, chunks)]
    if chunks is not None:
        chunks = tuple(chunks)
    else:
        chunks = broadcast_chunks(*[a.chunks for a in arrs])

    return Array(merge(dsk, *[a.dask for a in arrs]), name, chunks, dtype)
