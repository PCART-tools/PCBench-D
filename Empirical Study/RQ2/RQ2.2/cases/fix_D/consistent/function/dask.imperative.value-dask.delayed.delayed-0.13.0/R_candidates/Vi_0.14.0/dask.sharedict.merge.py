def merge(*dicts):
    result = ShareDict()
    for d in dicts:
        if isinstance(d, tuple):
            key, d = d
            result.update_with_key(d, key=key)
        else:
            result.update_with_key(d)
    return result
