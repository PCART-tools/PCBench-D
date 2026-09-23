def _compute_rechunk(x, chunks):
    """ Compute the rechunk of *x* to the given *chunks*.
    """
    ndim = x.ndim
    crossed = intersect_chunks(x.chunks, chunks)
    x2 = dict()
    intermediates = dict()
    token = tokenize(x, chunks)
    merge_temp_name = 'rechunk-merge-' + token
    split_temp_name = 'rechunk-split-' + token
    split_name_suffixes = count()

    # Pre-allocate old block references, to allow re-use and reduce the
    # graph's memory footprint a bit.
    old_blocks = np.empty([len(c) for c in x.chunks], dtype='O')
    for index in np.ndindex(old_blocks.shape):
        old_blocks[index] = (x.name,) + index

    # Iterate over all new blocks
    new_index = product(*(range(len(c)) for c in chunks))

    for new_idx, cross1 in zip(new_index, crossed):
        key = (merge_temp_name,) + new_idx
        old_block_indices = [[cr[i][0] for cr in cross1] for i in range(ndim)]
        subdims1 = [len(set(old_block_indices[i]))
                    for i in range(ndim)]

        rec_cat_arg = np.empty(subdims1, dtype='O')
        rec_cat_arg_flat = rec_cat_arg.flat

        # Iterate over the old blocks required to build the new block
        for rec_cat_index, ind_slices in enumerate(cross1):
            old_block_index, slices = zip(*ind_slices)
            name = (split_temp_name, next(split_name_suffixes))
            intermediates[name] = (getitem, old_blocks[old_block_index], slices)
            rec_cat_arg_flat[rec_cat_index] = name

        assert rec_cat_index == rec_cat_arg.size - 1
        # New block is formed by concatenation of sliced old blocks
        x2[key] = (concatenate3, rec_cat_arg.tolist())

    assert new_idx == tuple(len(c) - 1 for c in chunks)
    del old_blocks, new_index

    x2 = merge(x.dask, x2, intermediates)
    return Array(x2, merge_temp_name, chunks, dtype=x.dtype)
