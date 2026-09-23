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
    out_keys = []
    seen = set()
    dependencies = dict()

    work = list(set(flatten(keys)))
    while work:
        new_work = []
        out_keys += work
        deps = [(k, get_dependencies(dsk, k, as_list=True))  # fuse needs lists
                for k in work]
        dependencies.update(deps)
        for _, deplist in deps:
            for d in deplist:
                if d not in seen:
                    seen.add(d)
                    new_work.append(d)
        work = new_work

    out = {k: dsk[k] for k in out_keys}

    return out, dependencies
