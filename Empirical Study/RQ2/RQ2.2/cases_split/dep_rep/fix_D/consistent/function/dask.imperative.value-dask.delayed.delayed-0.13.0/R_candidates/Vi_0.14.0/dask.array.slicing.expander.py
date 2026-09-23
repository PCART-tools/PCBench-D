def expander(where):
    """ An optimized version of insert_many() when *where*
    is known upfront and used many times.

    >>> expander([0, 2])(['a', 'b', 'c'], 'z')
    ('z', 'a', 'z', 'b', 'c')
    """
    return _expander(tuple(where))
