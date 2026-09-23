def _get_names_from_index(data):
    index = lrange(len(data))
    has_some_name = any([getattr(s, 'name', None) is not None for s in data])
    if not has_some_name:
        return index

    count = 0
    for i, s in enumerate(data):
        n = getattr(s, 'name', None)
        if n is not None:
            index[i] = n
        else:
            index[i] = 'Unnamed %d' % count
            count += 1

    return index
