def take(outname, inname, chunks, index, axis=0):
    """ Index array with an iterable of index

    Handles a single index by a single list

    Mimics ``np.take``

    >>> chunks, dsk = take('y', 'x', [(20, 20, 20, 20)], [5, 1, 47, 3], axis=0)
    >>> chunks
    ((2, 1, 1),)
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, (np.concatenate, [(getitem, ('x', 0), ([1, 3, 5],)),
                                           (getitem, ('x', 2), ([7],))],
                                          0),
                         (2, 0, 4, 1))}

    When list is sorted we retain original block structure

    >>> chunks, dsk = take('y', 'x', [(20, 20, 20, 20)], [1, 3, 5, 47], axis=0)
    >>> chunks
    ((3, 1),)
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, ('x', 0), ([1, 3, 5],)),
     ('y', 2): (getitem, ('x', 2), ([7],))}
    """
    plan = slicing_plan(chunks[axis], index)
    if len(plan) >= len(chunks[axis]) * 10:
        factor = math.ceil(len(plan) / len(chunks[axis]))
        from .core import PerformanceWarning
        warnings.warn("Slicing with an out-of-order index is generating %d "
                      "times more chunks" % factor, PerformanceWarning,
                      stacklevel=6)

    index_lists = [idx for _, idx in plan]
    where_index = [i for i, _ in plan]

    dims = [range(len(bd)) for bd in chunks]

    indims = list(dims)
    indims[axis] = list(range(len(where_index)))
    keys = list(product([outname], *indims))

    outdims = list(dims)
    outdims[axis] = where_index
    slices = [[colon] * len(bd) for bd in chunks]
    slices[axis] = index_lists
    slices = list(product(*slices))
    inkeys = list(product([inname], *outdims))
    values = [(getitem, inkey, slc) for inkey, slc in zip(inkeys, slices)]

    chunks2 = list(chunks)
    chunks2[axis] = tuple(map(len, index_lists))
    dsk = dict(zip(keys, values))
    return tuple(chunks2), dsk
