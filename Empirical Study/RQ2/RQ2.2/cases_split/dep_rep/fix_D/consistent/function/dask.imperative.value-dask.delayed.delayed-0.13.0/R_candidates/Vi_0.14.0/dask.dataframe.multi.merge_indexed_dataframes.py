def merge_indexed_dataframes(lhs, rhs, how='left', lsuffix='', rsuffix='',
                             indicator=False):
    """ Join two partitioned dataframes along their index """

    (lhs, rhs), divisions, parts = align_partitions(lhs, rhs)
    divisions, parts = require(divisions, parts, required[how])

    left_empty = lhs._meta
    right_empty = rhs._meta

    name = 'join-indexed-' + tokenize(lhs, rhs, how, lsuffix, rsuffix,
                                      indicator)

    dsk = dict()
    for i, (a, b) in enumerate(parts):
        if a is None and how in ('right', 'outer'):
            a = left_empty
        if b is None and how in ('left', 'outer'):
            b = right_empty

        dsk[(name, i)] = (methods.merge, a, b, how, None, None, True, True,
                          indicator, (lsuffix, rsuffix), left_empty,
                          right_empty)

    meta = pd.merge(lhs._meta_nonempty, rhs._meta_nonempty, how=how,
                    left_index=True, right_index=True,
                    suffixes=(lsuffix, rsuffix), indicator=indicator)
    return new_dd_object(toolz.merge(lhs.dask, rhs.dask, dsk),
                         name, meta, divisions)
