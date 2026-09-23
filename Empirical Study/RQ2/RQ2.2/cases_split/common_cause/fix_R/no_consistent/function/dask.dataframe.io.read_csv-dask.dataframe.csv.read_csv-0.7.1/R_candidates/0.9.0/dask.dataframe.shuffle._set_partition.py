def _set_partition(df, index, divisions, p, drop=True):
    """ Shard partition and dump into partd """
    df = df.set_index(index, drop=drop)
    df = strip_categories(df)
    divisions = list(divisions)
    shards = shard_df_on_index(df, divisions[1:-1])
    p.append(dict(enumerate(shards)))
