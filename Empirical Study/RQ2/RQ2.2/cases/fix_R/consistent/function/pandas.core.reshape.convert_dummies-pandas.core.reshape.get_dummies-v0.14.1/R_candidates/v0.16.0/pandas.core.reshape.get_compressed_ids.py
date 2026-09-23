def get_compressed_ids(labels, sizes):
    from pandas.core.groupby import get_group_index

    ids = get_group_index(labels, sizes, sort=True, xnull=False)
    return _compress_group_index(ids, sort=True)
