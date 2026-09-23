def get_dependencies(dsk, key=None, task=None, as_list=False):
    """ Get the immediate tasks on which this task depends

    Examples
    --------
    >>> dsk = {'x': 1,
    ...        'y': (inc, 'x'),
    ...        'z': (add, 'x', 'y'),
    ...        'w': (inc, 'z'),
    ...        'a': (add, (inc, 'x'), 1)}

    >>> get_dependencies(dsk, 'x')
    set([])

    >>> get_dependencies(dsk, 'y')
    set(['x'])

    >>> get_dependencies(dsk, 'z')  # doctest: +SKIP
    set(['x', 'y'])

    >>> get_dependencies(dsk, 'w')  # Only direct dependencies
    set(['z'])

    >>> get_dependencies(dsk, 'a')  # Ignore non-keys
    set(['x'])

    >>> get_dependencies(dsk, task=(inc, 'x'))  # provide tasks directly
    set(['x'])
    """
    if key is not None:
        arg = dsk[key]
    elif task is not None:
        arg = task
    else:
        raise ValueError("Provide either key or task")

    result = []
    work = [arg]

    while work:
        new_work = []
        for w in work:
            typ = type(w)
            if typ is tuple and w and callable(w[0]):  # istask(w)
                new_work += w[1:]
            elif typ is list:
                new_work += w
            elif typ is dict:
                new_work += w.values()
            else:
                try:
                    if w in dsk:
                        result.append(w)
                except TypeError:  # not hashable
                    pass
        work = new_work

    return result if as_list else set(result)
