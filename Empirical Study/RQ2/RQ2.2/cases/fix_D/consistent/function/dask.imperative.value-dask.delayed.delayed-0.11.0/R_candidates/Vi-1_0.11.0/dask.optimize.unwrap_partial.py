def unwrap_partial(func):
    while hasattr(func, 'func'):
        func = func.func
    return func
