def _vindex(x, *indexes):
    """ Point wise slicing

    This is equivalent to numpy slicing with multiple input lists

    >>> x = np.arange(56).reshape((7, 8))
    >>> x
    array([[ 0,  1,  2,  3,  4,  5,  6,  7],
           [ 8,  9, 10, 11, 12, 13, 14, 15],
           [16, 17, 18, 19, 20, 21, 22, 23],
           [24, 25, 26, 27, 28, 29, 30, 31],
           [32, 33, 34, 35, 36, 37, 38, 39],
           [40, 41, 42, 43, 44, 45, 46, 47],
           [48, 49, 50, 51, 52, 53, 54, 55]])

    >>> d = from_array(x, chunks=(3, 4))
    >>> result = _vindex(d, [0, 1, 6, 0], [0, 1, 0, 7])
    >>> result.compute()
    array([ 0,  9, 48,  7])
    """
    indexes = [list(index) if index is not None else index for index in indexes]
    bounds = [list(accumulate(add, (0,) + c)) for c in x.chunks]
    bounds2 = [b for i, b in zip(indexes, bounds) if i is not None]
    axis = _get_axis(indexes)

    points = list()
    for i, idx in enumerate(zip(*[i for i in indexes if i is not None])):
        block_idx = [np.searchsorted(b, ind, 'right') - 1
                     for b, ind in zip(bounds2, idx)]
        inblock_idx = [ind - bounds2[k][j]
                       for k, (ind, j) in enumerate(zip(idx, block_idx))]
        points.append((i, tuple(block_idx), tuple(inblock_idx)))

    per_block = groupby(1, points)
    per_block = dict((k, v) for k, v in per_block.items() if v)

    other_blocks = list(product(*[list(range(len(c))) if i is None else [None]
                                  for i, c in zip(indexes, x.chunks)]))

    token = tokenize(x, indexes)
    name = 'vindex-slice-' + token

    full_slices = [slice(None, None) if i is None else None for i in indexes]

    dsk = dict((keyname(name, i, okey),
                (_vindex_transpose,
                 (_vindex_slice, (x.name,) + interleave_none(okey, key),
                  interleave_none(full_slices, list(zip(*pluck(2, per_block[key]))))),
                 axis))
               for i, key in enumerate(per_block)
               for okey in other_blocks)

    if per_block:
        dsk2 = dict((keyname('vindex-merge-' + token, 0, okey),
                     (_vindex_merge,
                      [list(pluck(0, per_block[key])) for key in per_block],
                      [keyname(name, i, okey) for i in range(len(per_block))]))
                    for okey in other_blocks)
    else:
        dsk2 = dict()

    chunks = [c for i, c in zip(indexes, x.chunks) if i is None]
    chunks.insert(0, (len(points),) if points else ())
    chunks = tuple(chunks)

    name = 'vindex-merge-' + token
    dsk.update(dsk2)

    return Array(sharedict.merge(x.dask, (name, dsk)), name, chunks, x.dtype)
