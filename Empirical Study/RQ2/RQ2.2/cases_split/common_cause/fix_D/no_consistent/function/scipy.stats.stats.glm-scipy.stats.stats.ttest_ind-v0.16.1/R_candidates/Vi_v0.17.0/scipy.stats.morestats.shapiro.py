def shapiro(x, a=None, reta=False):
    """
    Perform the Shapiro-Wilk test for normality.

    The Shapiro-Wilk test tests the null hypothesis that the
    data was drawn from a normal distribution.

    Parameters
    ----------
    x : array_like
        Array of sample data.
    a : array_like, optional
        Array of internal parameters used in the calculation.  If these
        are not given, they will be computed internally.  If x has length
        n, then a must have length n/2.
    reta : bool, optional
        Whether or not to return the internally computed a values.  The
        default is False.

    Returns
    -------
    W : float
        The test statistic.
    p-value : float
        The p-value for the hypothesis test.
    a : array_like, optional
        If `reta` is True, then these are the internally computed "a"
        values that may be passed into this function on future calls.

    See Also
    --------
    anderson : The Anderson-Darling test for normality
    kstest : The Kolmogorov-Smirnov test for goodness of fit.

    Notes
    -----
    The algorithm used is described in [4]_ but censoring parameters as
    described are not implemented. For N > 5000 the W test statistic is accurate
    but the p-value may not be.

    The chance of rejecting the null hypothesis when it is true is close to 5%
    regardless of sample size.

    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
    .. [2] Shapiro, S. S. & Wilk, M.B (1965). An analysis of variance test for
           normality (complete samples), Biometrika, Vol. 52, pp. 591-611.
    .. [3] Razali, N. M. & Wah, Y. B. (2011) Power comparisons of Shapiro-Wilk,
           Kolmogorov-Smirnov, Lilliefors and Anderson-Darling tests, Journal of
           Statistical Modeling and Analytics, Vol. 2, pp. 21-33.
    .. [4] ALGORITHM AS R94 APPL. STATIST. (1995) VOL. 44, NO. 4.

    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(12345678)
    >>> x = stats.norm.rvs(loc=5, scale=3, size=100)
    >>> stats.shapiro(x)
    (0.9772805571556091, 0.08144091814756393)

    """
    if a is not None or reta:
        warnings.warn("input parameters 'a' and 'reta' are scheduled to be "
                      "removed in version 0.18.0", FutureWarning)
    x = np.ravel(x)

    N = len(x)
    if N < 3:
        raise ValueError("Data must be at least length 3.")
    if a is None:
        a = zeros(N, 'f')
        init = 0
    else:
        if len(a) != N // 2:
            raise ValueError("len(a) must equal len(x)/2")
        init = 1
    y = sort(x)
    a, w, pw, ifault = statlib.swilk(y, a[:N//2], init)
    if ifault not in [0, 2]:
        warnings.warn("Input data for shapiro has range zero. The results "
                      "may not be accurate.")
    if N > 5000:
        warnings.warn("p-value may not be accurate for N > 5000.")
    if reta:
        return w, pw, a
    else:
        return w, pw
