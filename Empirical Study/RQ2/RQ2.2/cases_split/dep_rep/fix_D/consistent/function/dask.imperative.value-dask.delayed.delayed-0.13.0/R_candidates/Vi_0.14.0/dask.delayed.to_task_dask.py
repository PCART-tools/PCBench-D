def to_task_dask(expr):
    """Normalize a python object and merge all sub-graphs.

    - Replace ``Delayed`` with their keys
    - Convert literals to things the schedulers can handle
    - Extract dask graphs from all enclosed values

    Parameters
    ----------
    expr : object
        The object to be normalized. This function knows how to handle
        ``Delayed``s, as well as most builtin python types.

    Returns
    -------
    task : normalized task to be run
    dask : a merged dask graph that forms the dag for this task

    Examples
    --------
    >>> a = delayed(1, 'a')
    >>> b = delayed(2, 'b')
    >>> task, dask = to_task_dask([a, b, 3])
    >>> task  # doctest: +SKIP
    ['a', 'b', 3]
    >>> dict(dask)  # doctest: +SKIP
    {'a': 1, 'b': 2}

    >>> task, dasks = to_task_dask({a: 1, b: 2})
    >>> task  # doctest: +SKIP
    (dict, [['a', 1], ['b', 2]])
    >>> dict(dask)  # doctest: +SKIP
    {'a': 1, 'b': 2}
    """
    if isinstance(expr, Delayed):
        return expr.key, expr.dask
    if isinstance(expr, base.Base):
        name = 'finalize-' + tokenize(expr, pure=True)
        keys = expr._keys()
        dsk = expr._optimize(dict(expr.dask), keys)
        dsk[name] = (expr._finalize, (concrete, keys))
        return name, dsk
    if isinstance(expr, tuple) and type(expr) != tuple:
        return expr, {}
    if isinstance(expr, (Iterator, list, tuple, set)):
        args, dasks = unzip((to_task_dask(e) for e in expr), 2)
        args = list(args)
        dsk = sharedict.merge(*dasks)
        # Ensure output type matches input type
        if isinstance(expr, (tuple, set)):
            return (type(expr), args), dsk
        else:
            return args, dsk
    if isinstance(expr, dict):
        args, dsk = to_task_dask([[k, v] for k, v in expr.items()])
        return (dict, args), dsk
    return expr, {}
