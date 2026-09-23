def single_partition_join(left, right, **kwargs):
    # if the merge is perfomed on_index, divisions can be kept, otherwise the
    # new index will not necessarily correspond the current divisions

    meta = pd.merge(left._meta_nonempty, right._meta_nonempty, **kwargs)
    name = 'merge-' + tokenize(left, right, **kwargs)
    if left.npartitions == 1:
        left_key = first(left._keys())
        dsk = dict(((name, i), (apply, pd.merge, [left_key, right_key],
                                kwargs))
                   for i, right_key in enumerate(right._keys()))

        if kwargs.get('right_index'):
            divisions = right.divisions
        else:
            divisions = [None for _ in right.divisions]

    elif right.npartitions == 1:
        right_key = first(right._keys())
        dsk = dict(((name, i), (apply, pd.merge, [left_key, right_key],
                                kwargs))
                   for i, left_key in enumerate(left._keys()))

        if kwargs.get('left_index'):
            divisions = left.divisions
        else:
            divisions = [None for _ in left.divisions]

    return new_dd_object(toolz.merge(dsk, left.dask, right.dask), name,
                         meta, divisions)
