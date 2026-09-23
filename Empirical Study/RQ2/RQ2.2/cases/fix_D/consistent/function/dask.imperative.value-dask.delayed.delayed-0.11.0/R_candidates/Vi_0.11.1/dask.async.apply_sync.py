def apply_sync(func, args=(), kwds={}):
    """ A naive synchronous version of apply_async """
    return func(*args, **kwds)
