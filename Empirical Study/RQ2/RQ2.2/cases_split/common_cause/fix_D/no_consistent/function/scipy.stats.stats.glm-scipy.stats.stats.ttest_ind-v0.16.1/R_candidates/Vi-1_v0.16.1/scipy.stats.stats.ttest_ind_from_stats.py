def ttest_ind_from_stats(mean1, std1, nobs1, mean2, std2, nobs2,
                         equal_var=True):
    """
    T-test for means of two independent samples from descriptive statistics.

    This is a two-sided test for the null hypothesis that 2 independent samples
    have identical average (expected) values.

    Parameters
    ----------
    mean1 : array_like
        The mean(s) of sample 1.
    std1 : array_like
        The standard deviation(s) of sample 1.
    nobs1 : array_like
        The number(s) of observations of sample 1.
    mean2 : array_like
        The mean(s) of sample 2
    std2 : array_like
        The standard deviations(s) of sample 2.
    nobs2 : array_like
        The number(s) of observations of sample 2.
    equal_var : bool, optional
        If True (default), perform a standard independent 2 sample test
        that assumes equal population variances [1]_.
        If False, perform Welch's t-test, which does not assume equal
        population variance [2]_.

    Returns
    -------
    statistic : float or array
        The calculated t-statistics
    pvalue : float or array
        The two-tailed p-value.

    See also
    --------
    scipy.stats.ttest_ind

    Notes
    -----

    .. versionadded:: 0.16.0

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/T-test#Independent_two-sample_t-test

    .. [2] http://en.wikipedia.org/wiki/Welch%27s_t_test
    """
    if equal_var:
        df, denom = _equal_var_ttest_denom(std1**2, nobs1, std2**2, nobs2)
    else:
        df, denom = _unequal_var_ttest_denom(std1**2, nobs1,
                                             std2**2, nobs2)

    res = _ttest_ind_from_stats(mean1, mean2, denom, df)
    return Ttest_indResult(*res)
