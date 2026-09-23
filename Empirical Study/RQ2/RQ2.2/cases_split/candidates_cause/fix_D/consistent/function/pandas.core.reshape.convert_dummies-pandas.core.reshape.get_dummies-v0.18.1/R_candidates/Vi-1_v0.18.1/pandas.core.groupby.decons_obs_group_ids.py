def decons_obs_group_ids(comp_ids, obs_ids, shape, labels, xnull):
    """
    reconstruct labels from observed group ids

    Parameters
    ----------
    xnull: boolean,
        if nulls are excluded; i.e. -1 labels are passed through
    """
    from pandas.hashtable import unique_label_indices

    if not xnull:
        lift = np.fromiter(((a == -1).any() for a in labels), dtype='i8')
        shape = np.asarray(shape, dtype='i8') + lift

    if not _int64_overflow_possible(shape):
        # obs ids are deconstructable! take the fast route!
        out = decons_group_index(obs_ids, shape)
        return out if xnull or not lift.any() \
            else [x - y for x, y in zip(out, lift)]

    i = unique_label_indices(comp_ids)
    i8copy = lambda a: a.astype('i8', subok=False, copy=True)
    return [i8copy(lab[i]) for lab in labels]
