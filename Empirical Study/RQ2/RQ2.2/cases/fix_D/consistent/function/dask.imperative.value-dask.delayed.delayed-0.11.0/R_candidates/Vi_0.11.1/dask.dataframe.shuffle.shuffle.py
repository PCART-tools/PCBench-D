def shuffle(df, index, shuffle=None, npartitions=None, max_branch=32,
            compute=None):
    """ Group DataFrame by index

    Hash grouping of elements. After this operation all elements that have
    the same index will be in the same partition. Note that this requires
    full dataset read, serialization and shuffle. This is expensive. If
    possible you should avoid shuffles.

    This does not preserve a meaningful index/partitioning scheme. This is not
    deterministic if done in parallel.

    See Also
    --------
    set_index
    set_partition
    shuffle_disk
    shuffle_tasks
    """
    if not isinstance(index, _Frame):
        index = df[index]
    partitions = index.map_partitions(partitioning_index,
                                      npartitions=npartitions or df.npartitions,
                                      meta=pd.Series([0]))
    df2 = df.assign(_partitions=partitions)
    df3 = rearrange_by_column(df2, '_partitions', npartitions=npartitions,
                              max_branch=max_branch, shuffle=shuffle,
                              compute=compute)

    df4 = df3.drop('_partitions', axis=1, dtype=df.columns.dtype)
    return df4
