def flatten(obj, result=None):
    """Return flattened version of (possibly nested) iterable object."""
    if not isinstance(obj, Iterable | Sized) or isinstance(obj, str):
        return obj
    if result is None:
        result = []
    for item in obj:
        if not isinstance(item, Iterable | Sized) or isinstance(item, str):
            result.append(item)
        else:
            flatten(item, result)
    return tuple(result)
