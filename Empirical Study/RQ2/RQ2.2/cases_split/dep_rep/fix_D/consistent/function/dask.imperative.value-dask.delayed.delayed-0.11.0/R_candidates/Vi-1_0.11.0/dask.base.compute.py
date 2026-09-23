def compute(*args, **kwargs):
    """Compute several dask collections at once.

    Parameters
    ----------
    args : object
        Any number of objects. If the object is a dask collection, it's
        computed and the result is returned. Otherwise it's passed through
        unchanged.
    get : callable, optional
        A scheduler ``get`` function to use. If not provided, the default is
        to check the global settings first, and then fall back to defaults for
        the collections.
    optimize_graph : bool, optional
        If True [default], the optimizations for each collection are applied
        before computation. Otherwise the graph is run as is. This can be
        useful for debugging.
    kwargs
        Extra keywords to forward to the scheduler ``get`` function.

    Examples
    --------
    >>> import dask.array as da
    >>> a = da.arange(10, chunks=2).sum()
    >>> b = da.arange(10, chunks=2).mean()
    >>> compute(a, b)
    (45, 4.5)
    """
    variables = [a for a in args if isinstance(a, Base)]
    if not variables:
        return args

    get = kwargs.pop('get', None) or _globals['get']

    if not get:
        get = variables[0]._default_get
        if not all(a._default_get == get for a in variables):
            raise ValueError("Compute called on multiple collections with "
                             "differing default schedulers. Please specify a "
                             "scheduler `get` function using either "
                             "the `get` kwarg or globally with `set_options`.")

    if kwargs.get('optimize_graph', True):
        groups = groupby(attrgetter('_optimize'), variables)
        dsk = merge([opt(merge([v.dask for v in val]),
                         [v._keys() for v in val], **kwargs)
                    for opt, val in groups.items()])
    else:
        dsk = merge(var.dask for var in variables)
    keys = [var._keys() for var in variables]
    results = get(dsk, keys, **kwargs)

    results_iter = iter(results)
    return tuple(a if not isinstance(a, Base)
                   else a._finalize(next(results_iter))
                   for a in args)
