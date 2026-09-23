def ss(a, axis=0):
    """
    Squares each element of the input array, and returns the sum(s) of that.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or None, optional
        The axis along which to calculate. If None, use whole array.
        Default is 0, i.e. along the first axis.

    Returns
    -------
    ss : ndarray
        The sum along the given axis for (a**2).

    See also
    --------
    square_of_sums : The square(s) of the sum(s) (the opposite of `ss`).

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.array([1., 2., 5.])
    >>> stats.ss(a)
    30.0

    And calculating along an axis:

    >>> b = np.array([[1., 2., 5.], [2., 5., 6.]])
    >>> stats.ss(b, axis=1)
    array([ 30., 65.])

    """
    a, axis = _chk_asarray(a, axis)
    return np.sum(a*a, axis)
