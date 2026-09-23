def slice_with_newaxes(out_name, in_name, blockdims, index):
    """
    Handle indexing with Nones

    Strips out Nones then hands off to slice_wrap_lists
    """
    # Strip Nones from index
    index2 = tuple([ind for ind in index if ind is not None])
    where_none = [i for i, ind in enumerate(index) if ind is None]

    # Pass down and do work
    dsk, blockdims2 = slice_wrap_lists(out_name, in_name, blockdims, index2)

    # Insert ",0" into the key:  ('x', 2, 3) -> ('x', 0, 2, 0, 3)
    dsk2 = dict(((out_name,) + insert_many(k[1:], where_none, 0),
                 (v[:2] + (insert_many(v[2], where_none, None),)))
                for k, v in dsk.items()
                if k[0] == out_name)

    # Add back intermediate parts of the dask that weren't the output
    dsk3 = merge(dsk2, dict((k, v) for k, v in dsk.items() if k[0] != out_name))

    # Insert (1,) into blockdims:  ((2, 2), (3, 3)) -> ((2, 2), (1,), (3, 3))
    blockdims3 = insert_many(blockdims2, where_none, (1,))

    return dsk3, blockdims3
