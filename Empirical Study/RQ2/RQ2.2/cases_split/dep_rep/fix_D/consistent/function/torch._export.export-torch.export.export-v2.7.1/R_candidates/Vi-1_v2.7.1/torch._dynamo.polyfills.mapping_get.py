def mapping_get(obj, key, value=None):
    try:
        return obj.__getitem__(key)
    except KeyError:
        return value
