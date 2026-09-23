def __array_wrap__(numpy_ufunc, x, *args, **kwargs):
    return x.__array_wrap__(numpy_ufunc(x, *args, **kwargs))
