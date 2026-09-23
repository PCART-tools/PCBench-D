def find_repeats(arr):
    """
    Find repeats and repeat counts.

    Parameters
    ----------
    arr : array_like
        Input array. This is cast to float64.

    Returns
    -------
    values : ndarray
        The unique values from the (flattened) input that are repeated.

    counts : ndarray
        Number of times the corresponding 'value' is repeated.

    Notes
    -----
    In numpy >= 1.9 `numpy.unique` provides similar functionality. The main
    difference is that `find_repeats` only returns repeated values.

    Examples
    --------
    >>> from scipy import stats
    >>> stats.find_repeats([2, 1, 2, 3, 2, 2, 5])
    RepeatedResults(values=array([ 2.]), counts=array([4]))

    >>> stats.find_repeats([[10, 20, 1, 2], [5, 5, 4, 4]])
    RepeatedResults(values=array([ 4.,  5.]), counts=array([2, 2]))

    """
    # Note: always copies.
    return RepeatedResults(*_find_repeats(np.array(arr, dtype=np.float64)))
