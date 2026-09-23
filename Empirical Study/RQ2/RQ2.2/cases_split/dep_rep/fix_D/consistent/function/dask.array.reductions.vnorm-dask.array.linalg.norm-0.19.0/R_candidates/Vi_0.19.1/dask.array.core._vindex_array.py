def _vindex_array(x, dict_indexes):
    """Point wise indexing with only NumPy Arrays."""

    try:
        broadcast_indexes = np.broadcast_arrays(*dict_indexes.values())
    except ValueError:
        # note: error message exactly matches numpy
        shapes_str = ' '.join(str(a.shape) for a in dict_indexes.values())
        raise IndexError('shape mismatch: indexing arrays could not be '
                         'broadcast together with shapes ' + shapes_str)
    broadcast_shape = broadcast_indexes[0].shape

    lookup = dict(zip(dict_indexes, broadcast_indexes))
    flat_indexes = [lookup[i].ravel().tolist() if i in lookup else None
                    for i in range(x.ndim)]
    flat_indexes.extend([None] * (x.ndim - len(flat_indexes)))

    flat_indexes = [
        list(index) if index is not None else index for index in flat_indexes
    ]
    bounds = [list(accumulate(add, (0,) + c)) for c in x.chunks]
    bounds2 = [
        b for i, b in zip(flat_indexes, bounds) if i is not None
    ]
    axis = _get_axis(flat_indexes)
    token = tokenize(x, flat_indexes)
    out_name = 'vindex-merge-' + token

    points = list()
    for i, idx in enumerate(zip(*[i for i in flat_indexes if i is not None])):
        block_idx = [np.searchsorted(b, ind, 'right') - 1
                     for b, ind in zip(bounds2, idx)]
        inblock_idx = [ind - bounds2[k][j]
                       for k, (ind, j) in enumerate(zip(idx, block_idx))]
        points.append((i, tuple(block_idx), tuple(inblock_idx)))

    chunks = [c for i, c in zip(flat_indexes, x.chunks) if i is None]
    chunks.insert(0, (len(points),) if points else (0,))
    chunks = tuple(chunks)

    if points:
        per_block = groupby(1, points)
        per_block = dict((k, v) for k, v in per_block.items() if v)

        other_blocks = list(product(*[list(range(len(c))) if i is None else [None]
                                    for i, c in zip(flat_indexes, x.chunks)]))

        full_slices = [
            slice(None, None) if i is None else None for i in flat_indexes
        ]

        name = 'vindex-slice-' + token
        dsk = dict((keyname(name, i, okey),
                    (_vindex_transpose,
                    (_vindex_slice, (x.name,) + interleave_none(okey, key),
                     interleave_none(full_slices, list(zip(*pluck(2, per_block[key]))))),
                     axis))
                   for i, key in enumerate(per_block)
                   for okey in other_blocks)

        dsk.update((keyname('vindex-merge-' + token, 0, okey),
                   (_vindex_merge,
                    [list(pluck(0, per_block[key])) for key in per_block],
                    [keyname(name, i, okey) for i in range(len(per_block))]))
                   for okey in other_blocks)

        result_1d = Array(
            sharedict.merge(x.dask, (out_name, dsk)), out_name, chunks, x.dtype
        )
        return result_1d.reshape(broadcast_shape + result_1d.shape[1:])

    # output has a zero dimension, just create a new zero-shape array with the
    # same dtype
    from .wrap import empty
    result_1d = empty(
        tuple(map(sum, chunks)), chunks=chunks, dtype=x.dtype, name=out_name
    )
    return result_1d.reshape(broadcast_shape + result_1d.shape[1:])
