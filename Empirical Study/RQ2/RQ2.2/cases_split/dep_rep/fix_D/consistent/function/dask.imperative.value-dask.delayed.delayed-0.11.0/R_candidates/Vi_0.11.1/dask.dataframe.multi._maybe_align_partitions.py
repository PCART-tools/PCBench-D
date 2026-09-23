def _maybe_align_partitions(args):
    """Align DataFrame blocks if divisions are different.

    Note that if all divisions are unknown, but have equal npartitions, then
    they will be passed through unchanged. This is different than
    `align_partitions`, which will fail if divisions aren't all known"""
    dfs = [df for df in args if isinstance(df, _Frame)]
    if not dfs:
        return args

    divisions = dfs[0].divisions
    if not all(df.divisions == divisions for df in dfs):
        dfs2 = iter(align_partitions(*dfs)[0])
        return [a if not isinstance(a, _Frame) else next(dfs2) for a in args]
    return args
