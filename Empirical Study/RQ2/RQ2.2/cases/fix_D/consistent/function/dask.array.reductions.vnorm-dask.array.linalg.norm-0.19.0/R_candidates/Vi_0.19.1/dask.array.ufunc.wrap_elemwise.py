def wrap_elemwise(numpy_ufunc, array_wrap=False):
    """ Wrap up numpy function into dask.array """

    def wrapped(*args, **kwargs):
        dsk = [arg for arg in args if hasattr(arg, '_elemwise')]
        if len(dsk) > 0:
            if array_wrap:
                return dsk[0]._elemwise(__array_wrap__, numpy_ufunc,
                                        *args, **kwargs)
            else:
                return dsk[0]._elemwise(numpy_ufunc, *args, **kwargs)
        else:
            return numpy_ufunc(*args, **kwargs)

    # functools.wraps cannot wrap ufunc in Python 2.x
    wrapped.__name__ = numpy_ufunc.__name__
    wrapped.__doc__ = skip_doctest(numpy_ufunc.__doc__)
    return wrapped
