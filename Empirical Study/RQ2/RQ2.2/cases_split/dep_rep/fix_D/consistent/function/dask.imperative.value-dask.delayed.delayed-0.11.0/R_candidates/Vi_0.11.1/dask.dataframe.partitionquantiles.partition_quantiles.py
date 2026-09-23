def partition_quantiles(df, npartitions, upsample=1.0, random_state=None):
    """ Approximate quantiles of Series used for repartitioning
    """
    assert isinstance(df, Series)
    # currently, only Series has quantile method
    # Index.quantile(list-like) must be pd.Series, not pd.Index
    return_type = Series

    qs = np.linspace(0, 1, npartitions + 1)
    token = tokenize(df, qs, upsample)
    if random_state is None:
        random_state = hash(token) % np.iinfo(np.int32).max
    seeds = different_seeds(df.npartitions, random_state)

    df_keys = df._keys()

    name0 = 're-quantiles-0-' + token
    dtype_dsk = {(name0, 0): (dtype_info, df_keys[0])}

    name1 = 're-quantiles-1-' + token
    val_dsk = dict(((name1, i), (percentiles_summary, key, df.npartitions,
                                 npartitions, upsample, seeds[i]))
                   for i, key in enumerate(df_keys))

    name2 = 're-quantiles-2-' + token
    merge_dsk = create_merge_tree(merge_and_compress_summaries, sorted(val_dsk), name2)
    if not merge_dsk:
        # Compress the data even if we only have one partition
        merge_dsk = {(name2, 0, 0): (merge_and_compress_summaries, [list(val_dsk)[0]])}

    merged_key = max(merge_dsk)

    name3 = 're-quantiles-3-' + token
    last_dsk = {(name3, 0): (pd.Series, (process_val_weights, merged_key,
                                         npartitions, (name0, 0)), qs, None, df.name)}

    dsk = merge(df.dask, dtype_dsk, val_dsk, merge_dsk, last_dsk)
    new_divisions = [0.0, 1.0]
    return return_type(dsk, name3, df._meta, new_divisions)
