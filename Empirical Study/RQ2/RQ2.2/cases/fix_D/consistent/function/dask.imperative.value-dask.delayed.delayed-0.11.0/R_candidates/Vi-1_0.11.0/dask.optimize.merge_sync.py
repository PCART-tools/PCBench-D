def merge_sync(dsk1, dsk2):
    """Merge two dasks together, combining equivalent tasks.

    If a task in `dsk2` exists in `dsk1`, the task and key from `dsk1` is used.
    If a task in `dsk2` has the same key as a task in `dsk1` (and they aren't
    equivalent tasks), then a new key is created for the task in `dsk2`. This
    prevents name conflicts.

    Parameters
    ----------
    dsk1, dsk2 : dict
        Variable names in `dsk2` are replaced with equivalent ones in `dsk1`
        before merging.

    Returns
    -------
    new_dsk : dict
        The merged dask.
    key_map : dict
        A mapping between the keys from `dsk2` to their new names in `new_dsk`.

    Examples
    --------
    >>> from operator import add, mul
    >>> dsk1 = {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5)}
    >>> dsk2 = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    >>> new_dsk, key_map = merge_sync(dsk1, dsk2)
    >>> new_dsk     # doctest: +SKIP
    {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5), 'z': (mul, 'b', 2)}
    >>> key_map     # doctest: +SKIP
    {'x': 'a', 'y': 'b', 'z': 'z'}

    Conflicting names are replaced with auto-generated names upon merging.

    >>> dsk1 = {'a': 1, 'res': (add, 'a', 1)}
    >>> dsk2 = {'x': 1, 'res': (add, 'x', 2)}
    >>> new_dsk, key_map = merge_sync(dsk1, dsk2)
    >>> new_dsk     # doctest: +SKIP
    {'a': 1, 'res': (add, 'a', 1), 'merge_1': (add, 'a', 2)}
    >>> key_map     # doctest: +SKIP
    {'x': 'a', 'res': 'merge_1'}
    """

    dsk2_topo = toposort(dsk2)
    sd = _sync_keys(dsk1, dsk2, dsk2_topo)
    new_dsk = dsk1.copy()
    for key in dsk2_topo:
        if key in sd:
            new_key = sd[key]
        else:
            if key in dsk1:
                new_key = next(merge_sync.names)
            else:
                new_key = key
            sd[key] = new_key
        task = dsk2[key]
        for a, b in sd.items():
            task = subs(task, a, b)
        new_dsk[new_key] = task
    return new_dsk, sd
