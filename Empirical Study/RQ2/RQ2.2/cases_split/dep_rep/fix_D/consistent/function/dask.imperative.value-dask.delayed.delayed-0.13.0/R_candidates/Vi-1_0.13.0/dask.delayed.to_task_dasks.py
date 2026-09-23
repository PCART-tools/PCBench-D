def to_task_dasks(expr):
    """Normalize a python object and extract all sub-dasks.

    - Replace ``Delayed`` with their keys
    - Convert literals to things the schedulers can handle
    - Extract dasks from all enclosed values

    Parameters
    ----------
    expr : object
        The object to be normalized. This function knows how to handle
        ``Delayed``s, as well as most builtin python types.

    Returns
    -------
    task : normalized task to be run
    dasks : list of dasks that form the dag for this task

    Examples
    --------

    >>> a = delayed(1, 'a')
    >>> b = delayed(2, 'b')
    >>> task, dasks = to_task_dasks([a, b, 3])
    >>> task # doctest: +SKIP
    ['a', 'b', 3]
    >>> dasks # doctest: +SKIP
    [{'a': 1}, {'b': 2}]

    >>> task, dasks = to_task_dasks({a: 1, b: 2})
    >>> task # doctest: +SKIP
    (dict, [['a', 1], ['b', 2]])
    >>> dasks # doctest: +SKIP
    [{'a': 1}, {'b': 2}]
    """
    if isinstance(expr, Delayed):
        return expr.key, expr._dasks
    if isinstance(expr, base.Base):
        name = 'finalize-' + tokenize(expr, pure=True)
        keys = expr._keys()
        dsk = expr._optimize(expr.dask, keys)
        dsk[name] = (expr._finalize, (concrete, keys))
        return name, [dsk]
    if isinstance(expr, tuple) and type(expr) != tuple:
        return expr, []
    if isinstance(expr, (Iterator, list, tuple, set)):
        args, dasks = unzip((to_task_dasks(e) for e in expr), 2)
        args = list(args)
        dasks = flat_unique(dasks)
        # Ensure output type matches input type
        if isinstance(expr, (tuple, set)):
            return (type(expr), args), dasks
        else:
            return args, dasks
    if isinstance(expr, dict):
        args, dasks = to_task_dasks([[k, v] for k, v in expr.items()])
        return (dict, args), dasks
    return expr, []
