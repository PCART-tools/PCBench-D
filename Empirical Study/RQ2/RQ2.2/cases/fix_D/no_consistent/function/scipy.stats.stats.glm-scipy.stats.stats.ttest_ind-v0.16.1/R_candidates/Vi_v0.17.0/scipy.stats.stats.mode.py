def mode(a, axis=0, nan_policy='propagate'):
    """
    Returns an array of the modal (most common) value in the passed array.

    If there is more than one such value, only the first is returned.
    The bin-count for the modal bins is also returned.

    Parameters
    ----------
    a : array_like
        n-dimensional array of which to find mode(s).
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    mode : ndarray
        Array of modal values.
    count : ndarray
        Array of counts for each mode.

    Examples
    --------
    >>> a = np.array([[6, 8, 3, 0],
    ...               [3, 2, 1, 7],
    ...               [8, 1, 8, 4],
    ...               [5, 3, 0, 5],
    ...               [4, 7, 5, 9]])
    >>> from scipy import stats
    >>> stats.mode(a)
    (array([[3, 1, 0, 0]]), array([[1, 1, 1, 1]]))

    To get mode of whole array, specify ``axis=None``:

    >>> stats.mode(a, axis=None)
    (array([3]), array([3]))

    """
    a, axis = _chk_asarray(a, axis)
    if a.size == 0:
        return np.array([]), np.array([])

    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        return mstats_basic.mode(a, axis)

    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape, dtype=a.dtype)
    oldcounts = np.zeros(testshape, dtype=int)
    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis), axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return ModeResult(mostfrequent, oldcounts)
