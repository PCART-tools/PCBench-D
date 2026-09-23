def single_partition_join(left, right, **kwargs):
    meta = pd.merge(left._meta_nonempty, right._meta_nonempty, **kwargs)
    name = 'merge-' + tokenize(left, right, **kwargs)
    if left.npartitions == 1:
        left_key = first(left._keys())
        dsk = dict(((name, i), (apply, pd.merge, [left_key, right_key],
                                kwargs))
                   for i, right_key in enumerate(right._keys()))
        divisions = right.divisions
    elif right.npartitions == 1:
        right_key = first(right._keys())
        dsk = dict(((name, i), (apply, pd.merge, [left_key, right_key],
                                kwargs))
                   for i, left_key in enumerate(left._keys()))
        divisions = left.divisions
    return DataFrame(toolz.merge(dsk, left.dask, right.dask), name,
                     meta, divisions)
