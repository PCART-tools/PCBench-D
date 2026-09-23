def insert_to_ooc(arr, out, lock=True, region=None,
                  return_stored=False, load_stored=False, tok=None):
    """
    Creates a Dask graph for storing chunks from ``arr`` in ``out``.

    Parameters
    ----------
    arr: da.Array
        A dask array
    out: array-like
        Where to store results too.
    lock: Lock-like or bool, optional
        Whether to lock or with what (default is ``True``,
        which means a ``threading.Lock`` instance).
    region: slice-like, optional
        Where in ``out`` to store ``arr``'s results
        (default is ``None``, meaning all of ``out``).
    return_stored: bool, optional
        Whether to return ``out``
        (default is ``False``, meaning ``None`` is returned).
    load_stored: bool, optional
        Whether to handling loading from ``out`` at the same time.
        Ignored if ``return_stored`` is not ``True``.
        (default is ``False``, meaning defer to ``return_stored``).
    tok: str, optional
        Token to use when naming keys

    Examples
    --------
    >>> import dask.array as da
    >>> d = da.ones((5, 6), chunks=(2, 3))
    >>> a = np.empty(d.shape)
    >>> insert_to_ooc(d, a)  # doctest: +SKIP
    """

    if lock is True:
        lock = Lock()

    slices = slices_from_chunks(arr.chunks)
    if region:
        slices = [fuse_slice(region, slc) for slc in slices]

    name = 'store-%s' % (tok or str(uuid.uuid1()))
    func = store_chunk
    args = ()
    if return_stored and load_stored:
        name = 'load-%s' % name
        func = load_store_chunk
        args = args + (load_stored,)

    dsk = {
        (name,) + t[1:]: (func, t, out, slc, lock, return_stored) + args
        for t, slc in zip(core.flatten(arr.__dask_keys__()), slices)
    }

    return dsk
