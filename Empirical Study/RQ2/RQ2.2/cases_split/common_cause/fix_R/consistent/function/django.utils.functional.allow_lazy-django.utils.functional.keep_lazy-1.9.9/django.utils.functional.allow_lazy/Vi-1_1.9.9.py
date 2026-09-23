def allow_lazy(func, *resultclasses):
    """
    A decorator that allows a function to be called with one or more lazy
    arguments. If none of the args are lazy, the function is evaluated
    immediately, otherwise a __proxy__ is returned that will evaluate the
    function when needed.
    """
    lazy_func = lazy(func, *resultclasses)

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, Promise):
                break
        else:
            return func(*args, **kwargs)
        return lazy_func(*args, **kwargs)
    return wrapper
