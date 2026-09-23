def getargspec(func):
    """Version of inspect.getargspec that works for functools.partial objects"""
    if isinstance(func, functools.partial):
        return _getargspec(func.func)
    else:
        if isinstance(func, type):
            return _getargspec(func.__init__)
        else:
            return _getargspec(func)
