def common_blockdim(blockdims):
    """ Find the common block dimensions from the list of block dimensions

    Currently only implements the simplest possible heuristic: the common
    block-dimension is the only one that does not span fully span a dimension.
    This is a conservative choice that allows us to avoid potentially very
    expensive rechunking.

    Assumes that each element of the input block dimensions has all the same
    sum (i.e., that they correspond to dimensions of the same size).

    Examples
    --------

    >>> common_blockdim([(3,), (2, 1)])
    set([(2, 1)])
    >>> common_blockdim([(2, 2), (3, 1)])  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    ValueError: Chunks do not align
    """
    non_trivial_dims = set([d for d in blockdims if len(d) > 1])
    if len(non_trivial_dims) > 1:
        raise ValueError('Chunks do not align %s' % non_trivial_dims)
    elif non_trivial_dims:
        return non_trivial_dims
    else:
        return blockdims
