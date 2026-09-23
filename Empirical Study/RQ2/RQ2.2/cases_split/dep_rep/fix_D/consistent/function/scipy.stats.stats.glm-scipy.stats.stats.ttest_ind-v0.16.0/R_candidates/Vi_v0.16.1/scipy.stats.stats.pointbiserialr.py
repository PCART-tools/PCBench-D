def pointbiserialr(x, y):
    """Calculates a point biserial correlation coefficient and the associated
    p-value.

    The point biserial correlation is used to measure the relationship
    between a binary variable, x, and a continuous variable, y. Like other
    correlation coefficients, this one varies between -1 and +1 with 0
    implying no correlation. Correlations of -1 or +1 imply a determinative
    relationship.

    This function uses a shortcut formula but produces the same result as
    `pearsonr`.

    Parameters
    ----------
    x : array_like of bools
        Input array.
    y : array_like
        Input array.

    Returns
    -------
    correlation : float
        R value
    pvalue : float
        2-tailed p-value

    References
    ----------
    http://en.wikipedia.org/wiki/Point-biserial_correlation_coefficient

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.array([0, 0, 0, 1, 1, 1, 1])
    >>> b = np.arange(7)
    >>> stats.pointbiserialr(a, b)
    (0.8660254037844386, 0.011724811003954652)
    >>> stats.pearsonr(a, b)
    (0.86602540378443871, 0.011724811003954626)
    >>> np.corrcoef(a, b)
    array([[ 1.       ,  0.8660254],
           [ 0.8660254,  1.       ]])

    """
    x = np.asarray(x, dtype=bool)
    y = np.asarray(y, dtype=float)
    n = len(x)

    # phat is the fraction of x values that are True
    phat = x.sum() / float(len(x))
    y0 = y[~x]  # y-values where x is False
    y1 = y[x]  # y-values where x is True
    y0m = y0.mean()
    y1m = y1.mean()

    # phat - phat**2 is more stable than phat*(1-phat)
    rpb = (y1m - y0m) * np.sqrt(phat - phat**2) / y.std()

    df = n - 2
    # fixme: see comment about TINY in pearsonr()
    TINY = 1e-20
    t = rpb * np.sqrt(df / ((1.0 - rpb + TINY)*(1.0 + rpb + TINY)))
    prob = betai(0.5*df, 0.5, df/(df+t*t))

    return PointbiserialrResult(rpb, prob)
