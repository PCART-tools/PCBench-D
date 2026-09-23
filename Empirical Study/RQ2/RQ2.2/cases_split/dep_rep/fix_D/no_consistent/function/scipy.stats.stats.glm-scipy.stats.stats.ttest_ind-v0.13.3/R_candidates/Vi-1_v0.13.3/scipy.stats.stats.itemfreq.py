def itemfreq(a):
    """
    Returns a 2D array of item frequencies.

    Parameters
    ----------
    a : (N,) array_like
        Input array.

    Returns
    -------
    itemfreq : (2,K) ndarray
        A 2D frequency table (col [0:n-1]=scores, col n=frequencies).
        Column 1 contains sorted, unique values from `a`, column 2 contains
        their respective counts.

    Notes
    -----
    This uses a loop that is only reasonably fast if the number of unique
    elements is not large. For integers, numpy.bincount is much faster.
    This function currently does not support strings or multi-dimensional
    scores.

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
    # TODO: I'm not sure I understand what this does. The docstring is
    # internally inconsistent.
    # comment: fortunately, this function doesn't appear to be used elsewhere
    scores = _support.unique(a)
    scores = np.sort(scores)
    freq = zeros(len(scores))
    for i in range(len(scores)):
        freq[i] = np.add.reduce(np.equal(a,scores[i]))
    return array(_support.abut(scores, freq))
