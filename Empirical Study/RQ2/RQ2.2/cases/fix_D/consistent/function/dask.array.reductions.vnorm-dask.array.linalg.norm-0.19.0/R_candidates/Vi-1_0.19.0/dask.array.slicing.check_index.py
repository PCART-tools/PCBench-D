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
    IndexError: Index out of bounds 5

    >>> check_index(slice(0, 3), 5)

    >>> check_index([True], 1)
    >>> check_index([True, True], 3)
    Traceback (most recent call last):
    ...
    IndexError: Boolean array length 2 doesn't equal dimension 3
    >>> check_index([True, True, True], 1)
    Traceback (most recent call last):
    ...
    IndexError: Boolean array length 3 doesn't equal dimension 1
    """
    # unknown dimension, assumed to be in bounds
    if np.isnan(dimension):
        return
    elif isinstance(ind, (list, np.ndarray)):
        x = np.asanyarray(ind)
        if x.dtype == bool:
            if x.size != dimension:
                raise IndexError(
                    "Boolean array length %s doesn't equal dimension %s" %
                    (x.size, dimension))
        elif (x >= dimension).any() or (x < -dimension).any():
            raise IndexError("Index out of bounds %s" % dimension)
    elif isinstance(ind, slice):
        return
    elif is_dask_collection(ind):
        return
    elif ind is None:
        return

    elif ind >= dimension:
        raise IndexError("Index is not smaller than dimension %d >= %d" %
                         (ind, dimension))

    elif ind < -dimension:
        msg = "Negative index is not greater than negative dimension %d <= -%d"
        raise IndexError(msg % (ind, dimension))
