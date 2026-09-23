def friedmanchisquare(*args):
    """
    Computes the Friedman test for repeated measurements

    The Friedman test tests the null hypothesis that repeated measurements of
    the same individuals have the same distribution.  It is often used
    to test for consistency among measurements obtained in different ways.
    For example, if two measurement techniques are used on the same set of
    individuals, the Friedman test can be used to determine if the two
    measurement techniques are consistent.

    Parameters
    ----------
    measurements1, measurements2, measurements3... : array_like
        Arrays of measurements.  All of the arrays must have the same number
        of elements.  At least 3 sets of measurements must be given.

    Returns
    -------
    statistic : float
        the test statistic, correcting for ties
    pvalue : float
        the associated p-value assuming that the test statistic has a chi
        squared distribution

    Notes
    -----
    Due to the assumption that the test statistic has a chi squared
    distribution, the p-value is only reliable for n > 10 and more than
    6 repeated measurements.

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Friedman_test

    """
    k = len(args)
    if k < 3:
        raise ValueError('\nLess than 3 levels.  Friedman test not appropriate.\n')

    n = len(args[0])
    for i in range(1, k):
        if len(args[i]) != n:
            raise ValueError('Unequal N in friedmanchisquare.  Aborting.')

    # Rank data
    data = np.vstack(args).T
    data = data.astype(float)
    for i in range(len(data)):
        data[i] = rankdata(data[i])

    # Handle ties
    ties = 0
    for i in range(len(data)):
        replist, repnum = find_repeats(array(data[i]))
        for t in repnum:
            ties += t * (t*t - 1)
    c = 1 - ties / float(k*(k*k - 1)*n)

    ssbn = np.sum(data.sum(axis=0)**2)
    chisq = (12.0 / (k*n*(k+1)) * ssbn - 3*n*(k+1)) / c

    FriedmanchisquareResult = namedtuple('FriedmanchisquareResult',
                                         ('statistic', 'pvalue'))
    return FriedmanchisquareResult(chisq, chisqprob(chisq, k - 1))
