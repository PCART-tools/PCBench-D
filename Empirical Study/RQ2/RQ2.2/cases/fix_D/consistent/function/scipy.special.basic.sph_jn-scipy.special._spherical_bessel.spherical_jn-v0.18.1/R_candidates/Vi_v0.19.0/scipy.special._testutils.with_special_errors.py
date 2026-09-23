def with_special_errors(func):
    """
    Enable special function errors (such as underflow, overflow,
    loss of precision, etc.)
    """
    def wrapper(*a, **kw):
        with sc.errstate(all='raise'):
            res = func(*a, **kw)
        return res
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
