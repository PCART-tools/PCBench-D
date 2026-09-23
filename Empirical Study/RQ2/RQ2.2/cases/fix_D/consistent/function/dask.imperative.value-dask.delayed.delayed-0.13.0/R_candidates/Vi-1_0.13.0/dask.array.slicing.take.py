def take(outname, inname, blockdims, index, axis=0):
    """ Index array with an iterable of index

    Handles a single index by a single list

    Mimics ``np.take``

    >>> blockdims, dsk = take('y', 'x', [(20, 20, 20, 20)], [5, 1, 47, 3], axis=0)
    >>> blockdims
    ((4,),)
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, (np.concatenate, [(getitem, ('x', 0), ([1, 3, 5],)),
                                           (getitem, ('x', 2), ([7],))],
                                          0),
                         (2, 0, 4, 1))}

    When list is sorted we retain original block structure

    >>> blockdims, dsk = take('y', 'x', [(20, 20, 20, 20)], [1, 3, 5, 47], axis=0)
    >>> blockdims
    ((3, 1),)
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, ('x', 0), ([1, 3, 5],)),
     ('y', 2): (getitem, ('x', 2), ([7],))}
    """
    if issorted(index):
        return take_sorted(outname, inname, blockdims, index, axis)

    n = len(blockdims)
    sizes = blockdims[axis]  # the blocksizes on the axis that we care about

    index_lists = partition_by_size(sizes, sorted(index))

    dims = [[0] if axis == i else list(range(len(bd)))
            for i, bd in enumerate(blockdims)]
    keys = list(product([outname], *dims))

    rev_index = list(map(sorted(index).index, index))
    vals = [(getitem, (np.concatenate,
                       [(getitem, ((inname, ) + d[:axis] + (i, ) + d[axis + 1:]),
                         ((colon, ) * axis + (IL, ) + (colon, ) * (n - axis - 1)))
                        for i, IL in enumerate(index_lists) if IL], axis),
             ((colon, ) * axis + (rev_index, ) + (colon, ) * (n - axis - 1)))
            for d in product(*dims)]

    blockdims2 = list(blockdims)
    blockdims2[axis] = (len(index), )

    return tuple(blockdims2), dict(zip(keys, vals))
