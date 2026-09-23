def _maybe_align_partitions(args):
    """ Align DataFrame blocks if divisions are different """
    # passed to align_partitions
    indexer, dasks = zip(*[x for x in enumerate(args)
                           if isinstance(x[1], (_Frame, Scalar))])

    # to get current divisions
    dfs = [df for df in dasks if isinstance(df, _Frame)]
    if len(dfs) == 0:
        # no need to align
        return args

    divisions = dfs[0].divisions
    if not all(df.divisions == divisions for df in dfs):
        dasks, _, _ = align_partitions(*dasks)
        for i, d in zip(indexer, dasks):
            args[i] = d
    return args
