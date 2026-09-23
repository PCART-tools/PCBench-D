def from_array(x, chunks, name=None, lock=False, fancy=True):
    """ Create dask array from something that looks like an array

    Input must have a ``.shape`` and support numpy-style slicing.

    Parameters
    ----------
    x : array_like
    chunks : int, tuple
        How to chunk the array. Must be one of the following forms:
        - A blocksize like 1000.
        - A blockshape like (1000, 1000).
        - Explicit sizes of all blocks along all dimensions
          like ((1000, 1000, 500), (400, 400)).
    name : str, optional
        The key name to use for the array. Defaults to a hash of ``x``.
        Use ``name=False`` to generate a random name instead of hashing (fast)
    lock : bool or Lock, optional
        If ``x`` doesn't support concurrent reads then provide a lock here, or
        pass in True to have dask.array create one for you.
    fancy : bool, optional
        If ``x`` doesn't support fancy indexing (e.g. indexing with lists or
        arrays) then set to False. Default is True.

    Examples
    --------

    >>> x = h5py.File('...')['/data/path']  # doctest: +SKIP
    >>> a = da.from_array(x, chunks=(1000, 1000))  # doctest: +SKIP

    If your underlying datastore does not support concurrent reads then include
    the ``lock=True`` keyword argument or ``lock=mylock`` if you want multiple
    arrays to coordinate around the same lock.

    >>> a = da.from_array(x, chunks=(1000, 1000), lock=True)  # doctest: +SKIP
    """
    chunks = normalize_chunks(chunks, x.shape)
    if len(chunks) != len(x.shape):
        raise ValueError("Input array has %d dimensions but the supplied "
                         "chunks has only %d dimensions" %
                         (len(x.shape), len(chunks)))
    if tuple(map(sum, chunks)) != x.shape:
        raise ValueError("Chunks do not add up to shape. "
                         "Got chunks=%s, shape=%s" % (chunks, x.shape))
    if name in (None, True):
        token = tokenize(x, chunks)
        original_name = 'array-original-' + token
        name = name or 'array-' + token
    elif name is False:
        original_name = name = 'array-' + str(uuid.uuid1())
    else:
        original_name = name
    if lock is True:
        lock = SerializableLock()
    dsk = getem(original_name, chunks, out_name=name, fancy=fancy, lock=lock)
    dsk[original_name] = x
    return Array(dsk, name, chunks, dtype=x.dtype)
