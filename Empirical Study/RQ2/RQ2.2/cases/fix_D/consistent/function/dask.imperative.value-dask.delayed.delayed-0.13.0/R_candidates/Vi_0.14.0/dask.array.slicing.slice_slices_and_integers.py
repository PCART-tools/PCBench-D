def slice_slices_and_integers(out_name, in_name, blockdims, index):
    """
    Dask array indexing with slices and integers

    See Also
    --------

    _slice_1d
    """
    shape = tuple(map(sum, blockdims))

    for dim, ind in zip(shape, index):
        if np.isnan(dim) and ind != slice(None, None, None):
            raise ValueError("Arrays chunk sizes are unknown: %s", shape)

    assert all(isinstance(ind, (slice, int, long)) for ind in index)
    assert len(index) == len(blockdims)

    # Get a list (for each dimension) of dicts{blocknum: slice()}
    block_slices = list(map(_slice_1d, shape, blockdims, index))
    sorted_block_slices = [sorted(i.items()) for i in block_slices]

    # (in_name, 1, 1, 2), (in_name, 1, 1, 4), (in_name, 2, 1, 2), ...
    in_names = list(product([in_name], *[pluck(0, s) for s in sorted_block_slices]))

    # (out_name, 0, 0, 0), (out_name, 0, 0, 1), (out_name, 0, 1, 0), ...
    out_names = list(product([out_name],
                             *[range(len(d))[::-1] if i.step and i.step < 0 else range(len(d))
                               for d, i in zip(block_slices, index)
                               if not isinstance(i, (int, long))]))

    all_slices = list(product(*[pluck(1, s) for s in sorted_block_slices]))

    dsk_out = {out_name: (getitem, in_name, slices)
               for out_name, in_name, slices
               in zip(out_names, in_names, all_slices)}

    new_blockdims = [new_blockdim(d, db, i)
                     for d, i, db in zip(shape, index, blockdims)
                     if not isinstance(i, (int, long))]

    return dsk_out, new_blockdims
