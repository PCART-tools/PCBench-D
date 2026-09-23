def shuffle_group(df, col, stage, k, npartitions):
    if col == '_partitions':
        ind = df[col].values % npartitions
    else:
        ind = partitioning_index(df[col], npartitions)
    c = ind // k ** stage % k
    g = df.groupby(c)
    return {i: g.get_group(i) if i in g.groups else df.head(0) for i in range(k)}
