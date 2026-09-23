def getcycle(d, keys):
    """ Return a list of nodes that form a cycle if Dask is not a DAG.

    Returns an empty list if no cycle is found.

    ``keys`` may be a single key or list of keys.

    Examples
    --------

    >>> d = {'x': (inc, 'z'), 'y': (inc, 'x'), 'z': (inc, 'y')}
    >>> getcycle(d, 'x')
    ['x', 'z', 'y', 'x']

    See Also
    --------
    isdag
    """
    return _toposort(d, keys=keys, returncycle=True)
