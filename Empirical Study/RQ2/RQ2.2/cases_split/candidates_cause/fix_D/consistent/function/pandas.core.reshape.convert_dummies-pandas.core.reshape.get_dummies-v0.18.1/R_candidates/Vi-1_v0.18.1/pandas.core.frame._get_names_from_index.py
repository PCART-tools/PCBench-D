def _get_names_from_index(data):
    has_some_name = any([getattr(s, 'name', None) is not None for s in data])
    if not has_some_name:
        return _default_index(len(data))

    index = lrange(len(data))
    count = 0
    for i, s in enumerate(data):
        n = getattr(s, 'name', None)
        if n is not None:
            index[i] = n
        else:
            index[i] = 'Unnamed %d' % count
            count += 1

    return index
