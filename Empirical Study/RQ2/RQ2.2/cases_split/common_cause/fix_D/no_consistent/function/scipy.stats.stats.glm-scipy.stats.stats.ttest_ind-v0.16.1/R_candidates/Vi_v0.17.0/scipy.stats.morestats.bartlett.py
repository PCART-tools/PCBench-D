def bartlett(*args):
    """
    Perform Bartlett's test for equal variances

    Bartlett's test tests the null hypothesis that all input samples
    are from populations with equal variances.  For samples
    from significantly non-normal populations, Levene's test
    `levene` is more robust.

    Parameters
    ----------
    sample1, sample2,... : array_like
        arrays of sample data.  May be different lengths.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value of the test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    levene : A robust parametric test for equality of k variances

    Notes
    -----
    Conover et al. (1981) examine many of the existing parametric and
    nonparametric tests by extensive simulations and they conclude that the
    tests proposed by Fligner and Killeen (1976) and Levene (1960) appear to be
    superior in terms of robustness of departures from normality and power [3]_.

    References
    ----------
    .. [1]  http://www.itl.nist.gov/div898/handbook/eda/section3/eda357.htm

    .. [2]  Snedecor, George W. and Cochran, William G. (1989), Statistical
              Methods, Eighth Edition, Iowa State University Press.

    .. [3] Park, C. and Lindsay, B. G. (1999). Robust Scale Estimation and
           Hypothesis Testing based on Quadratic Inference Function. Technical
           Report #99-03, Center for Likelihood Studies, Pennsylvania State
           University.

    .. [4] Bartlett, M. S. (1937). Properties of Sufficiency and Statistical
           Tests. Proceedings of the Royal Society of London. Series A,
           Mathematical and Physical Sciences, Vol. 160, No.901, pp. 268-282.

    """
    # Handle empty input
    for a in args:
        if np.asanyarray(a).size == 0:
            return BartlettResult(np.nan, np.nan)

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = zeros(k)
    ssq = zeros(k, 'd')
    for j in range(k):
        Ni[j] = len(args[j])
        ssq[j] = np.var(args[j], ddof=1)
    Ntot = np.sum(Ni, axis=0)
    spsq = np.sum((Ni - 1)*ssq, axis=0) / (1.0*(Ntot - k))
    numer = (Ntot*1.0 - k) * log(spsq) - np.sum((Ni - 1.0)*log(ssq), axis=0)
    denom = 1.0 + 1.0/(3*(k - 1)) * ((np.sum(1.0/(Ni - 1.0), axis=0)) -
                                     1.0/(Ntot - k))
    T = numer / denom
    pval = distributions.chi2.sf(T, k - 1)  # 1 - cdf

    return BartlettResult(T, pval)
