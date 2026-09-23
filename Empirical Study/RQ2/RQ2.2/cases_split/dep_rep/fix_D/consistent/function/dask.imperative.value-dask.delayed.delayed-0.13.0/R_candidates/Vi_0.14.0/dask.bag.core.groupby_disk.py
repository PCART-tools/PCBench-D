def groupby_disk(b, grouper, npartitions=None, blocksize=2**20):
    if npartitions is None:
        npartitions = b.npartitions
    token = tokenize(b, grouper, npartitions, blocksize)

    import partd
    p = ('partd-' + token,)
    try:
        dsk1 = {p: (partd.Python, (partd.Snappy, (partd.File,)))}
    except AttributeError:
        dsk1 = {p: (partd.Python, (partd.File,))}

    # Partition data on disk
    name = 'groupby-part-{0}-{1}'.format(funcname(grouper), token)
    dsk2 = dict(((name, i), (partition, grouper, (b.name, i),
                             npartitions, p, blocksize))
                for i in range(b.npartitions))

    # Barrier
    barrier_token = 'groupby-barrier-' + token

    def barrier(args):
        return 0

    dsk3 = {barrier_token: (barrier, list(dsk2))}

    # Collect groups
    name = 'groupby-collect-' + token
    dsk4 = dict(((name, i),
                 (collect, grouper, i, p, barrier_token))
                for i in range(npartitions))

    return type(b)(merge(b.dask, dsk1, dsk2, dsk3, dsk4), name, npartitions)
