def fligner(*args, **kwds):
    """
    Perform Fligner-Killeen test for equality of variance.

    Fligner's test tests the null hypothesis that all input samples
    are from populations with equal variances.  Fligner-Killeen's test is
    distribution free when populations are identical [2]_.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        Arrays of sample data.  Need not be the same length.
    center : {'mean', 'median', 'trimmed'}, optional
        Keyword argument controlling which function of the data is used in
        computing the test statistic.  The default is 'median'.
    proportiontocut : float, optional
        When `center` is 'trimmed', this gives the proportion of data points
        to cut from each end. (See `scipy.stats.trim_mean`.)
        Default is 0.05.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value for the hypothesis test.

    See Also
    --------
    bartlett : A parametric test for equality of k variances in normal samples
    levene : A robust parametric test for equality of k variances

    Notes
    -----
    As with Levene's test there are three variants of Fligner's test that
    differ by the measure of central tendency used in the test.  See `levene`
    for more information.

    Conover et al. (1981) examine many of the existing parametric and
    nonparametric tests by extensive simulations and they conclude that the
    tests proposed by Fligner and Killeen (1976) and Levene (1960) appear to be
    superior in terms of robustness of departures from normality and power [3]_.

    References
    ----------
    .. [1] http://www.stat.psu.edu/~bgl/center/tr/TR993.ps

    .. [2] Fligner, M.A. and Killeen, T.J. (1976). Distribution-free two-sample
           tests for scale. 'Journal of the American Statistical Association.'
           71(353), 210-213.

    .. [3] Park, C. and Lindsay, B. G. (1999). Robust Scale Estimation and
           Hypothesis Testing based on Quadratic Inference Function. Technical
           Report #99-03, Center for Likelihood Studies, Pennsylvania State
           University.

    .. [4] Conover, W. J., Johnson, M. E. and Johnson M. M. (1981). A
           comparative study of tests for homogeneity of variances, with
           applications to the outer continental shelf biding data.
           Technometrics, 23(4), 351-361.

    """
    # Handle empty input
    for a in args:
        if np.asanyarray(a).size == 0:
            return FlignerResult(np.nan, np.nan)

    # Handle keyword arguments.
    center = 'median'
    proportiontocut = 0.05
    for kw, value in kwds.items():
        if kw not in ['center', 'proportiontocut']:
            raise TypeError("fligner() got an unexpected keyword "
                            "argument '%s'" % kw)
        if kw == 'center':
            center = value
        else:
            proportiontocut = value

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")

    if center not in ['mean', 'median', 'trimmed']:
        raise ValueError("Keyword argument <center> must be 'mean', 'median'"
                         + "or 'trimmed'.")

    if center == 'median':
        func = lambda x: np.median(x, axis=0)
    elif center == 'mean':
        func = lambda x: np.mean(x, axis=0)
    else:  # center == 'trimmed'
        args = tuple(stats.trimboth(arg, proportiontocut) for arg in args)
        func = lambda x: np.mean(x, axis=0)

    Ni = asarray([len(args[j]) for j in range(k)])
    Yci = asarray([func(args[j]) for j in range(k)])
    Ntot = np.sum(Ni, axis=0)
    # compute Zij's
    Zij = [abs(asarray(args[i]) - Yci[i]) for i in range(k)]
    allZij = []
    g = [0]
    for i in range(k):
        allZij.extend(list(Zij[i]))
        g.append(len(allZij))

    ranks = stats.rankdata(allZij)
    a = distributions.norm.ppf(ranks / (2*(Ntot + 1.0)) + 0.5)

    # compute Aibar
    Aibar = _apply_func(a, g, np.sum) / Ni
    anbar = np.mean(a, axis=0)
    varsq = np.var(a, axis=0, ddof=1)
    Xsq = np.sum(Ni * (asarray(Aibar) - anbar)**2.0, axis=0) / varsq
    pval = distributions.chi2.sf(Xsq, k - 1)  # 1 - cdf
    return FlignerResult(Xsq, pval)
