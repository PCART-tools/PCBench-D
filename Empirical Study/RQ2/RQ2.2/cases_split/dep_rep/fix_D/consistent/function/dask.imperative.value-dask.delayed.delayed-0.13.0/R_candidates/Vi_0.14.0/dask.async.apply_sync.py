def apply_sync(func, args=(), kwds={}, callback=None):
    """ A naive synchronous version of apply_async """
    res = func(*args, **kwds)
    if callback is not None:
        callback(res)
