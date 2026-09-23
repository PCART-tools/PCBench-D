def _flat_set(x):
    if x is None:
        return set()
    elif isinstance(x, set):
        return x
    elif not isinstance(x, (list, set)):
        x = [x]
    return set(x)
