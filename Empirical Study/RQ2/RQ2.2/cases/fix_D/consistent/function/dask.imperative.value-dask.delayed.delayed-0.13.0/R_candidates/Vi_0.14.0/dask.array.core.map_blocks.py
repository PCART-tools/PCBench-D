def map_blocks(func, *args, **kwargs):
    """ Map a function across all blocks of a dask array.

    Parameters
    ----------
    func : callable
        Function to apply to every block in the array.
    args : dask arrays or constants
    dtype : np.dtype, optional
        The ``dtype`` of the output array. It is recommended to provide this.
        If not provided, will be inferred by applying the function to a small
        set of fake data.
    chunks : tuple, optional
        Chunk shape of resulting blocks if the function does not preserve
        shape. If not provided, the resulting array is assumed to have the same
        block structure as the first input array.
    drop_axis : number or iterable, optional
        Dimensions lost by the function.
    new_axis : number or iterable, optional
        New dimensions created by the function.
    name : string, optional
        The key name to use for the array. If not provided, will be determined
        by a hash of the arguments.
    **kwargs :
        Other keyword arguments to pass to function. Values must be constants
        (not dask.arrays)

    Examples
    --------
    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)

    >>> x.map_blocks(lambda x: x * 2).compute()
    array([ 0,  2,  4,  6,  8, 10])

    The ``da.map_blocks`` function can also accept multiple arrays.

    >>> d = da.arange(5, chunks=2)
    >>> e = da.arange(5, chunks=2)

    >>> f = map_blocks(lambda a, b: a + b**2, d, e)
    >>> f.compute()
    array([ 0,  2,  6, 12, 20])

    If the function changes shape of the blocks then you must provide chunks
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

    Map_blocks aligns blocks by block positions without regard to shape. In the
    following example we have two arrays with the same number of blocks but
    with different shape and chunk sizes.

    >>> x = da.arange(1000, chunks=(100,))
    >>> y = da.arange(100, chunks=(10,))

    The relevant attribute to match is numblocks.

    >>> x.numblocks
    (10,)
    >>> y.numblocks
    (10,)

    If these match (up to broadcasting rules) then we can map arbitrary
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
        msg = ("First argument must be callable function, not %s\n"
               "Usage:   da.map_blocks(function, x)\n"
               "   or:   da.map_blocks(function, x, y, z)")
        raise TypeError(msg % type(func).__name__)
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

    if drop_axis and new_axis:
        raise ValueError("Can't specify drop_axis and new_axis together")

    arrs = [a for a in args if isinstance(a, Array)]
    other = [(i, a) for i, a in enumerate(args) if not isinstance(a, Array)]

    argpairs = [(a.name, tuple(range(a.ndim))[::-1]) for a in arrs]
    numblocks = {a.name: a.numblocks for a in arrs}
    arginds = list(concat(argpairs))
    out_ind = tuple(range(max(a.ndim for a in arrs)))[::-1]

    try:
        spec = getargspec(func)
        block_id = ('block_id' in spec.args or
                    'block_id' in getattr(spec, 'kwonly_args', ()))
    except:
        block_id = False

    if block_id:
        kwargs['block_id'] = '__dummy__'

    if other:
        dsk = top(partial_by_order, name, out_ind, *arginds,
                  numblocks=numblocks, function=func, other=other,
                  **kwargs)
    else:
        dsk = top(func, name, out_ind, *arginds, numblocks=numblocks,
                  **kwargs)

    # If func has block_id as an argument, add it to the kwargs for each call
    if block_id:
        for k in dsk.keys():
            dsk[k] = dsk[k][:-1] + (assoc(dsk[k][-1], 'block_id', k[1:]),)

    if dtype is None:
        if block_id:
            kwargs2 = assoc(kwargs, 'block_id', first(dsk.keys())[1:])
        else:
            kwargs2 = kwargs
        dtype = apply_infer_dtype(func, args, kwargs2, 'map_blocks')

    if len(arrs) == 1:
        numblocks = list(arrs[0].numblocks)
    else:
        dims = broadcast_dimensions(argpairs, numblocks)
        numblocks = [b for (_, b) in sorted(dims.items(), reverse=True)]

    if drop_axis:
        if any(numblocks[i] > 1 for i in drop_axis):
            raise ValueError("Can't drop an axis with more than 1 block. "
                             "Please use `atop` instead.")
        dsk = dict((tuple(k for i, k in enumerate(k)
                          if i - 1 not in drop_axis), v)
                   for k, v in dsk.items())
        numblocks = [n for i, n in enumerate(numblocks) if i not in drop_axis]
    elif new_axis:
        dsk, old_dsk = dict(), dsk
        for key in old_dsk:
            new_key = list(key)
            for i in new_axis:
                new_key.insert(i + 1, 0)
            dsk[tuple(new_key)] = old_dsk[key]
        for i in sorted(new_axis):
            numblocks.insert(i, 1)

    if chunks:
        if len(chunks) != len(numblocks):
            raise ValueError("Provided chunks have {0} dims, expected {1} "
                             "dims.".format(len(chunks), len(numblocks)))
        chunks2 = []
        for i, (c, nb) in enumerate(zip(chunks, numblocks)):
            if isinstance(c, tuple):
                if not len(c) == nb:
                    raise ValueError("Dimension {0} has {1} blocks, "
                                     "chunks specified with "
                                     "{2} blocks".format(i, nb, len(c)))
                chunks2.append(c)
            else:
                chunks2.append(nb * (c,))
    else:
        if len(arrs) == 1:
            chunks2 = list(arrs[0].chunks)
        else:
            try:
                chunks2 = list(broadcast_chunks(*[a.chunks for a in arrs]))
            except:
                raise ValueError("Arrays in `map_blocks` don't align, can't "
                                 "infer output chunks. Please provide "
                                 "`chunks` kwarg.")
        if drop_axis:
            chunks2 = [c for (i, c) in enumerate(chunks2) if i not in drop_axis]
        elif new_axis:
            for i in sorted(new_axis):
                chunks2.insert(i, (1,))

    chunks = tuple(chunks2)

    return Array(sharedict.merge((name, dsk), *[a.dask for a in arrs]),
                 name, chunks, dtype)
