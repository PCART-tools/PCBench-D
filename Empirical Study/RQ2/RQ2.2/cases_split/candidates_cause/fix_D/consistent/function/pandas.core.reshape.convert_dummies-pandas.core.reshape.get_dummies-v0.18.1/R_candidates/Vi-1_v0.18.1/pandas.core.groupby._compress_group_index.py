def _compress_group_index(group_index, sort=True):
    """
    Group_index is offsets into cartesian product of all possible labels. This
    space can be huge, so this function compresses it, by computing offsets
    (comp_ids) into the list of unique labels (obs_group_ids).
    """

    size_hint = min(len(group_index), _hash._SIZE_HINT_LIMIT)
    table = _hash.Int64HashTable(size_hint)

    group_index = com._ensure_int64(group_index)

    # note, group labels come out ascending (ie, 1,2,3 etc)
    comp_ids, obs_group_ids = table.get_labels_groupby(group_index)

    if sort and len(obs_group_ids) > 0:
        obs_group_ids, comp_ids = _reorder_by_uniques(obs_group_ids, comp_ids)

    return comp_ids, obs_group_ids
