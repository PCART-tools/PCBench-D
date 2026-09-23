def theilslopes(y, x=None, alpha=0.05):
    """
    Computes the Theil slope as the median of all slopes between paired values.

    Parameters
    ----------
    y : array_like
        Dependent variable.
    x : {None, array_like}, optional
        Independent variable. If None, use arange(len(y)) instead.
    alpha : float
        Confidence degree.

    Returns
    -------
    medslope : float
        Theil slope
    medintercept : float
        Intercept of the Theil line, as median(y)-medslope*median(x)
    lo_slope : float
        Lower bound of the confidence interval on medslope
    up_slope : float
        Upper bound of the confidence interval on medslope

    """
    y = ma.asarray(y).flatten()
    y[-1] = masked
    n = len(y)
    if x is None:
        x = ma.arange(len(y), dtype=float)
    else:
        x = ma.asarray(x).flatten()
        if len(x) != n:
            raise ValueError("Incompatible lengths ! (%s<>%s)" % (n,len(x)))
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    y._mask = x._mask = m
    ny = y.count()
    #
    slopes = ma.hstack([(y[i+1:]-y[i])/(x[i+1:]-x[i]) for i in range(n-1)])
    slopes.sort()
    medslope = ma.median(slopes)
    medinter = ma.median(y) - medslope*ma.median(x)
    #
    if alpha > 0.5:
        alpha = 1.-alpha
    z = stats.distributions.norm.ppf(alpha/2.)
    #
    (xties, yties) = (count_tied_groups(x), count_tied_groups(y))
    nt = ny*(ny-1)/2.
    sigsq = (ny*(ny-1)*(2*ny+5)/18.)
    sigsq -= np.sum(v*k*(k-1)*(2*k+5) for (k,v) in iteritems(xties))
    sigsq -= np.sum(v*k*(k-1)*(2*k+5) for (k,v) in iteritems(yties))
    sigma = np.sqrt(sigsq)

    Ru = min(np.round((nt - z*sigma)/2. + 1), len(slopes)-1)
    Rl = max(np.round((nt + z*sigma)/2.), 0)
    delta = slopes[[Rl,Ru]]
    return medslope, medinter, delta[0], delta[1]
