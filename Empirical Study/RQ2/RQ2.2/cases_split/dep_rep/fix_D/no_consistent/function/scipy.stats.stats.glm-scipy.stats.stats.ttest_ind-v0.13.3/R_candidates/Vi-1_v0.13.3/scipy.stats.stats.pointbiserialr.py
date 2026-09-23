def pointbiserialr(x, y):
    # comment: I am changing the semantics somewhat. The original function is
    # fairly general and accepts an x sequence that has any type of thing in it as
    # along as there are only two unique items. I am going to restrict this to
    # a boolean array for my sanity.
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
    r : float
        R value
    p-value : float
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

    ## Test data: http://support.sas.com/ctx/samples/index.jsp?sid=490&tab=output
    # x = [1,0,1,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]
    # y = [14.8,13.8,12.4,10.1,7.1,6.1,5.8,4.6,4.3,3.5,3.3,3.2,3.0,2.8,2.8,2.5,
    #      2.4,2.3,2.1,1.7,1.7,1.5,1.3,1.3,1.2,1.2,1.1,0.8,0.7,0.6,0.5,0.2,0.2,
    #      0.1]
    # rpb = 0.36149

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

    df = n-2
    # fixme: see comment about TINY in pearsonr()
    TINY = 1e-20
    t = rpb*np.sqrt(df/((1.0-rpb+TINY)*(1.0+rpb+TINY)))
    prob = betai(0.5*df, 0.5, df/(df+t*t))
    return rpb, prob
