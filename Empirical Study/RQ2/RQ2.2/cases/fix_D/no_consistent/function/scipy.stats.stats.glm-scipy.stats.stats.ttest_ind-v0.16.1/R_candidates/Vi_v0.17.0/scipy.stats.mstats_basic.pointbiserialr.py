def pointbiserialr(x, y):
    """Calculates a point biserial correlation coefficient and its p-value.

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

    Notes
    -----
    Missing values are considered pair-wise: if a value is missing in x,
    the corresponding value in y is masked.

    For more details on `pointbiserialr`, see `stats.pointbiserialr`.

    """
    x = ma.fix_invalid(x, copy=True).astype(bool)
    y = ma.fix_invalid(y, copy=True).astype(float)
    # Get rid of the missing data
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    if m is not nomask:
        unmask = np.logical_not(m)
        x = x[unmask]
        y = y[unmask]

    n = len(x)
    # phat is the fraction of x values that are True
    phat = x.sum() / float(n)
    y0 = y[~x]  # y-values where x is False
    y1 = y[x]  # y-values where x is True
    y0m = y0.mean()
    y1m = y1.mean()

    rpb = (y1m - y0m)*np.sqrt(phat * (1-phat)) / y.std()

    df = n-2
    t = rpb*ma.sqrt(df/(1.0-rpb**2))
    prob = _betai(0.5*df, 0.5, df/(df+t*t))

    return PointbiserialrResult(rpb, prob)
