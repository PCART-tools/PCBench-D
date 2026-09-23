def cull(dsk, keys):
    """ Return new dask with only the tasks required to calculate keys.

    In other words, remove unnecessary tasks from dask.
    ``keys`` may be a single key or list of keys.

    Examples
    --------
    >>> d = {'x': 1, 'y': (inc, 'x'), 'out': (add, 'x', 10)}
    >>> dsk, dependencies = cull(d, 'out')  # doctest: +SKIP
    >>> dsk  # doctest: +SKIP
    {'x': 1, 'out': (add, 'x', 10)}
    >>> dependencies  # doctest: +SKIP
    {'x': set(), 'out': set(['x'])}

    Returns
    -------
    dsk: culled dask graph
    dependencies: Dict mapping {key: [deps]}.  Useful side effect to accelerate
        other optimizations, notably fuse.
    """
    if not isinstance(keys, (list, set)):
        keys = [keys]
    out = dict()
    seen = set()
    dependencies = dict()
    stack = list(set(flatten(keys)))
    while stack:
        key = stack.pop()
        out[key] = dsk[key]
        deps = get_dependencies(dsk, key, as_list=True)  # fuse needs lists
        dependencies[key] = deps
        unseen = [d for d in deps if d not in seen]
        stack.extend(unseen)
        seen.update(unseen)
    return out, dependencies
