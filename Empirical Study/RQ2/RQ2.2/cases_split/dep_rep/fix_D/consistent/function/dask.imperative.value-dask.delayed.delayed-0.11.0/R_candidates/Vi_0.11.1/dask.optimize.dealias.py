def dealias(dsk, keys=None, dependencies=None):
    """ Remove aliases from dask

    Removes and renames aliases using ``inline``. Optional ``keys`` keyword
    argument protects keys from being deleted. This is useful to protect keys
    that would be expected by a scheduler. If not provided, all inlined aliases
    are removed.

    Examples
    --------
    >>> dsk = {'a': (range, 5),
    ...        'b': 'a',
    ...        'c': 'b',
    ...        'd': (sum, 'c'),
    ...        'e': 'd',
    ...        'f': (inc, 'd')}

    >>> dealias(dsk)  # doctest: +SKIP
    {'a': (range, 5),
     'd': (sum, 'a'),
     'f': (inc, 'd')}

    >>> dsk = {'a': (range, 5),
    ...        'b': 'a'}
    >>> dealias(dsk)  # doctest: +SKIP
    {'a': (range, 5)}

    >>> dealias(dsk, keys=['a', 'b'])  # doctest: +SKIP
    {'a': (range, 5),
     'b': 'a'}
    """
    keys = keys or set()
    if not isinstance(keys, set):
        keys = set(keys)

    if not dependencies:
        dependencies = dict((k, get_dependencies(dsk, k)) for k in dsk)

    aliases = set(k for k, task in dsk.items() if
                  ishashable(task) and task in dsk)

    dsk2 = inline(dsk, aliases, inline_constants=False)
    for k in aliases.difference(keys):
        del dsk2[k]
    return dsk2
