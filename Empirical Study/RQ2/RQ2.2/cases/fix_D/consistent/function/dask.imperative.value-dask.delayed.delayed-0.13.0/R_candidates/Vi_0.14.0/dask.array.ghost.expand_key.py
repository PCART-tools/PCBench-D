def expand_key(k, dims):
    """ Get all neighboring keys around center

    >>> expand_key(('x', 2, 3), dims=[5, 5])  # doctest: +NORMALIZE_WHITESPACE
    [[('x', 1.1, 2.1), ('x', 1.1, 3), ('x', 1.1, 3.9)],
     [('x',   2, 2.1), ('x',   2, 3), ('x',   2, 3.9)],
     [('x', 2.9, 2.1), ('x', 2.9, 3), ('x', 2.9, 3.9)]]

    >>> expand_key(('x', 0, 4), dims=[5, 5])  # doctest: +NORMALIZE_WHITESPACE
    [[('x',   0, 3.1), ('x',   0,   4)],
     [('x', 0.9, 3.1), ('x', 0.9,   4)]]
    """
    def inds(i, ind):
        rv = []
        if ind - 0.9 > 0:
            rv.append(ind - 0.9)
        rv.append(ind)
        if ind + 0.9 < dims[i] - 1:
            rv.append(ind + 0.9)
        return rv

    shape = []
    for i, ind in enumerate(k[1:]):
        num = 1
        if ind > 0:
            num += 1
        if ind < dims[i] - 1:
            num += 1
        shape.append(num)

    seq = list(product([k[0]], *[inds(i, ind)
                                 for i, ind in enumerate(k[1:])]))
    return reshapelist(shape, seq)
