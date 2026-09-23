def hilbert(n):
    """
    Create a Hilbert matrix of order `n`.

    Returns the `n` by `n` array with entries `h[i,j] = 1 / (i + j + 1)`.

    Parameters
    ----------
    n : int
        The size of the array to create.

    Returns
    -------
    h : (n, n) ndarray
        The Hilbert matrix.

    See Also
    --------
    invhilbert : Compute the inverse of a Hilbert matrix.

    Notes
    -----
    .. versionadded:: 0.10.0

    Examples
    --------
    >>> from scipy.linalg import hilbert
    >>> hilbert(3)
    array([[ 1.        ,  0.5       ,  0.33333333],
           [ 0.5       ,  0.33333333,  0.25      ],
           [ 0.33333333,  0.25      ,  0.2       ]])

    """
    values = 1.0 / (1.0 + np.arange(2 * n - 1))
    h = hankel(values[:n], r=values[n - 1:])
    return h
