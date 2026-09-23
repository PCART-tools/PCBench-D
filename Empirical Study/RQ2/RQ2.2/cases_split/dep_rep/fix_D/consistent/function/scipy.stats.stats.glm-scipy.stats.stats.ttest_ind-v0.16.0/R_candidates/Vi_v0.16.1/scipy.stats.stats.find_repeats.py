def find_repeats(arr):
    """
    Find repeats and repeat counts.

    Parameters
    ----------
    arr : array_like
        Input array

    Returns
    -------
    find_repeats : tuple
        Returns a tuple of two 1-D ndarrays.  The first ndarray are the repeats
        as sorted, unique values that are repeated in `arr`.  The second
        ndarray are the counts mapped one-to-one of the repeated values
        in the first ndarray.

    Examples
    --------
    >>> from scipy import stats
    >>> stats.find_repeats([2, 1, 2, 3, 2, 2, 5])
    (array([ 2. ]), array([ 4 ], dtype=int32)

    >>> stats.find_repeats([[10, 20, 1, 2], [5, 5, 4, 4]])
    (array([ 4., 5.]), array([2, 2], dtype=int32))

    """
    v1, v2, n = futil.dfreps(arr)
    return v1[:n], v2[:n]
