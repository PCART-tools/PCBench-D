def sanitize_index(ind):
    """ Sanitize the elements for indexing along one axis

    >>> sanitize_index([2, 3, 5])
    array([2, 3, 5])
    >>> sanitize_index([True, False, True, False])
    array([0, 2])
    >>> sanitize_index(np.array([1, 2, 3]))
    array([1, 2, 3])
    >>> sanitize_index(np.array([False, True, True]))
    array([1, 2])
    >>> type(sanitize_index(np.int32(0)))
    <class 'int'>
    >>> sanitize_index(1.0)
    1
    >>> sanitize_index(0.5)
    Traceback (most recent call last):
    ...
    IndexError: Bad index.  Must be integer-like: 0.5
    """
    if ind is None:
        return None
    elif isinstance(ind, slice):
        return slice(_sanitize_index_element(ind.start),
                     _sanitize_index_element(ind.stop),
                     _sanitize_index_element(ind.step))
    elif isinstance(ind, Number):
        return _sanitize_index_element(ind)
    elif is_dask_collection(ind):
        return ind
    index_array = np.asanyarray(ind)
    if index_array.dtype == bool:
        nonzero = np.nonzero(index_array)
        if len(nonzero) == 1:
            # If a 1-element tuple, unwrap the element
            nonzero = nonzero[0]
        return np.asanyarray(nonzero)
    elif np.issubdtype(index_array.dtype, np.integer):
        return index_array
    elif np.issubdtype(index_array.dtype, float):
        int_index = index_array.astype(np.intp)
        if np.allclose(index_array, int_index):
            return int_index
        else:
            check_int = np.isclose(index_array, int_index)
            first_err = index_array.ravel(
            )[np.flatnonzero(~check_int)[0]]
            raise IndexError("Bad index.  Must be integer-like: %s" %
                             first_err)
    else:
        raise TypeError("Invalid index type", type(ind), ind)
