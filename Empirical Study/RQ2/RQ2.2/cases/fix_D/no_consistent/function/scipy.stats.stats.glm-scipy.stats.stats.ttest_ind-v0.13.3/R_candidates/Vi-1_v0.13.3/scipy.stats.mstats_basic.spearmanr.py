def spearmanr(x, y, use_ties=True):
    """
    Calculates a Spearman rank-order correlation coefficient and the p-value
    to test for non-correlation.

    The Spearman correlation is a nonparametric measure of the linear
    relationship between two datasets. Unlike the Pearson correlation, the
    Spearman correlation does not assume that both datasets are normally
    distributed. Like other correlation coefficients, this one varies
    between -1 and +1 with 0 implying no correlation. Correlations of -1 or
    +1 imply an exact linear relationship. Positive correlations imply that
    as `x` increases, so does `y`. Negative correlations imply that as `x`
    increases, `y` decreases.

    Missing values are discarded pair-wise: if a value is missing in `x`, the
    corresponding value in `y` is masked.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Spearman correlation at least as extreme
    as the one computed from these datasets. The p-values are not entirely
    reliable but are probably reasonable for datasets larger than 500 or so.

    Parameters
    ----------
    x : array_like
        The length of `x` must be > 2.
    y : array_like
        The length of `y` must be > 2.
    use_ties : bool, optional
        Whether the correction for ties should be computed.

    Returns
    -------
    spearmanr : float
        Spearman correlation coefficient, 2-tailed p-value.

    References
    ----------
    [CRCProbStat2000] section 14.7

    """
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.ravel(), y.ravel())
    #
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    n -= m.sum()
    if m is not nomask:
        x = ma.array(x, mask=m, copy=True)
        y = ma.array(y, mask=m, copy=True)
    df = n-2
    if df < 0:
        raise ValueError("The input must have at least 3 entries!")
    # Gets the ranks and rank differences
    rankx = rankdata(x)
    ranky = rankdata(y)
    dsq = np.add.reduce((rankx-ranky)**2)
    # Tie correction
    if use_ties:
        xties = count_tied_groups(x)
        yties = count_tied_groups(y)
        corr_x = np.sum(v*k*(k**2-1) for (k,v) in iteritems(xties))/12.
        corr_y = np.sum(v*k*(k**2-1) for (k,v) in iteritems(yties))/12.
    else:
        corr_x = corr_y = 0
    denom = n*(n**2 - 1)/6.
    if corr_x != 0 or corr_y != 0:
        rho = denom - dsq - corr_x - corr_y
        rho /= ma.sqrt((denom-2*corr_x)*(denom-2*corr_y))
    else:
        rho = 1. - dsq/denom
    #
    t = ma.sqrt(ma.divide(df,(rho+1.0)*(1.0-rho))) * rho
    if t is masked:
        prob = 0.
    else:
        prob = betai(0.5*df,0.5,df/(df+t*t))
    return rho, prob
