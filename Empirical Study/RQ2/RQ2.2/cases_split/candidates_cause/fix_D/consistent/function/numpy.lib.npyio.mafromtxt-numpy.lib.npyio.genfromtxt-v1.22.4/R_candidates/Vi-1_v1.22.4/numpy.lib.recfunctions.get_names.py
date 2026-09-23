def get_names(adtype):
    """
    Returns the field names of the input datatype as a tuple.

    Parameters
    ----------
    adtype : dtype
        Input datatype

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.get_names(np.empty((1,), dtype=int))
    Traceback (most recent call last):
        ...
    AttributeError: 'numpy.ndarray' object has no attribute 'names'

    >>> rfn.get_names(np.empty((1,), dtype=[('A',int), ('B', float)]))
    Traceback (most recent call last):
        ...
    AttributeError: 'numpy.ndarray' object has no attribute 'names'
    >>> adtype = np.dtype([('a', int), ('b', [('ba', int), ('bb', int)])])
    >>> rfn.get_names(adtype)
    ('a', ('b', ('ba', 'bb')))
    """
    listnames = []
    names = adtype.names
    for name in names:
        current = adtype[name]
        if current.names is not None:
            listnames.append((name, tuple(get_names(current))))
        else:
            listnames.append(name)
    return tuple(listnames)
