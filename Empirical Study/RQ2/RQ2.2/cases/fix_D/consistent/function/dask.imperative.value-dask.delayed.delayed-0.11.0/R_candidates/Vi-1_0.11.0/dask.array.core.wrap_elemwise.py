def wrap_elemwise(func, **kwargs):
    """ Wrap up numpy function into dask.array """
    f = partial(elemwise, func, **kwargs)
    f.__doc__ = func.__doc__
    f.__name__ = func.__name__
    return f
