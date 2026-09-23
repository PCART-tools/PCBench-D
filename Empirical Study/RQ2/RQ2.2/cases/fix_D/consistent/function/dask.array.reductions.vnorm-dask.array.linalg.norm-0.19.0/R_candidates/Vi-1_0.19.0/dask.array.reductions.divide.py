def divide(a, b, dtype=None):
    key = lambda x: getattr(x, '__array_priority__', float('-inf'))
    f = divide_lookup.dispatch(type(builtins.max(a, b, key=key)))
    return f(a, b, dtype=dtype)
