def str_slice_replace(arr, start=None, stop=None, repl=None):
    """
    Replace a slice of each string in the Series/Index with another
    string.

    Parameters
    ----------
    start : int or None
    stop : int or None
    repl : str or None
        String for replacement

    Returns
    -------
    replaced : Series/Index of objects
    """
    if repl is None:
        repl = ''

    def f(x):
        if x[start:stop] == '':
            local_stop = start
        else:
            local_stop = stop
        y = ''
        if start is not None:
            y += x[:start]
        y += repl
        if stop is not None:
            y += x[local_stop:]
        return y

    return _na_map(f, arr)
