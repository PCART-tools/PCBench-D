def circulant(c):
    """
    Construct a circulant matrix.

    Parameters
    ----------
    c : (N,) array_like
        1-D array, the first column of the matrix.

    Returns
    -------
    A : (N, N) ndarray
        A circulant matrix whose first column is `c`.

    See also
    --------
    toeplitz : Toeplitz matrix
    hankel : Hankel matrix

    Notes
    -----
    .. versionadded:: 0.8.0

    Examples
    --------
    >>> from scipy.linalg import circulant
    >>> circulant([1, 2, 3])
    array([[1, 3, 2],
           [2, 1, 3],
           [3, 2, 1]])

    """
    c = np.asarray(c).ravel()
    a, b = np.ogrid[0:len(c), 0:-len(c):-1]
    indx = a + b
    # `indx` is a 2D array of indices into `c`, arranged so that `c[indx]` is
    # the circulant matrix.
    return c[indx]
