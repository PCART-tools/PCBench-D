def funcname(func, full=False):
    """Get the name of a function."""
    while hasattr(func, 'func'):
        func = func.func
    try:
        if full:
            return func.__qualname__.strip('<>')
        else:
            return func.__name__.strip('<>')
    except:
        return str(func).strip('<>')
