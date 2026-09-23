@curry
def wrap(wrap_func, func, **kwargs):
    f = partial(wrap_func, func, **kwargs)
    template = """
    Blocked variant of %(name)s

    Follows the signature of %(name)s exactly except that it also requires a
    keyword argument chunks=(...)

    Original signature follows below.
    """
    if func.__doc__ is not None:
        f.__doc__ = template % {'name': func.__name__} + func.__doc__
        f.__name__ = 'blocked_' + func.__name__
    return f
