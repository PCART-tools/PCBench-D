def square_of_sums(a, axis=0):
    """
    Sums elements of the input array, and returns the square(s) of that sum.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or None, optional
        If axis is None, ravel `a` first. If `axis` is an integer, this will
        be the axis over which to operate. Defaults to 0.

    Returns
    -------
    square_of_sums : float or ndarray
        The square of the sum over `axis`.

    See also
    --------
    ss : The sum of squares (the opposite of `square_of_sums`).

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.arange(20).reshape(5,4)
    >>> stats.square_of_sums(a)
    array([ 1600.,  2025.,  2500.,  3025.])
    >>> stats.square_of_sums(a, axis=None)
    36100.0

    """
    a, axis = _chk_asarray(a, axis)
    s = np.sum(a,axis)
    if not np.isscalar(s):
        return s.astype(float)*s
    else:
        return float(s)*s
