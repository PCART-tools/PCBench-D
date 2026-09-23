def check_bool_indexer(ax, key):
    # boolean indexing, need to check that the data are aligned, otherwise
    # disallowed

    # this function assumes that is_bool_indexer(key) == True

    result = key
    if isinstance(key, ABCSeries) and not key.index.equals(ax):
        result = result.reindex(ax)
        mask = isnull(result._values)
        if mask.any():
            raise IndexingError('Unalignable boolean Series key provided')
        result = result.astype(bool)._values
    elif is_sparse(result):
        result = result.to_dense()
        result = np.asarray(result, dtype=bool)
    else:
        # is_bool_indexer has already checked for nulls in the case of an
        # object array key, so no check needed here
        result = np.asarray(result, dtype=bool)

    return result
