def sortkey(item):
    """ Sorting key function that is robust to different types

    Both strings and tuples are common key types in dask graphs.
    However In Python 3 one can not compare strings with tuples directly.
    This function maps many types to a form where they can be compared

    Examples
    --------
    >>> sortkey('Hello')
    ('str', 'Hello')

    >>> sortkey(('x', 1))
    ('tuple', ('x', 1))
    """
    return (type(item).__name__, item)
