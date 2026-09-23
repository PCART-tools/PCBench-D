def boundaries(x, depth=None, kind=None):
    """ Add boundary conditions to an array before ghosting

    See Also
    --------

    periodic
    constant
    """
    if not isinstance(kind, dict):
        kind = dict((i, kind) for i in range(x.ndim))
    if not isinstance(depth, dict):
        depth = dict((i, depth) for i in range(x.ndim))

    for i in range(x.ndim):
        d = depth.get(i, 0)
        if d == 0:
            continue

        this_kind = kind.get(i, 'none')
        if this_kind == 'none':
            continue
        elif this_kind == 'periodic':
            x = periodic(x, i, d)
        elif this_kind == 'reflect':
            x = reflect(x, i, d)
        elif this_kind == 'nearest':
            x = nearest(x, i, d)
        elif i in kind:
            x = constant(x, i, d, kind[i])

    return x
