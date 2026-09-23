def posify_index(shape, ind):
    """ Flip negative indices around to positive ones

    >>> posify_index(10, 3)
    3
    >>> posify_index(10, -3)
    7
    >>> posify_index(10, [3, -3])
    [3, 7]

    >>> posify_index((10, 20), (3, -3))
    (3, 17)
    >>> posify_index((10, 20), (3, [3, 4, -3]))
    (3, [3, 4, 17])
    """
    if isinstance(ind, tuple):
        return tuple(map(posify_index, shape, ind))
    if isinstance(ind, (int, long)):
        if ind < 0:
            return ind + shape
        else:
            return ind
    if isinstance(ind, list):
        return [posify_index(shape, i) for i in ind]
    return ind
