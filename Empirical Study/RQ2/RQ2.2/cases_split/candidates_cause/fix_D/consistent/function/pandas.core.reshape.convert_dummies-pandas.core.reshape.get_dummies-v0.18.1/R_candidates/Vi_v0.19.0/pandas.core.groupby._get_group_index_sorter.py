def _get_group_index_sorter(group_index, ngroups):
    """
    _algos.groupsort_indexer implements `counting sort` and it is at least
    O(ngroups), where
        ngroups = prod(shape)
        shape = map(len, keys)
    that is, linear in the number of combinations (cartesian product) of unique
    values of groupby keys. This can be huge when doing multi-key groupby.
    np.argsort(kind='mergesort') is O(count x log(count)) where count is the
    length of the data-frame;
    Both algorithms are `stable` sort and that is necessary for correctness of
    groupby operations. e.g. consider:
        df.groupby(key)[col].transform('first')
    """
    count = len(group_index)
    alpha = 0.0  # taking complexities literally; there may be
    beta = 1.0  # some room for fine-tuning these parameters
    do_groupsort = (count > 0 and ((alpha + beta * ngroups) <
                                   (count * np.log(count))))
    if do_groupsort:
        sorter, _ = _algos.groupsort_indexer(_ensure_int64(group_index),
                                             ngroups)
        return _ensure_platform_int(sorter)
    else:
        return group_index.argsort(kind='mergesort')
