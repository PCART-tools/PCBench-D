def _sanitize_and_check(indexes):
    kinds = list(set([type(index) for index in indexes]))

    if list in kinds:
        if len(kinds) > 1:
            indexes = [Index(com._try_sort(x))
                       if not isinstance(x, Index) else x
                       for x in indexes]
            kinds.remove(list)
        else:
            return indexes, 'list'

    if len(kinds) > 1 or Index not in kinds:
        return indexes, 'special'
    else:
        return indexes, 'array'
