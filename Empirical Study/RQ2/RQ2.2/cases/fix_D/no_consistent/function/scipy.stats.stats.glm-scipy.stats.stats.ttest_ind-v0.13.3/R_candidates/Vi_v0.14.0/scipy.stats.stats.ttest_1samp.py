def ttest_1samp(a, popmean, axis=0):
    """
    Calculates the T-test for the mean of ONE group of scores.

    This is a two-sided test for the null hypothesis that the expected value
    (mean) of a sample of independent observations `a` is equal to the given
    population mean, `popmean`.

    Parameters
    ----------
    a : array_like
        sample observation
    popmean : float or array_like
        expected value in null hypothesis, if array_like than it must have the
        same shape as `a` excluding the axis dimension
    axis : int, optional, (default axis=0)
        Axis can equal None (ravel array first), or an integer (the axis
        over which to operate on a).

    Returns
    -------
    t : float or array
        t-statistic
    prob : float or array
        two-tailed p-value

    Examples
    --------
    >>> from scipy import stats

    >>> np.random.seed(7654567)  # fix seed to get the same result
    >>> rvs = stats.norm.rvs(loc=5, scale=10, size=(50,2))

    Test if mean of random sample is equal to true mean, and different mean.
    We reject the null hypothesis in the second case and don't reject it in
    the first case.

    >>> stats.ttest_1samp(rvs,5.0)
    (array([-0.68014479, -0.04323899]), array([ 0.49961383,  0.96568674]))
    >>> stats.ttest_1samp(rvs,0.0)
    (array([ 2.77025808,  4.11038784]), array([ 0.00789095,  0.00014999]))

    Examples using axis and non-scalar dimension for population mean.

    >>> stats.ttest_1samp(rvs,[5.0,0.0])
    (array([-0.68014479,  4.11038784]), array([  4.99613833e-01,   1.49986458e-04]))
    >>> stats.ttest_1samp(rvs.T,[5.0,0.0],axis=1)
    (array([-0.68014479,  4.11038784]), array([  4.99613833e-01,   1.49986458e-04]))
    >>> stats.ttest_1samp(rvs,[[5.0],[0.0]])
    (array([[-0.68014479, -0.04323899],
           [ 2.77025808,  4.11038784]]), array([[  4.99613833e-01,   9.65686743e-01],
           [  7.89094663e-03,   1.49986458e-04]]))

    """
    a, axis = _chk_asarray(a, axis)
    n = a.shape[axis]
    df = n - 1

    d = np.mean(a, axis) - popmean
    v = np.var(a, axis, ddof=1)
    denom = np.sqrt(v / float(n))

    t = np.divide(d, denom)
    t, prob = _ttest_finish(df, t)

    return t, prob
