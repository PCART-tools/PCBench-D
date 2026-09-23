def skewtest(a, axis=0):
    """
    Tests whether the skew is different from the normal distribution.

    Parameters
    ----------
    a : array
        The data to be tested
    axis : int or None, optional
       Axis along which statistics are calculated. Default is 0.
       If None, compute over the whole array `a`.

    Returns
    -------
    statistic : float
        The computed z-score for this test.
    pvalue : float
        a 2-sided p-value for the hypothesis test

    Notes
    -----
    For more details about `skewtest`, see `stats.skewtest`.

    """
    a, axis = _chk_asarray(a, axis)
    if axis is None:
        a = a.ravel()
        axis = 0
    b2 = skew(a,axis)
    n = a.count(axis)
    if np.min(n) < 8:
        raise ValueError(
            "skewtest is not valid with less than 8 samples; %i samples"
            " were given." % np.min(n))

    y = b2 * ma.sqrt(((n+1)*(n+3)) / (6.0*(n-2)))
    beta2 = (3.0*(n*n+27*n-70)*(n+1)*(n+3)) / ((n-2.0)*(n+5)*(n+7)*(n+9))
    W2 = -1 + ma.sqrt(2*(beta2-1))
    delta = 1/ma.sqrt(0.5*ma.log(W2))
    alpha = ma.sqrt(2.0/(W2-1))
    y = ma.where(y == 0, 1, y)
    Z = delta*ma.log(y/alpha + ma.sqrt((y/alpha)**2+1))

    return SkewtestResult(Z, 2 * distributions.norm.sf(np.abs(Z)))
