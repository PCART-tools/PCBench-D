def sanitize_index(ind):
    """ Sanitize the elements for indexing along one axis

    >>> sanitize_index([2, 3, 5])
    [2, 3, 5]
    >>> sanitize_index([True, False, True, False])
    [0, 2]
    >>> sanitize_index(np.array([1, 2, 3]))
    [1, 2, 3]
    >>> sanitize_index(np.array([False, True, True]))
    [1, 2]
    >>> type(sanitize_index(np.int32(0)))
    <type 'int'>
    >>> sanitize_index(1.0)
    1
    >>> sanitize_index(0.5)
    Traceback (most recent call last):
    ...
    IndexError: Bad index.  Must be integer-like: 0.5
    """
    if isinstance(ind, Number):
        ind2 = int(ind)
        if ind2 != ind:
            raise IndexError("Bad index.  Must be integer-like: %s" % ind)
        else:
            return ind2
    if hasattr(ind, 'tolist'):
        ind = ind.tolist()
    if isinstance(ind, list) and ind and isinstance(ind[0], bool):
        ind = [a for a, b in enumerate(ind) if b]
        return ind
    if isinstance(ind, list):
        return [sanitize_index(i) for i in ind]
    if isinstance(ind, slice):
        return slice(sanitize_index(ind.start),
                     sanitize_index(ind.stop),
                     sanitize_index(ind.step))
    if ind is None:
        return ind
    try:
        return sanitize_index(np.array(ind).tolist())
    except:
        raise TypeError("Invalid index type", type(ind), ind)
