def compute(*args, **kwargs):
    """Compute several dask collections at once.

    Parameters
    ----------
    args : object
        Any number of objects. If it is a dask object, it's computed and the
        result is returned. By default, python builtin collections are also
        traversed to look for dask objects (for more information see the
        ``traverse`` keyword). Non-dask arguments are passed through unchanged.
    traverse : bool, optional
        By default dask traverses builtin python collections looking for dask
        objects passed to ``compute``. For large collections this can be
        expensive. If none of the arguments contain any dask objects, set
        ``traverse=False`` to avoid doing this traversal.
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

    By default, dask objects inside python collections will also be computed:

    >>> compute({'a': a, 'b': b, 'c': 1})  # doctest: +SKIP
    ({'a': 45, 'b': 4.5, 'c': 1},)
    """
    from dask.delayed import delayed
    traverse = kwargs.pop('traverse', True)
    if traverse:
        args = tuple(delayed(a)
                     if isinstance(a, (list, set, tuple, dict, Iterator))
                     else a for a in args)

    optimize_graph = kwargs.pop('optimize_graph', True)
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

    dsk = collections_to_dsk(variables, optimize_graph, **kwargs)
    keys = [var._keys() for var in variables]
    results = get(dsk, keys, **kwargs)

    results_iter = iter(results)
    return tuple(a if not isinstance(a, Base)
                 else a._finalize(next(results_iter))
                 for a in args)
