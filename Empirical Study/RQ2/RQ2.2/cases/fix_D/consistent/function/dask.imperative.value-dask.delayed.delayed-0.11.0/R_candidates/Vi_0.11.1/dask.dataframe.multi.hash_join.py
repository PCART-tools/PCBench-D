def hash_join(lhs, left_on, rhs, right_on, how='inner',
              npartitions=None, suffixes=('_x', '_y'), shuffle=None,
              indicator=False):
    """ Join two DataFrames on particular columns with hash join

    This shuffles both datasets on the joined column and then performs an
    embarrassingly parallel join partition-by-partition

    >>> hash_join(a, 'id', rhs, 'id', how='left', npartitions=10)  # doctest: +SKIP
    """
    if npartitions is None:
        npartitions = max(lhs.npartitions, rhs.npartitions)

    lhs2 = shuffle_func(lhs, left_on, npartitions=npartitions, shuffle=shuffle)
    rhs2 = shuffle_func(rhs, right_on, npartitions=npartitions, shuffle=shuffle)

    if isinstance(left_on, Index):
        left_on = None
        left_index = True
    else:
        left_index = False

    if isinstance(right_on, Index):
        right_on = None
        right_index = True
    else:
        right_index = False

    # dummy result
    meta = pd.merge(lhs._meta_nonempty, rhs._meta_nonempty, how=how,
                    left_on=left_on, right_on=right_on,
                    left_index=left_index, right_index=right_index,
                    suffixes=suffixes, indicator=indicator)

    merger = partial(_pdmerge, suffixes=suffixes,
                     default_left=lhs._meta,
                     default_right=rhs._meta)

    if isinstance(left_on, list):
        left_on = (list, tuple(left_on))
    if isinstance(right_on, list):
        right_on = (list, tuple(right_on))

    token = tokenize(lhs2, left_on, rhs2, right_on, left_index, right_index,
                     how, npartitions, suffixes, shuffle, indicator)
    name = 'hash-join-' + token

    dsk = dict(((name, i), (merger, (lhs2._name, i), (rhs2._name, i),
                            how, left_on, right_on,
                            left_index, right_index, indicator))
                for i in range(npartitions))

    divisions = [None] * (npartitions + 1)
    return DataFrame(toolz.merge(lhs2.dask, rhs2.dask, dsk),
                     name, meta, divisions)
