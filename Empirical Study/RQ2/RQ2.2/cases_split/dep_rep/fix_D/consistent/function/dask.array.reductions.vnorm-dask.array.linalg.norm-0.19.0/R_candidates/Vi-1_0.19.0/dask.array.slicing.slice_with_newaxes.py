def slice_with_newaxes(out_name, in_name, blockdims, index):
    """
    Handle indexing with Nones

    Strips out Nones then hands off to slice_wrap_lists
    """
    # Strip Nones from index
    index2 = tuple([ind for ind in index if ind is not None])
    where_none = [i for i, ind in enumerate(index) if ind is None]
    where_none_orig = list(where_none)
    for i, x in enumerate(where_none):
        n = sum(isinstance(ind, int) for ind in index[:x])
        if n:
            where_none[i] -= n

    # Pass down and do work
    dsk, blockdims2 = slice_wrap_lists(out_name, in_name, blockdims, index2)

    if where_none:
        expand = expander(where_none)
        expand_orig = expander(where_none_orig)

        # Insert ",0" into the key:  ('x', 2, 3) -> ('x', 0, 2, 0, 3)
        dsk2 = {(out_name,) + expand(k[1:], 0):
                (v[:2] + (expand_orig(v[2], None),))
                for k, v in dsk.items()
                if k[0] == out_name}

        # Add back intermediate parts of the dask that weren't the output
        dsk3 = merge(dsk2, {k: v for k, v in dsk.items() if k[0] != out_name})

        # Insert (1,) into blockdims:  ((2, 2), (3, 3)) -> ((2, 2), (1,), (3, 3))
        blockdims3 = expand(blockdims2, (1,))

        return dsk3, blockdims3

    else:
        return dsk, blockdims2
