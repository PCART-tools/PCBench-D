def funcname(func):
    """Get the name of a function."""
    # functools.partial
    if isinstance(func, functools.partial):
        return funcname(func.func)
    # methodcaller
    if isinstance(func, methodcaller):
        return func.method

    module_name = getattr(func, '__module__', None) or ''
    type_name = getattr(type(func), '__name__', None) or ''

    # toolz.curry
    if 'toolz' in module_name and 'curry' == type_name:
        return func.func_name
    # multipledispatch objects
    if 'multipledispatch' in module_name and 'Dispatcher' == type_name:
        return func.name

    # All other callables
    try:
        name = func.__name__
        if name == '<lambda>':
            return 'lambda'
        return name
    except:
        return str(func)
