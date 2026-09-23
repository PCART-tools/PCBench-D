def _get_recursive(d, x):
    # recursive, no cycle detection
    if isinstance(x, list):
        return [_get_recursive(d, k) for k in x]
    elif ishashable(x) and x in d:
        return _get_recursive(d, d[x])
    elif istask(x):
        func, args = x[0], x[1:]
        args2 = [_get_recursive(d, k) for k in args]
        return func(*args2)
    else:
        return x
