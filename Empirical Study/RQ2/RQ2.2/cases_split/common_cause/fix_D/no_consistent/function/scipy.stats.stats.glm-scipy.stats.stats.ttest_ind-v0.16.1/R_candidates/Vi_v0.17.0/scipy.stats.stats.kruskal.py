def kruskal(*args, **kwargs):
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
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    statistic : float
       The Kruskal-Wallis H statistic, corrected for ties
    pvalue : float
       The p-value for the test using the assumption that H has a chi
       square distribution

    See Also
    --------
    f_oneway : 1-way ANOVA
    mannwhitneyu : Mann-Whitney rank test on two samples.
    friedmanchisquare : Friedman test for repeated measurements

    Notes
    -----
    Due to the assumption that H has a chi square distribution, the number
    of samples in each group must not be too small.  A typical rule is
    that each sample must have at least 5 measurements.

    References
    ----------
    .. [1] W. H. Kruskal & W. W. Wallis, "Use of Ranks in
       One-Criterion Variance Analysis", Journal of the American Statistical
       Association, Vol. 47, Issue 260, pp. 583-621, 1952.
    .. [2] http://en.wikipedia.org/wiki/Kruskal-Wallis_one-way_analysis_of_variance

    Examples
    --------
    >>> from scipy import stats
    >>> x = [1, 3, 5, 7, 9]
    >>> y = [2, 4, 6, 8, 10]
    >>> stats.kruskal(x, y)
    KruskalResult(statistic=0.27272727272727337, pvalue=0.60150813444058948)

    >>> x = [1, 1, 1]
    >>> y = [2, 2, 2]
    >>> z = [2, 2]
    >>> stats.kruskal(x, y, z)
    KruskalResult(statistic=7.0, pvalue=0.030197383422318501)

    """
    args = list(map(np.asarray, args))
    num_groups = len(args)
    if num_groups < 2:
        raise ValueError("Need at least two groups in stats.kruskal()")

    for arg in args:
        if arg.size == 0:
            return KruskalResult(np.nan, np.nan)
    n = np.asarray(list(map(len, args)))

    if 'nan_policy' in kwargs.keys():
        if kwargs['nan_policy'] not in ('propagate', 'raise', 'omit'):
            raise ValueError("nan_policy must be 'propagate', "
                             "'raise' or'omit'")
        else:
            nan_policy = kwargs['nan_policy']
    else:
        nan_policy = 'propagate'

    contains_nan = False
    for arg in args:
        cn = _contains_nan(arg, nan_policy)
        if cn[0]:
            contains_nan = True
            break

    if contains_nan and nan_policy == 'omit':
        for a in args:
            a = ma.masked_invalid(a)
        return mstats_basic.kruskal(*args)

    if contains_nan and nan_policy == 'propagate':
        return KruskalResult(np.nan, np.nan)

    alldata = np.concatenate(args)
    ranked = rankdata(alldata)
    ties = tiecorrect(ranked)
    if ties == 0:
        raise ValueError('All numbers are identical in kruskal')

    # Compute sum^2/n for each group and sum
    j = np.insert(np.cumsum(n), 0, 0)
    ssbn = 0
    for i in range(num_groups):
        ssbn += _square_of_sums(ranked[j[i]:j[i+1]]) / float(n[i])

    totaln = np.sum(n)
    h = 12.0 / (totaln * (totaln + 1)) * ssbn - 3 * (totaln + 1)
    df = num_groups - 1
    h /= ties

    return KruskalResult(h, distributions.chi2.sf(h, df))
