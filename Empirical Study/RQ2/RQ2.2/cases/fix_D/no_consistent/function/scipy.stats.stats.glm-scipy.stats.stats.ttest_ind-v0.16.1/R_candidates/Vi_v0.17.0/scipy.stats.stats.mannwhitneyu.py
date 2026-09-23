def mannwhitneyu(x, y, use_continuity=True, alternative='two-sided'):
    """
    Computes the Mann-Whitney rank test on samples x and y.

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    use_continuity : bool, optional
            Whether a continuity correction (1/2.) should be taken into
            account. Default is True.

    Returns
    -------
    statistic : float
        The Mann-Whitney statistics.
    pvalue : float
        One-sided p-value assuming a asymptotic normal distribution.

    Notes
    -----
    Use only when the number of observation in each sample is > 20 and
    you have 2 independent samples of ranks. Mann-Whitney U is
    significant if the u-obtained is LESS THAN or equal to the critical
    value of U.

    This test corrects for ties and by default uses a continuity correction.
    The reported p-value is for a one-sided hypothesis, to get the two-sided
    p-value multiply the returned p-value by 2.

    """
    x = np.asarray(x)
    y = np.asarray(y)
    n1 = len(x)
    n2 = len(y)
    ranked = rankdata(np.concatenate((x, y)))
    rankx = ranked[0:n1]  # get the x-ranks
    u1 = n1*n2 + (n1*(n1+1))/2.0 - np.sum(rankx, axis=0)  # calc U for x
    u2 = n1*n2 - u1  # remainder is U for y
    T = tiecorrect(ranked)
    if T == 0:
        raise ValueError('All numbers are identical in amannwhitneyu')
    sd = np.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)

    fact2 = 1

    meanrank = n1*n2/2.0 + 0.5 * use_continuity
    if alternative == 'less':
        z = u1 - meanrank
    elif alternative == 'greater':
        z = u2 - meanrank
    elif alternative == 'two-sided':
        bigu = max(u1, u2)
        z = np.abs(bigu - meanrank)
        fact2 = 2.
    else:
        raise ValueError("alternative should be 'less', 'greater'"
                         "or 'two-sided'")

    z = z / sd

    return MannwhitneyuResult(u2, distributions.norm.sf(z) * fact2)
