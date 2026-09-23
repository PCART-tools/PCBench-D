def from_array(x, chunks, name=None, lock=False):
    """ Create dask array from something that looks like an array

    Input must have a ``.shape`` and support numpy-style slicing.

    The ``chunks`` argument must be one of the following forms:

    -   a blocksize like 1000
    -   a blockshape like (1000, 1000)
    -   explicit sizes of all blocks along all dimensions
        like ((1000, 1000, 500), (400, 400)).

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
                "chunks has only %d dimensions" % (len(x.shape), len(chunks)))
    token = tokenize(x, chunks)
    original_name = (name or 'array-') + 'original-' + token
    name = name or 'array-' + token
    dsk = getem(original_name, chunks, out_name=name)
    if lock is True:
        lock = Lock()
    if lock:
        dsk = dict((k, v + (lock,)) for k, v in dsk.items())
    return Array(merge({original_name: x}, dsk), name, chunks, dtype=x.dtype)
