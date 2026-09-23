def join_indexed_dataframes(lhs, rhs, how='left', lsuffix='', rsuffix=''):
    """ Join two partitiond dataframes along their index """
    (lhs, rhs), divisions, parts = align_partitions(lhs, rhs)
    divisions, parts = require(divisions, parts, required[how])

    left_empty = lhs._meta_nonempty
    right_empty = rhs._meta_nonempty

    name = 'join-indexed-' + tokenize(lhs, rhs, how, lsuffix, rsuffix)

    dsk = dict()
    for i, (a, b) in enumerate(parts):
        if a is None and how in ('right', 'outer'):
            a = left_empty
        if b is None and how in ('left', 'outer'):
            b = right_empty

        dsk[(name, i)] = (pd.DataFrame.join, a, b, None, how,
                          lsuffix, rsuffix)

    # dummy result
    meta = left_empty.join(right_empty, on=None, how=how,
                           lsuffix=lsuffix, rsuffix=rsuffix)
    return DataFrame(toolz.merge(lhs.dask, rhs.dask, dsk),
                     name, meta, divisions)
