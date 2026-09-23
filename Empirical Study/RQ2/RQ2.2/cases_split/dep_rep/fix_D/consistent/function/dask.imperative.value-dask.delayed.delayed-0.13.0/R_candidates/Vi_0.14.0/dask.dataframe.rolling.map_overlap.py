def map_overlap(func, df, before, after, *args, **kwargs):
    """Apply a function to each partition, sharing rows with adjacent partitions.

    Parameters
    ----------
    func : function
        Function applied to each partition.
    df : dd.DataFrame, dd.Series
    before : int
        The number of rows to prepend to partition ``i`` from the end of
        partition ``i - 1``.
    after : int
        The number of rows to append to partition ``i`` from the beginning
        of partition ``i + 1``.
    args, kwargs :
        Arguments and keywords to pass to the function. The partition will
        be the first argument, and these will be passed *after*.

    See Also
    --------
    dd.DataFrame.map_overlap
    """
    if not (isinstance(before, int) and before >= 0 and
            isinstance(after, int) and after >= 0):
        raise ValueError("before and after must be positive integers")

    if 'token' in kwargs:
        func_name = kwargs.pop('token')
        token = tokenize(df, before, after, *args, **kwargs)
    else:
        func_name = 'overlap-' + funcname(func)
        token = tokenize(func, df, before, after, *args, **kwargs)

    if 'meta' in kwargs:
        meta = kwargs.pop('meta')
    else:
        meta = _emulate(func, df, *args, **kwargs)
    meta = make_meta(meta)

    name = '{0}-{1}'.format(func_name, token)
    name_a = 'overlap-prepend-' + tokenize(df, before)
    name_b = 'overlap-append-' + tokenize(df, after)
    df_name = df._name

    dsk = df.dask.copy()
    if before:
        dsk.update({(name_a, i): (M.tail, (df_name, i), before)
                    for i in range(df.npartitions - 1)})
        prevs = [None] + [(name_a, i) for i in range(df.npartitions - 1)]
    else:
        prevs = [None] * df.npartitions

    if after:
        dsk.update({(name_b, i): (M.head, (df_name, i), after)
                    for i in range(1, df.npartitions)})
        nexts = [(name_b, i) for i in range(1, df.npartitions)] + [None]
    else:
        nexts = [None] * df.npartitions

    for i, (prev, current, next) in enumerate(zip(prevs, df._keys(), nexts)):
        dsk[(name, i)] = (overlap_chunk, func, prev, current, next, before,
                          after, args, kwargs)

    return df._constructor(dsk, name, meta, df.divisions)
