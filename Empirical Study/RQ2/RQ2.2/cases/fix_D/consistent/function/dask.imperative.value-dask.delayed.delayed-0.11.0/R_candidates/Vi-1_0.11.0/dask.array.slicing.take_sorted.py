def take_sorted(outname, inname, blockdims, index, axis=0):
    """ Index array with sorted list index

    Forms a dask for the following case

        x[:, [1, 3, 5, 10], ...]

    where the index, ``[1, 3, 5, 10]`` is sorted in non-decreasing order.

    >>> blockdims, dsk = take('y', 'x', [(20, 20, 20, 20)], [1, 3, 5, 47], axis=0)
    >>> blockdims
    ((3, 1),)
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, ('x', 0), ([1, 3, 5],)),
     ('y', 1): (getitem, ('x', 2), ([7],))}

    See Also
    --------
    take - calls this function
    """
    sizes = blockdims[axis]  # the blocksizes on the axis that we care about

    index_lists = partition_by_size(sizes, sorted(index))
    where_index = [i for i, il in enumerate(index_lists) if il]
    index_lists = [il for il in index_lists if il]

    dims = [range(len(bd)) for bd in blockdims]

    indims = list(dims)
    indims[axis] = list(range(len(where_index)))
    keys = list(product([outname], *indims))

    outdims = list(dims)
    outdims[axis] = where_index
    slices = [[colon]*len(bd) for bd in blockdims]
    slices[axis] = index_lists
    slices = list(product(*slices))
    inkeys = list(product([inname], *outdims))
    values = [(getitem, inkey, slc) for inkey, slc in zip(inkeys, slices)]

    blockdims2 = list(blockdims)
    blockdims2[axis] = tuple(map(len, index_lists))

    return tuple(blockdims2), dict(zip(keys, values))
