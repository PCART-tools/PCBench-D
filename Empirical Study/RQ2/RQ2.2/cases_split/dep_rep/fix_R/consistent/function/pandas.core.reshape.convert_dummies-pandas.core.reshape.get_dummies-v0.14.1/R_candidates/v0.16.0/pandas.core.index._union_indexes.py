def _union_indexes(indexes):
    if len(indexes) == 0:
        raise AssertionError('Must have at least 1 Index to union')
    if len(indexes) == 1:
        result = indexes[0]
        if isinstance(result, list):
            result = Index(sorted(result))
        return result

    indexes, kind = _sanitize_and_check(indexes)
    def _unique_indices(inds):
        def conv(i):
            if isinstance(i, Index):
                i = i.tolist()
            return i
        return Index(lib.fast_unique_multiple_list([ conv(i) for i in inds ]))

    if kind == 'special':
        result = indexes[0]

        if hasattr(result, 'union_many'):
            return result.union_many(indexes[1:])
        else:
            for other in indexes[1:]:
                result = result.union(other)
            return result
    elif kind == 'array':
        index = indexes[0]
        for other in indexes[1:]:
            if not index.equals(other):
                return _unique_indices(indexes)

        return index
    else:
        return _unique_indices(indexes)
