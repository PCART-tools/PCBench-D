def dft(n, scale=None):
    """
    Discrete Fourier transform matrix.

    Create the matrix that computes the discrete Fourier transform of a
    sequence [1]_.  The n-th primitive root of unity used to generate the
    matrix is exp(-2*pi*i/n), where i = sqrt(-1).

    Parameters
    ----------
    n : int
        Size the matrix to create.
    scale : str, optional
        Must be None, 'sqrtn', or 'n'.
        If `scale` is 'sqrtn', the matrix is divided by `sqrt(n)`.
        If `scale` is 'n', the matrix is divided by `n`.
        If `scale` is None (the default), the matrix is not normalized, and the
        return value is simply the Vandermonde matrix of the roots of unity.

    Returns
    -------
    m : (n, n) ndarray
        The DFT matrix.

    Notes
    -----
    When `scale` is None, multiplying a vector by the matrix returned by
    `dft` is mathematically equivalent to (but much less efficient than)
    the calculation performed by `scipy.fftpack.fft`.

    .. versionadded:: 0.14.0

    References
    ----------
    .. [1] "DFT matrix", http://en.wikipedia.org/wiki/DFT_matrix

    Examples
    --------
    >>> np.set_printoptions(precision=5, suppress=True)
    >>> x = np.array([1, 2, 3, 0, 3, 2, 1, 0])
    >>> m = dft(8)
    >>> m.dot(x)   # Comute the DFT of x
    array([ 12.+0.j,  -2.-2.j,   0.-4.j,  -2.+2.j,   4.+0.j,  -2.-2.j,
            -0.+4.j,  -2.+2.j])

    Verify that ``m.dot(x)`` is the same as ``fft(x)``.

    >>> from scipy.fftpack import fft
    >>> fft(x)     # Same result as m.dot(x)
    array([ 12.+0.j,  -2.-2.j,   0.-4.j,  -2.+2.j,   4.+0.j,  -2.-2.j,
             0.+4.j,  -2.+2.j])
    """
    if scale not in [None, 'sqrtn', 'n']:
        raise ValueError("scale must be None, 'sqrtn', or 'n'; "
                         "%r is not valid." % (scale,))

    omegas = np.exp(-2j * np.pi * np.arange(n) / n).reshape(-1, 1)
    m = omegas ** np.arange(n)
    if scale == 'sqrtn':
        m /= math.sqrt(n)
    elif scale == 'n':
        m /= n
    return m
