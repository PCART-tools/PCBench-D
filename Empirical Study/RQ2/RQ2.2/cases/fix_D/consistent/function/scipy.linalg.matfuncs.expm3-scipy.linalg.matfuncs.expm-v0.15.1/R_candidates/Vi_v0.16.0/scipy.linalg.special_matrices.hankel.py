def hankel(c, r=None):
    """
    Construct a Hankel matrix.

    The Hankel matrix has constant anti-diagonals, with `c` as its
    first column and `r` as its last row.  If `r` is not given, then
    `r = zeros_like(c)` is assumed.

    Parameters
    ----------
    c : array_like
        First column of the matrix.  Whatever the actual shape of `c`, it
        will be converted to a 1-D array.
    r : array_like, optional
        Last row of the matrix. If None, ``r = zeros_like(c)`` is assumed.
        r[0] is ignored; the last row of the returned matrix is
        ``[c[-1], r[1:]]``.  Whatever the actual shape of `r`, it will be
        converted to a 1-D array.

    Returns
    -------
    A : (len(c), len(r)) ndarray
        The Hankel matrix. Dtype is the same as ``(c[0] + r[0]).dtype``.

    See also
    --------
    toeplitz : Toeplitz matrix
    circulant : circulant matrix

    Examples
    --------
    >>> from scipy.linalg import hankel
    >>> hankel([1, 17, 99])
    array([[ 1, 17, 99],
           [17, 99,  0],
           [99,  0,  0]])
    >>> hankel([1,2,3,4], [4,7,7,8,9])
    array([[1, 2, 3, 4, 7],
           [2, 3, 4, 7, 7],
           [3, 4, 7, 7, 8],
           [4, 7, 7, 8, 9]])

    """
    c = np.asarray(c).ravel()
    if r is None:
        r = np.zeros_like(c)
    else:
        r = np.asarray(r).ravel()
    # Form a 1D array of values to be used in the matrix, containing `c`
    # followed by r[1:].
    vals = np.concatenate((c, r[1:]))
    a, b = np.ogrid[0:len(c), 0:len(r)]
    indx = a + b
    # `indx` is a 2D array of indices into the 1D array `vals`, arranged so
    # that `vals[indx]` is the Hankel matrix.
    return vals[indx]
