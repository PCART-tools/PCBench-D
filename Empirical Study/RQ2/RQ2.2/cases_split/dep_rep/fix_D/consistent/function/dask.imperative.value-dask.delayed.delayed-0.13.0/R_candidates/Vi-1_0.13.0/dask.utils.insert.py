def insert(tup, loc, val):
    """

    >>> insert(('a', 'b', 'c'), 0, 'x')
    ('x', 'b', 'c')
    """
    L = list(tup)
    L[loc] = val
    return tuple(L)
