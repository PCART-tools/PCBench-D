def expand_key(k, dims, name=None, axes=None):
    """ Get all neighboring keys around center

    Parameters
    ----------
    k: tuple
        They key around which to generate new keys
    dims: Sequence[int]
        The number of chunks in each dimension
    name: Option[str]
        The name to include in the output keys, or none to include no name
    axes: Dict[int, int]
        The axes active in the expansion.  We don't expand on non-active axes

    Examples
    --------
    >>> expand_key(('x', 2, 3), dims=[5, 5], name='y', axes={0: 1, 1: 1})  # doctest: +NORMALIZE_WHITESPACE
    [[('y', 1.1, 2.1), ('y', 1.1, 3), ('y', 1.1, 3.9)],
     [('y',   2, 2.1), ('y',   2, 3), ('y',   2, 3.9)],
     [('y', 2.9, 2.1), ('y', 2.9, 3), ('y', 2.9, 3.9)]]

    >>> expand_key(('x', 0, 4), dims=[5, 5], name='y', axes={0: 1, 1: 1})  # doctest: +NORMALIZE_WHITESPACE
    [[('y',   0, 3.1), ('y',   0,   4)],
     [('y', 0.9, 3.1), ('y', 0.9,   4)]]
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

    args = [inds(i, ind) if axes.get(i, 0) else [ind] for i, ind in enumerate(k[1:])]
    if name is not None:
        args = [[name]] + args
    seq = list(product(*args))
    shape2 = [d if axes.get(i, 0) else 1 for i, d in enumerate(shape)]
    result = reshapelist(shape2, seq)
    return result
