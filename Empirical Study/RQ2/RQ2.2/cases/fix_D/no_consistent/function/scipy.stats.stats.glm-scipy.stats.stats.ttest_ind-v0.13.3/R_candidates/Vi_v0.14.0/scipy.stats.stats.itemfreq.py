def itemfreq(a):
    """
    Returns a 2-D array of item frequencies.

    Parameters
    ----------
    a : (N,) array_like
        Input array.

    Returns
    -------
    itemfreq : (K, 2) ndarray
        A 2-D frequency table.  Column 1 contains sorted, unique values from
        `a`, column 2 contains their respective counts.

    Examples
    --------
    >>> a = np.array([1, 1, 5, 0, 1, 2, 2, 0, 1, 4])
    >>> stats.itemfreq(a)
    array([[ 0.,  2.],
           [ 1.,  4.],
           [ 2.,  2.],
           [ 4.,  1.],
           [ 5.,  1.]])
    >>> np.bincount(a)
    array([2, 4, 2, 0, 1, 1])

    >>> stats.itemfreq(a/10.)
    array([[ 0. ,  2. ],
           [ 0.1,  4. ],
           [ 0.2,  2. ],
           [ 0.4,  1. ],
           [ 0.5,  1. ]])

    """
    items, inv = np.unique(a, return_inverse=True)
    freq = np.bincount(inv)
    return np.array([items, freq]).T
