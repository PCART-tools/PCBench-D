def _get_root(key):
    path = key.split('.')
    cursor = _global_config
    for p in path[:-1]:
        cursor = cursor[p]
    return cursor, path[-1]
