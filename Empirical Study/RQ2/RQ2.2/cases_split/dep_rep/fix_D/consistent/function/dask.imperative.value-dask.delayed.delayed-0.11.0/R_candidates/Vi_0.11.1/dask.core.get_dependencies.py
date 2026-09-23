def get_dependencies(dsk, task, as_list=False):
    """ Get the immediate tasks on which this task depends

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
    """
    args = [dsk[task]]
    result = []
    while args:
        arg = args.pop()
        if istask(arg):
            args.extend(arg[1:])
        elif type(arg) is list:
            args.extend(arg)
        else:
            result.append(arg)
    if not result:
        return [] if as_list else set()
    rv = []
    for x in result:
        rv.extend(_deps(dsk, x))
    return rv if as_list else set(rv)
