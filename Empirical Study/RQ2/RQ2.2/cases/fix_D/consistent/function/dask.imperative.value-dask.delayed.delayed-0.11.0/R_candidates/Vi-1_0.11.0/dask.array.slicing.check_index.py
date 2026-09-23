def check_index(ind, dimension):
    """ Check validity of index for a given dimension

    Examples
    --------
    >>> check_index(3, 5)
    >>> check_index(5, 5)
    Traceback (most recent call last):
    ...
    IndexError: Index is not smaller than dimension 5 >= 5

    >>> check_index(6, 5)
    Traceback (most recent call last):
    ...
    IndexError: Index is not smaller than dimension 6 >= 5

    >>> check_index(-1, 5)
    >>> check_index(-6, 5)
    Traceback (most recent call last):
    ...
    IndexError: Negative index is not greater than negative dimension -6 <= -5

    >>> check_index([1, 2], 5)
    >>> check_index([6, 3], 5)
    Traceback (most recent call last):
    ...
    IndexError: Index is not smaller than dimension 6 >= 5

    >>> check_index(slice(0, 3), 5)
    """
    if isinstance(ind, list):
        for i in ind:
            check_index(i, dimension)
    elif isinstance(ind, slice):
        return

    elif ind >= dimension:
        raise IndexError("Index is not smaller than dimension %d >= %d"
                % (ind, dimension))

    elif ind <= -dimension:
        raise IndexError(
                "Negative index is not greater than negative dimension %d <= -%d"
                % (ind, dimension))
