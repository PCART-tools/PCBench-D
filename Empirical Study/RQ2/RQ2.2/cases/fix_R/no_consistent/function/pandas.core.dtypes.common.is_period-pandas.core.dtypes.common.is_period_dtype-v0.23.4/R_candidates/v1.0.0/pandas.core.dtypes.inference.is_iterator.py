def is_iterator(obj) -> bool:
    """
    Check if the object is an iterator.

    For example, lists are considered iterators
    but not strings or datetime objects.

    Parameters
    ----------
    obj : The object to check

    Returns
    -------
    is_iter : bool
        Whether `obj` is an iterator.

    Examples
    --------
    >>> is_iterator([1, 2, 3])
    True
    >>> is_iterator(datetime(2017, 1, 1))
    False
    >>> is_iterator("foo")
    False
    >>> is_iterator(1)
    False
    """

    if not hasattr(obj, "__iter__"):
        return False

    return hasattr(obj, "__next__")
