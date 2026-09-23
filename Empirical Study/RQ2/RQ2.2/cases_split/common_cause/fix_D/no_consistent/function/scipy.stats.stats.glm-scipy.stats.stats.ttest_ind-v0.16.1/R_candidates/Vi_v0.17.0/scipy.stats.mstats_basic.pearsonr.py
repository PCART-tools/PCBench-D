def pearsonr(x,y):
    """
    Calculates a Pearson correlation coefficient and the p-value for testing
    non-correlation.

    The Pearson correlation coefficient measures the linear relationship
    between two datasets. Strictly speaking, Pearson's correlation requires
    that each dataset be normally distributed. Like other correlation
    coefficients, this one varies between -1 and +1 with 0 implying no
    correlation. Correlations of -1 or +1 imply an exact linear
    relationship. Positive correlations imply that as `x` increases, so does
    `y`. Negative correlations imply that as `x` increases, `y` decreases.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Pearson correlation at least as extreme
    as the one computed from these datasets. The p-values are not entirely
    reliable but are probably reasonable for datasets larger than 500 or so.

    Parameters
    ----------
    x : 1-D array_like
        Input
    y : 1-D array_like
        Input

    Returns
    -------
    pearsonr : float
        Pearson's correlation coefficient, 2-tailed p-value.

    References
    ----------
    http://www.statsoft.com/textbook/glosp.html#Pearson%20Correlation

    """
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.ravel(), y.ravel())
    # Get the common mask and the total nb of unmasked elements
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    n -= m.sum()
    df = n-2
    if df < 0:
        return (masked, masked)

    (mx, my) = (x.mean(), y.mean())
    (xm, ym) = (x-mx, y-my)

    r_num = ma.add.reduce(xm*ym)
    r_den = ma.sqrt(ma.dot(xm,xm) * ma.dot(ym,ym))
    r = r_num / r_den
    # Presumably, if r > 1, then it is only some small artifact of floating
    # point arithmetic.
    r = min(r, 1.0)
    r = max(r, -1.0)
    df = n - 2

    if r is masked or abs(r) == 1.0:
        prob = 0.
    else:
        t_squared = (df / ((1.0 - r) * (1.0 + r))) * r * r
        prob = _betai(0.5*df, 0.5, df/(df + t_squared))

    return r, prob
