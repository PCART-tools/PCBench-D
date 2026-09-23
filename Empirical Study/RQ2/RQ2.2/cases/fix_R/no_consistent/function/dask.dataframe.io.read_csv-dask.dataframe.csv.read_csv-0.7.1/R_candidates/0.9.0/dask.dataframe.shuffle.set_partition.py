def set_partition(df, index, divisions, compute=False, drop=True, **kwargs):
    """ Group DataFrame by index

    Sets a new index and partitions data along that index according to
    divisions.  Divisions are often found by computing approximate quantiles.
    The function ``set_index`` will do both of these steps.

    Parameters
    ----------
    df: DataFrame/Series
        Data that we want to re-partition
    index: string or Series
        Column to become the new index
    divisions: list
        Values to form new divisions between partitions
    drop: bool, default True
        Whether to delete columns to be used as the new index

    See Also
    --------
    set_index
    shuffle
    partd
    """
    if isinstance(index, Series):
        assert df.divisions == index.divisions
        metadata = df._pd.set_index(index._pd, drop=drop)
    elif np.isscalar(index):
        metadata = df._pd.set_index(index, drop=drop)
    else:
         raise ValueError('index must be Series or scalar, {0} given'.format(type(index)))

    token = tokenize(df, index, divisions)
    always_new_token = uuid.uuid1().hex
    import partd

    p = ('zpartd-' + always_new_token,)

    # Get Categories
    catname = 'set-partition--get-categories-old-' + always_new_token
    catname2 = 'set-partition--get-categories-new-' + always_new_token

    dsk1 = {catname: (get_categories, df._keys()[0]),
            p: (partd.PandasBlocks, (partd.Buffer, (partd.Dict,), (partd.File,))),
            catname2: (new_categories, catname,
                       index.name if isinstance(index, Series) else index)}

    # Partition data on disk
    name = 'set-partition--partition-' + always_new_token
    if isinstance(index, _Frame):
        dsk2 = dict(((name, i),
                     (_set_partition, part, ind, divisions, p, drop))
                     for i, (part, ind)
                     in enumerate(zip(df._keys(), index._keys())))
    else:
        dsk2 = dict(((name, i),
                     (_set_partition, part, index, divisions, p, drop))
                     for i, part
                     in enumerate(df._keys()))

    # Barrier
    barrier_token = 'barrier-' + always_new_token
    dsk3 = {barrier_token: (barrier, list(dsk2))}

    if compute:
        dsk = merge(df.dask, dsk1, dsk2, dsk3)
        if isinstance(index, _Frame):
            dsk.update(index.dask)
        p, barrier_token, categories = df._get(dsk, [p, barrier_token, catname], **kwargs)
        dsk4 = {catname2: categories}
    else:
        dsk4 = {}

    # Collect groups
    name = 'set-partition--collect-' + token
    if compute and not categories:
        dsk4.update(dict(((name, i),
                     (_set_collect, i, p, barrier_token, df.columns))
                     for i in range(len(divisions) - 1)))
    else:
        dsk4.update(dict(((name, i),
                     (_categorize, catname2,
                        (_set_collect, i, p, barrier_token, df.columns)))
                    for i in range(len(divisions) - 1)))

    dsk = merge(df.dask, dsk1, dsk2, dsk3, dsk4)

    if isinstance(index, Series):
        dsk.update(index.dask)

    if compute:
        dsk, _ = cull(dsk, list(dsk4.keys()))

    return DataFrame(dsk, name, metadata, divisions)
