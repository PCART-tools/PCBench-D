def kruskal(*args):
    """
    Compute the Kruskal-Wallis H-test for independent samples

    The Kruskal-Wallis H-test tests the null hypothesis that the population
    median of all of the groups are equal.  It is a non-parametric version of
    ANOVA.  The test works on 2 or more independent samples, which may have
    different sizes.  Note that rejecting the null hypothesis does not
    indicate which of the groups differs.  Post-hoc comparisons between
    groups are required to determine which groups are different.

    Parameters
    ----------
    sample1, sample2, ... : array_like
       Two or more arrays with the sample measurements can be given as
       arguments.

    Returns
    -------
    statistic : float
       The Kruskal-Wallis H statistic, corrected for ties
    pvalue : float
       The p-value for the test using the assumption that H has a chi
       square distribution

    Notes
    -----
    Due to the assumption that H has a chi square distribution, the number
    of samples in each group must not be too small.  A typical rule is
    that each sample must have at least 5 measurements.

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Kruskal-Wallis_one-way_analysis_of_variance

    """
    args = list(map(np.asarray, args))  # convert to a numpy array
    na = len(args)     # Kruskal-Wallis on 'na' groups, each in it's own array
    if na < 2:
        raise ValueError("Need at least two groups in stats.kruskal()")
    n = np.asarray(list(map(len, args)))

    alldata = np.concatenate(args)
    ranked = rankdata(alldata)  # Rank the data
    ties = tiecorrect(ranked)      # Correct for ties
    if ties == 0:
        raise ValueError('All numbers are identical in kruskal')

    # Compute sum^2/n for each group and sum
    j = np.insert(np.cumsum(n), 0, 0)
    ssbn = 0
    for i in range(na):
        ssbn += square_of_sums(ranked[j[i]:j[i+1]]) / float(n[i])

    totaln = np.sum(n)
    h = 12.0 / (totaln * (totaln + 1)) * ssbn - 3 * (totaln + 1)
    df = na - 1
    h /= ties

    return KruskalResult(h, chisqprob(h, df))
