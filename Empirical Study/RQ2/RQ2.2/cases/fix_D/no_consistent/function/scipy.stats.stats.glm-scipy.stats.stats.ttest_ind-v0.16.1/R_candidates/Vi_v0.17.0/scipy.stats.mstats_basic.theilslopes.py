def theilslopes(y, x=None, alpha=0.95):
    r"""
    Computes the Theil-Sen estimator for a set of points (x, y).

    `theilslopes` implements a method for robust linear regression.  It
    computes the slope as the median of all slopes between paired values.

    Parameters
    ----------
    y : array_like
        Dependent variable.
    x : array_like or None, optional
        Independent variable. If None, use ``arange(len(y))`` instead.
    alpha : float, optional
        Confidence degree between 0 and 1. Default is 95% confidence.
        Note that `alpha` is symmetric around 0.5, i.e. both 0.1 and 0.9 are
        interpreted as "find the 90% confidence interval".

    Returns
    -------
    medslope : float
        Theil slope.
    medintercept : float
        Intercept of the Theil line, as ``median(y) - medslope*median(x)``.
    lo_slope : float
        Lower bound of the confidence interval on `medslope`.
    up_slope : float
        Upper bound of the confidence interval on `medslope`.

    Notes
    -----
    For more details on `theilslopes`, see `stats.theilslopes`.

    """
    y = ma.asarray(y).flatten()
    if x is None:
        x = ma.arange(len(y), dtype=float)
    else:
        x = ma.asarray(x).flatten()
        if len(x) != len(y):
            raise ValueError("Incompatible lengths ! (%s<>%s)" % (len(y),len(x)))

    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    y._mask = x._mask = m
    # Disregard any masked elements of x or y
    y = y.compressed()
    x = x.compressed().astype(float)
    # We now have unmasked arrays so can use `stats.theilslopes`
    return stats_theilslopes(y, x, alpha=alpha)
