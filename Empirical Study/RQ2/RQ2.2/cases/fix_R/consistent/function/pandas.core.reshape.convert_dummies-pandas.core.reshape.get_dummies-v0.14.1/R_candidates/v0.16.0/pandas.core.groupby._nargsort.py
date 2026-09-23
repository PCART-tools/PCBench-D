def _nargsort(items, kind='quicksort', ascending=True, na_position='last'):
    """
    This is intended to be a drop-in replacement for np.argsort which handles NaNs
    It adds ascending and na_position parameters.
    GH #6399, #5231
    """

    # specially handle Categorical
    if is_categorical_dtype(items):
        return items.argsort(ascending=ascending)

    items = np.asanyarray(items)
    idx = np.arange(len(items))
    mask = isnull(items)
    non_nans = items[~mask]
    non_nan_idx = idx[~mask]
    nan_idx = np.nonzero(mask)[0]
    if not ascending:
        non_nans = non_nans[::-1]
        non_nan_idx = non_nan_idx[::-1]
    indexer = non_nan_idx[non_nans.argsort(kind=kind)]
    if not ascending:
        indexer = indexer[::-1]
    # Finally, place the NaNs at the end or the beginning according to na_position
    if na_position == 'last':
        indexer = np.concatenate([indexer, nan_idx])
    elif na_position == 'first':
        indexer = np.concatenate([nan_idx, indexer])
    else:
        raise ValueError('invalid na_position: {!r}'.format(na_position))
    return indexer
