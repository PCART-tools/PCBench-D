def leslie(f, s):
    """
    Create a Leslie matrix.

    Given the length n array of fecundity coefficients `f` and the length
    n-1 array of survival coefficents `s`, return the associated Leslie matrix.

    Parameters
    ----------
    f : (N,) array_like
        The "fecundity" coefficients.
    s : (N-1,) array_like
        The "survival" coefficients, has to be 1-D.  The length of `s`
        must be one less than the length of `f`, and it must be at least 1.

    Returns
    -------
    L : (N, N) ndarray
        The array is zero except for the first row,
        which is `f`, and the first sub-diagonal, which is `s`.
        The data-type of the array will be the data-type of ``f[0]+s[0]``.

    Notes
    -----
    .. versionadded:: 0.8.0

    The Leslie matrix is used to model discrete-time, age-structured
    population growth [1]_ [2]_. In a population with `n` age classes, two sets
    of parameters define a Leslie matrix: the `n` "fecundity coefficients",
    which give the number of offspring per-capita produced by each age
    class, and the `n` - 1 "survival coefficients", which give the
    per-capita survival rate of each age class.

    References
    ----------
    .. [1] P. H. Leslie, On the use of matrices in certain population
           mathematics, Biometrika, Vol. 33, No. 3, 183--212 (Nov. 1945)
    .. [2] P. H. Leslie, Some further notes on the use of matrices in
           population mathematics, Biometrika, Vol. 35, No. 3/4, 213--245
           (Dec. 1948)

    Examples
    --------
    >>> from scipy.linalg import leslie
    >>> leslie([0.1, 2.0, 1.0, 0.1], [0.2, 0.8, 0.7])
    array([[ 0.1,  2. ,  1. ,  0.1],
           [ 0.2,  0. ,  0. ,  0. ],
           [ 0. ,  0.8,  0. ,  0. ],
           [ 0. ,  0. ,  0.7,  0. ]])

    """
    f = np.atleast_1d(f)
    s = np.atleast_1d(s)
    if f.ndim != 1:
        raise ValueError("Incorrect shape for f.  f must be one-dimensional")
    if s.ndim != 1:
        raise ValueError("Incorrect shape for s.  s must be one-dimensional")
    if f.size != s.size + 1:
        raise ValueError("Incorrect lengths for f and s.  The length"
                         " of s must be one less than the length of f.")
    if s.size == 0:
        raise ValueError("The length of s must be at least 1.")

    tmp = f[0] + s[0]
    n = f.size
    a = np.zeros((n, n), dtype=tmp.dtype)
    a[0] = f
    a[list(range(1, n)), list(range(0, n - 1))] = s
    return a
