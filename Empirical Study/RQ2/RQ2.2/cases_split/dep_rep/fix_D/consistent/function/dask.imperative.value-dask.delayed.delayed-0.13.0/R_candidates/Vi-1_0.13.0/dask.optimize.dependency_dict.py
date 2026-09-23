def dependency_dict(dsk):
    """Create a dict matching ordered dependencies to keys.

    Examples
    --------
    >>> from operator import add
    >>> dsk = {'a': 1, 'b': 2, 'c': (add, 'a', 'a'), 'd': (add, 'b', 'a')}
    >>> dependency_dict(dsk)    # doctest: +SKIP
    {(): ['a', 'b'], ('a', 'a'): ['c'], ('b', 'a'): ['d']}
    """

    dep_dict = {}
    for key in dsk:
        deps = tuple(get_dependencies(dsk, key, True))
        dep_dict.setdefault(deps, []).append(key)
    return dep_dict
