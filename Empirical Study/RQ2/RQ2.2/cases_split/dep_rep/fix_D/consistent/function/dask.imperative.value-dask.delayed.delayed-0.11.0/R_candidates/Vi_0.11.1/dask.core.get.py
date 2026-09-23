def get(d, x, recursive=False):
    """ Get value from Dask

    Examples
    --------

    >>> inc = lambda x: x + 1
    >>> d = {'x': 1, 'y': (inc, 'x')}

    >>> get(d, 'x')
    1
    >>> get(d, 'y')
    2
    """
    _get = _get_recursive if recursive else _get_nonrecursive
    if isinstance(x, list):
        return tuple(get(d, k) for k in x)
    elif x in d:
        return _get(d, x)
    raise KeyError("{0} is not a key in the graph".format(x))
