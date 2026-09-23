def _deps(dsk, arg):
    """ Get dependencies from keys or tasks

    Helper function for get_dependencies.

    >>> dsk = {'x': 1, 'y': 2}

    >>> _deps(dsk, 'x')
    ['x']
    >>> _deps(dsk, (add, 'x', 1))
    ['x']
    >>> _deps(dsk, ['x', 'y'])
    ['x', 'y']
    >>> _deps(dsk, {'a': 'x'})
    ['x']
    >>> _deps(dsk, (add, 'x', (inc, 'y')))  # doctest: +SKIP
    ['x', 'y']
    """
    if istask(arg):
        result = []
        for a in arg[1:]:
            result.extend(_deps(dsk, a))
        return result
    if type(arg) is list:
        return sum([_deps(dsk, a) for a in arg], [])
    if type(arg) is dict:
        return sum([_deps(dsk, v) for v in arg.values()], [])
    try:
        if arg not in dsk:
            return []
    except TypeError:  # not hashable
            return []
    return [arg]
