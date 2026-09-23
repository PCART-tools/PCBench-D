def _square_of_sums(a, axis=0):
    """
    Sums elements of the input array, and returns the square(s) of that sum.
    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or None, optional
        Axis along which to calculate. Default is 0. If None, compute over
        the whole array `a`.
    Returns
    -------
    square_of_sums : float or ndarray
        The square of the sum over `axis`.
    See also
    --------
    _sum_of_squares : The sum of squares (the opposite of `square_of_sums`).
    """
    s = da.sum(a, axis)
    return s * s
