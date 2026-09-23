def skewtest(a, axis=0):
    """
    Tests whether the skew is different from the normal distribution.

    This function tests the null hypothesis that the skewness of
    the population that the sample was drawn from is the same
    as that of a corresponding normal distribution.

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
    The sample size must be at least 8.

    """
    a, axis = _chk_asarray(a, axis)
    if axis is None:
        a = np.ravel(a)
        axis = 0
    b2 = skew(a, axis)
    n = float(a.shape[axis])
    if n < 8:
        raise ValueError(
            "skewtest is not valid with less than 8 samples; %i samples"
            " were given." % int(n))
    y = b2 * math.sqrt(((n + 1) * (n + 3)) / (6.0 * (n - 2)))
    beta2 = (3.0 * (n**2 + 27*n - 70) * (n+1) * (n+3) /
             ((n-2.0) * (n+5) * (n+7) * (n+9)))
    W2 = -1 + math.sqrt(2 * (beta2 - 1))
    delta = 1 / math.sqrt(0.5 * math.log(W2))
    alpha = math.sqrt(2.0 / (W2 - 1))
    y = np.where(y == 0, 1, y)
    Z = delta * np.log(y / alpha + np.sqrt((y / alpha)**2 + 1))

    return SkewtestResult(Z, 2 * distributions.norm.sf(np.abs(Z)))
