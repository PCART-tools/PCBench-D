def wrap_rolling(func):
    """Create a chunked version of a pandas.rolling_* function"""
    @wraps(func)
    def rolling(arg, window, *args, **kwargs):
        if not isinstance(window, int):
            raise TypeError('Window must be an integer')
        if window < 0:
            raise ValueError('Window must be a positive integer')
        if 'freq' in kwargs or 'how' in kwargs:
            raise NotImplementedError('Resampling before rolling computations '
                                      'not supported')
        old_name = arg._name
        token = tokenize(func, arg, window, args, kwargs)
        new_name = 'rolling-' + token
        f = partial(func, **kwargs)
        dsk = {(new_name, 0): (f, (old_name, 0), window) + args}
        for i in range(1, arg.npartitions + 1):
            dsk[(new_name, i)] = (rolling_chunk, f, (old_name, i - 1),
                                  (old_name, i), window) + args
        return arg._constructor(merge(arg.dask, dsk), new_name,
                                arg, arg.divisions)
    return rolling
