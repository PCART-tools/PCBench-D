def partitioning_index(df, npartitions):
    """Computes a deterministic index mapping each record to a partition.

    Identical rows are mapped to the same partition.

    Parameters
    ----------
    df : DataFrame/Series/Index
    npartitions : int
        The number of partitions to group into.

    Returns
    -------
    partitions : ndarray
        An array of int64 values mapping each record to a partition.
    """
    if isinstance(df, (pd.Series, pd.Index)):
        h = hash_series(df).astype('int64')
    elif isinstance(df, pd.DataFrame):
        cols = df.iteritems()
        h = hash_series(next(cols)[1]).astype('int64')
        for _, col in cols:
            h = np.multiply(h, 3, h)
            h = np.add(h, hash_series(col), h)
    else:
        raise TypeError("Unexpected type %s" % type(df))
    return h % int(npartitions)
