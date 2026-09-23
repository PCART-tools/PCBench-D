def from_array(x, chunks, name=None, lock=False, asarray=True, fancy=True,
               getitem=None):
    """ Create dask array from something that looks like an array

    Input must have a ``.shape`` and support numpy-style slicing.

    Parameters
    ----------
    x : array_like
    chunks : int, tuple
        How to chunk the array. Must be one of the following forms:
        -   A blocksize like 1000.
        -   A blockshape like (1000, 1000).
        -   Explicit sizes of all blocks along all dimensions like
            ((1000, 1000, 500), (400, 400)).

        -1 as a blocksize indicates the size of the corresponding dimension.
    name : str, optional
        The key name to use for the array. Defaults to a hash of ``x``.
        Use ``name=False`` to generate a random name instead of hashing (fast)
    lock : bool or Lock, optional
        If ``x`` doesn't support concurrent reads then provide a lock here, or
        pass in True to have dask.array create one for you.
    asarray : bool, optional
        If True (default), then chunks will be converted to instances of
        ``ndarray``. Set to False to pass passed chunks through unchanged.
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
    if isinstance(x, (list, tuple, memoryview) + np.ScalarType):
        x = np.array(x)

    chunks = normalize_chunks(chunks, x.shape, dtype=x.dtype)
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

    # Always use the getter for h5py etc. Not using isinstance(x, np.ndarray)
    # because np.matrix is a subclass of np.ndarray.
    if type(x) is np.ndarray and all(len(c) == 1 for c in chunks):
        # No slicing needed
        dsk = {(name, ) + (0, ) * x.ndim: x}
    else:
        if getitem is None:
            if type(x) is np.ndarray:
                # simpler and cleaner, but missing all the nuances of getter
                getitem = operator.getitem
            elif fancy:
                getitem = getter
            else:
                getitem = getter_nofancy

        dsk = getem(original_name, chunks, getitem=getitem, shape=x.shape,
                    out_name=name, lock=lock, asarray=asarray,
                    dtype=x.dtype)
        dsk[original_name] = x

    return Array(dsk, name, chunks, dtype=x.dtype)
