def set_partition(df, index, divisions, max_branch=32, drop=True, shuffle=None,
        compute=None):
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
    shuffle: str (optional)
        Either 'disk' for an on-disk shuffle or 'tasks' to use the task
        scheduling framework.  Use 'disk' if you are on a single machine
        and 'tasks' if you are on a distributed cluster.
    max_branch: int (optional)
        If using the task-based shuffle, the amount of splitting each
        partition undergoes.  Increase this for fewer copies but more
        scheduler overhead.

    See Also
    --------
    set_index
    shuffle
    partd
    """
    if np.isscalar(index):
        partitions = df[index].map_partitions(set_partitions_pre,
                divisions=divisions, meta=pd.Series([0]))
        df2 = df.assign(_partitions=partitions)
    else:
        partitions = index.map_partitions(set_partitions_pre,
                divisions=divisions, meta=pd.Series([0]))
        df2 = df.assign(_partitions=partitions, _index=index)

    df3 = rearrange_by_column(df2, '_partitions', max_branch=max_branch,
            npartitions=len(divisions) - 1, shuffle=shuffle, compute=compute)

    if np.isscalar(index):
        df4 = df3.map_partitions(set_index_post_scalar, index_name=index,
                drop=drop, column_dtype=df.columns.dtype)
    else:
        df4 = df3.map_partitions(set_index_post_series, index_name=index.name,
                drop=drop, column_dtype=df.columns.dtype)

    df4.divisions = divisions

    return df4.map_partitions(pd.DataFrame.sort_index)
