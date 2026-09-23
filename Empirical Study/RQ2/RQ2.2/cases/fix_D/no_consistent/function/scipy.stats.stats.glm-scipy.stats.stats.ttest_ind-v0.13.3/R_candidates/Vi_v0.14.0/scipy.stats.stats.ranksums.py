def ranksums(x, y):
    """
    Compute the Wilcoxon rank-sum statistic for two samples.

    The Wilcoxon rank-sum test tests the null hypothesis that two sets
    of measurements are drawn from the same distribution.  The alternative
    hypothesis is that values in one sample are more likely to be
    larger than the values in the other sample.

    This test should be used to compare two samples from continuous
    distributions.  It does not handle ties between measurements
    in x and y.  For tie-handling and an optional continuity correction
    see `scipy.stats.mannwhitneyu`.

    Parameters
    ----------
    x,y : array_like
        The data from the two samples

    Returns
    -------
    z-statistic : float
        The test statistic under the large-sample approximation that the
        rank sum statistic is normally distributed
    p-value : float
        The two-sided p-value of the test

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Wilcoxon_rank-sum_test

    """
    x,y = map(np.asarray, (x, y))
    n1 = len(x)
    n2 = len(y)
    alldata = np.concatenate((x,y))
    ranked = rankdata(alldata)
    x = ranked[:n1]
    y = ranked[n1:]
    s = np.sum(x,axis=0)
    expected = n1*(n1+n2+1) / 2.0
    z = (s - expected) / np.sqrt(n1*n2*(n1+n2+1)/12.0)
    prob = 2 * distributions.norm.sf(abs(z))
    return z, prob
