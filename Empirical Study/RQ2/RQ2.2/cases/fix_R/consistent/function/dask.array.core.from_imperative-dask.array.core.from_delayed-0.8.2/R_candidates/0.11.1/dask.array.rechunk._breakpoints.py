def _breakpoints(cumold, cumnew):
    """

    >>> new = cumdims_label(((2, 3), (2, 2, 1)), 'n')
    >>> old = cumdims_label(((2, 2, 1), (5,)), 'o')

    >>> _breakpoints(new[0], old[0])
    (('n', 0), ('o', 0), ('n', 2), ('o', 2), ('o', 4), ('n', 5), ('o', 5))
    >>> _breakpoints(new[1], old[1])
    (('n', 0), ('o', 0), ('n', 2), ('n', 4), ('n', 5), ('o', 5))
    """
    return tuple(sorted(tuple(cumold) + tuple(cumnew), key=lambda x:x[1]))
