def inline_singleton_lists(dsk, dependencies=None):
    """ Inline lists that are only used once

    >>> d = {'b': (list, 'a'),
    ...      'c': (f, 'b', 1)}     # doctest: +SKIP
    >>> inline_singleton_lists(d)  # doctest: +SKIP
    {'c': (f, (list, 'a'), 1)}

    Pairs nicely with lazify afterwards
    """
    if dependencies is None:
        dependencies = dict((k, get_dependencies(dsk, k)) for k in dsk)
    dependents = reverse_dict(dependencies)

    keys = [k for k, v in dsk.items()
            if istask(v) and v and v[0] is list and len(dependents[k]) == 1]
    dsk = inline(dsk, keys, inline_constants=False)
    for k in keys:
        del dsk[k]
    return dsk
