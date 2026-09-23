def _indexer_from_factorized(labels, shape, compress=True):
    ids = get_group_index(labels, shape, sort=True, xnull=False)

    if not compress:
        ngroups = (ids.size and ids.max()) + 1
    else:
        ids, obs = _compress_group_index(ids, sort=True)
        ngroups = len(obs)

    return _get_group_index_sorter(ids, ngroups)
