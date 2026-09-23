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

    References
    ----------
    .. [1]  http://www.itl.nist.gov/div898/handbook/eda/section3/eda357.htm

    .. [2]  Snedecor, George W. and Cochran, William G. (1989), Statistical
              Methods, Eighth Edition, Iowa State University Press.

    """
    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = zeros(k)
    ssq = zeros(k, 'd')
    for j in range(k):
        Ni[j] = len(args[j])
        ssq[j] = np.var(args[j], ddof=1)
    Ntot = sum(Ni, axis=0)
    spsq = sum((Ni - 1)*ssq, axis=0) / (1.0*(Ntot - k))
    numer = (Ntot*1.0 - k) * log(spsq) - sum((Ni - 1.0)*log(ssq), axis=0)
    denom = 1.0 + 1.0/(3*(k - 1)) * ((sum(1.0/(Ni - 1.0), axis=0)) -
                                     1.0/(Ntot - k))
    T = numer / denom
    pval = distributions.chi2.sf(T, k - 1)  # 1 - cdf

    BartlettResult = namedtuple('BartlettResult', ('statistic', 'pvalue'))
    return BartlettResult(T, pval)
