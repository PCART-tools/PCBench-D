def get_names_flat(adtype):
    """
    Returns the field names of the input datatype as a tuple. Nested structure
    are flattened beforehand.

    Parameters
    ----------
    adtype : dtype
        Input datatype

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.get_names_flat(np.empty((1,), dtype=int)) is None
    Traceback (most recent call last):
        ...
    AttributeError: 'numpy.ndarray' object has no attribute 'names'
    >>> rfn.get_names_flat(np.empty((1,), dtype=[('A',int), ('B', float)]))
    Traceback (most recent call last):
        ...
    AttributeError: 'numpy.ndarray' object has no attribute 'names'
    >>> adtype = np.dtype([('a', int), ('b', [('ba', int), ('bb', int)])])
    >>> rfn.get_names_flat(adtype)
    ('a', 'b', 'ba', 'bb')
    """
    listnames = []
    names = adtype.names
    for name in names:
        listnames.append(name)
        current = adtype[name]
        if current.names is not None:
            listnames.extend(get_names_flat(current))
    return tuple(listnames)
