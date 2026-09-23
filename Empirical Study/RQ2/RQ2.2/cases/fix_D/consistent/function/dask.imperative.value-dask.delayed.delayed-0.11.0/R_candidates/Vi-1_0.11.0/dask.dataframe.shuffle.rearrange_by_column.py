def rearrange_by_column(df, col, npartitions=None, max_branch=None,
        shuffle=None, compute=None):
    shuffle = shuffle or _globals.get('shuffle', 'disk')
    if shuffle == 'disk':
        return rearrange_by_column_disk(df, col, npartitions, compute=compute)
    elif shuffle == 'tasks':
        if npartitions is not None and npartitions < df.npartitions:
            raise ValueError("Must create as many or more partitions in shuffle")
        return rearrange_by_column_tasks(df, col, max_branch, npartitions)
    else:
        raise NotImplementedError("Unknown shuffle method %s" % shuffle)
