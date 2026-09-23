def persist(*args, **kwargs):
    """ Persist multiple Dask collections into memory

    This turns lazy Dask collections into Dask collections with the same
    metadata, but now with their results fully computed or actively computing
    in the background.

    For example a lazy dask.array built up from many lazy calls will now be a
    dask.array of the same shape, dtype, chunks, etc., but now with all of
    those previously lazy tasks either computed in memory as many small NumPy
    arrays (in the single-machine case) or asynchronously running in the
    background on a cluster (in the distributed case).

    This function operates differently if a ``dask.distributed.Client`` exists
    and is connected to a distributed scheduler.  In this case this function
    will return as soon as the task graph has been submitted to the cluster,
    but before the computations have completed.  Computations will continue
    asynchronously in the background.  When using this function with the single
    machine scheduler it blocks until the computations have finished.

    When using Dask on a single machine you should ensure that the dataset fits
    entirely within memory.

    Examples
    --------
    >>> df = dd.read_csv('/path/to/*.csv')  # doctest: +SKIP
    >>> df = df[df.name == 'Alice']  # doctest: +SKIP
    >>> df['in-debt'] = df.balance < 0  # doctest: +SKIP
    >>> df = df.persist()  # triggers computation  # doctest: +SKIP

    >>> df.value().min()  # future computations are now fast  # doctest: +SKIP
    -10
    >>> df.value().max()  # doctest: +SKIP
    100

    >>> from dask import persist  # use persist function on multiple collections
    >>> a, b = persist(a, b)  # doctest: +SKIP

    Parameters
    ----------
    *args: Dask collections
    get : callable, optional
        A scheduler ``get`` function to use. If not provided, the default
        is to check the global settings first, and then fall back to
        the collection defaults.
    optimize_graph : bool, optional
        If True [default], the graph is optimized before computation.
        Otherwise the graph is run as is. This can be useful for debugging.
    **kwargs
        Extra keywords to forward to the scheduler ``get`` function.

    Returns
    -------
    New dask collections backed by in-memory data
    """
    collections = [a for a in args if isinstance(a, Base)]
    if not collections:
        return args

    try:
        from distributed.client import default_client
    except ImportError:
        pass
    else:
        try:
            client = default_client()
        except ValueError:
            pass
        else:
            collections = client.persist(collections, **kwargs)
            if isinstance(collections, list):  # distributed is inconsistent here
                collections = tuple(collections)
            else:
                collections = (collections,)
            results_iter = iter(collections)
            return tuple(a if not isinstance(a, Base)
                         else next(results_iter)
                         for a in args)

    optimize_graph = kwargs.pop('optimize_graph', True)

    get = kwargs.pop('get', None) or _globals['get']

    if not get:
        get = collections[0]._default_get
        if not all(a._default_get == get for a in collections):
            raise ValueError("Compute called on multiple collections with "
                             "differing default schedulers. Please specify a "
                             "scheduler `get` function using either "
                             "the `get` kwarg or globally with `set_options`.")

    dsk = collections_to_dsk(collections, optimize_graph, **kwargs)
    keys = list(flatten([var._keys() for var in collections]))
    results = get(dsk, keys, **kwargs)

    d = dict(zip(keys, results))

    result = [redict_collection(c, {k: d[k]
                                    for k in flatten(c._keys())})
              for c in collections]
    results_iter = iter(result)
    return tuple(a if not isinstance(a, Base)
                 else next(results_iter)
                 for a in args)
