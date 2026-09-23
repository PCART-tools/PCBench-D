def rearrange_by_column_disk(df, column, npartitions=None, compute=False):
    """ Shuffle using local disk """
    if npartitions is None:
        npartitions = df.npartitions

    token = tokenize(df, column, npartitions)
    always_new_token = uuid.uuid1().hex

    import partd
    p = ('zpartd-' + always_new_token,)
    dsk1 = {p: (partd.PandasBlocks, (partd.Buffer, (partd.Dict,),
                                                   (partd.File,)))}

    # Partition data on disk
    name = 'shuffle-partition-' + always_new_token
    dsk2 = {(name, i): (shuffle_group_3, key, column, npartitions, p)
            for i, key in enumerate(df._keys())}

    dsk = merge(df.dask, dsk1, dsk2)
    if compute:
        keys = [p, sorted(dsk2)]
        pp, values = (_globals.get('get') or DataFrame._get)(dsk, keys)
        dsk1 = {p: pp}
        dsk = dict(zip(sorted(dsk2), values))

    # Barrier
    barrier_token = 'barrier-' + always_new_token
    dsk3 = {barrier_token: (barrier, list(dsk2))}

    # Collect groups
    name = 'shuffle-collect-' + token
    dsk4 = {(name, i): (collect, p, i, df._meta, barrier_token)
                for i in range(npartitions)}

    divisions = (None,) * (npartitions + 1)

    dsk = merge(dsk, dsk1, dsk3, dsk4)

    return DataFrame(dsk, name, df._meta, divisions)
