def helmert(n, full=False):
    """
    Create a Helmert matrix of order `n`.

    This has applications in statistics, compositional or simplicial analysis,
    and in Aitchison geometry.

    Parameters
    ----------
    n : int
        The size of the array to create.
    full : bool, optional
        If True the (n, n) ndarray will be returned.
        Otherwise the submatrix that does not include the first
        row will be returned.
        Default: False.

    Returns
    -------
    M : ndarray
        The Helmert matrix.
        The shape is (n, n) or (n-1, n) depending on the `full` argument.

    Examples
    --------
    >>> from scipy.linalg import helmert
    >>> helmert(5, full=True)
    array([[ 0.4472136 ,  0.4472136 ,  0.4472136 ,  0.4472136 ,  0.4472136 ],
           [ 0.70710678, -0.70710678,  0.        ,  0.        ,  0.        ],
           [ 0.40824829,  0.40824829, -0.81649658,  0.        ,  0.        ],
           [ 0.28867513,  0.28867513,  0.28867513, -0.8660254 ,  0.        ],
           [ 0.2236068 ,  0.2236068 ,  0.2236068 ,  0.2236068 , -0.89442719]])

    """
    H = np.tril(np.ones((n, n)), -1) - np.diag(np.arange(n))
    d = np.arange(n) * np.arange(1, n+1)
    H[0] = 1
    d[0] = n
    H_full = H / np.sqrt(d)[:, np.newaxis]
    if full:
        return H_full
    else:
        return H_full[1:]
