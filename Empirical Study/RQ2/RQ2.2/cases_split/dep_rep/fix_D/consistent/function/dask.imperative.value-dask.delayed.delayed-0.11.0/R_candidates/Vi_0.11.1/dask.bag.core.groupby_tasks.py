def groupby_tasks(b, grouper, hash=hash, max_branch=32):
    max_branch = max_branch or 32
    n = b.npartitions

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

    b2 = b.map(lambda x: (hash(grouper(x)), x))

    token = tokenize(b, grouper, hash, max_branch)

    start = dict((('shuffle-join-' + token, 0, inp),
                  (b2.name, i) if i < b.npartitions else [])
                 for i, inp in enumerate(inputs))

    for stage in range(1, stages + 1):
        group = dict((('shuffle-group-' + token, stage, inp),
                      (groupby,
                        (make_group, k, stage - 1),
                        ('shuffle-join-' + token, stage - 1, inp)))
                 for inp in inputs)

        split = dict((('shuffle-split-' + token, stage, i, inp),
                      (dict.get, ('shuffle-group-' + token, stage, inp), i, {}))
                     for i in range(k)
                     for inp in inputs)

        join = dict((('shuffle-join-' + token, stage, inp),
                     (list, (toolz.concat,
                        [('shuffle-split-' + token, stage, inp[stage - 1],
                          insert(inp, stage - 1, j)) for j in range(k)])))
                     for inp in inputs)
        groups.append(group)
        splits.append(split)
        joins.append(join)

    end = dict((('shuffle-' + token, i),
                (list, (dict.items, (groupby, grouper, (pluck, 1, j)))))
               for i, j in enumerate(join))

    dsk = merge(b2.dask, start, end, *(groups + splits + joins))

    return type(b)(dsk, 'shuffle-' + token, len(inputs))
