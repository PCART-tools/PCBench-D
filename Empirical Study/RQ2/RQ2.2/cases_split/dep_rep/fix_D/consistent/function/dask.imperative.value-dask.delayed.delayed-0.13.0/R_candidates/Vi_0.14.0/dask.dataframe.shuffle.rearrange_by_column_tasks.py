def rearrange_by_column_tasks(df, column, max_branch=32, npartitions=None):
    """ Order divisions of DataFrame so that all values within column align

    This enacts a task-based shuffle

    See also:
        rearrange_by_column_disk
        set_partitions_tasks
        shuffle_tasks
    """
    max_branch = max_branch or 32
    n = df.npartitions

    stages = int(math.ceil(math.log(n) / math.log(max_branch)))
    if stages > 1:
        k = int(math.ceil(n ** (1 / stages)))
    else:
        k = n

    groups = []
    splits = []
    joins = []

    inputs = [tuple(digit(i, j, k) for j in range(stages))
              for i in range(k**stages)]

    token = tokenize(df, column, max_branch)

    start = dict((('shuffle-join-' + token, 0, inp),
                  (df._name, i) if i < df.npartitions else df._meta)
                 for i, inp in enumerate(inputs))

    for stage in range(1, stages + 1):
        group = dict((('shuffle-group-' + token, stage, inp),
                      (shuffle_group, ('shuffle-join-' + token, stage - 1, inp),
                       column, stage - 1, k, n))
                     for inp in inputs)

        split = dict((('shuffle-split-' + token, stage, i, inp),
                      (getitem, ('shuffle-group-' + token, stage, inp), i))
                     for i in range(k)
                     for inp in inputs)

        join = dict((('shuffle-join-' + token, stage, inp),
                     (_concat,
                      [('shuffle-split-' + token, stage, inp[stage - 1],
                       insert(inp, stage - 1, j)) for j in range(k)]))
                    for inp in inputs)
        groups.append(group)
        splits.append(split)
        joins.append(join)

    end = dict((('shuffle-' + token, i),
                ('shuffle-join-' + token, stages, inp))
               for i, inp in enumerate(inputs))

    dsk = merge(df.dask, start, end, *(groups + splits + joins))
    df2 = DataFrame(dsk, 'shuffle-' + token, df, df.divisions)

    if npartitions is not None and npartitions != df.npartitions:
        parts = [i % df.npartitions for i in range(npartitions)]
        token = tokenize(df2, npartitions)
        dsk = {('repartition-group-' + token, i): (shuffle_group_2, k, column)
               for i, k in enumerate(df2._keys())}
        for p in range(npartitions):
            dsk[('repartition-get-' + token, p)] = \
                (shuffle_group_get, ('repartition-group-' + token, parts[p]), p)

        df3 = DataFrame(merge(df2.dask, dsk), 'repartition-get-' + token, df2,
                        [None] * (npartitions + 1))
    else:
        df3 = df2
        df3.divisions = (None,) * (df.npartitions + 1)

    return df3
