def pointbiserialr(x, y):
    r"""
    Calculates a point biserial correlation coefficient and its p-value.

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

    Notes
    -----
    `pointbiserialr` uses a t-test with ``n-1`` degrees of freedom.
    It is equivalent to `pearsonr.`

    The value of the point-biserial correlation can be calculated from:

    .. math::

        r_{pb} = \frac{\overline{Y_{1}} -
                 \overline{Y_{0}}}{s_{y}}\sqrt{\frac{N_{1} N_{2}}{N (N - 1))}}

    Where :math:`Y_{0}` and :math:`Y_{1}` are means of the metric
    observations coded 0 and 1 respectively; :math:`N_{0}` and :math:`N_{1}`
    are number of observations coded 0 and 1 respectively; :math:`N` is the
    total number of observations and :math:`s_{y}` is the standard
    deviation of all the metric observations.

    A value of :math:`r_{pb}` that is significantly different from zero is
    completely equivalent to a significant difference in means between the two
    groups. Thus, an independent groups t Test with :math:`N-2` degrees of
    freedom may be used to test whether :math:`r_{pb}` is nonzero. The
    relation between the t-statistic for comparing two independent groups and
    :math:`r_{pb}` is given by:

    .. math::

        t = \sqrt{N - 2}\frac{r_{pb}}{\sqrt{1 - r^{2}_{pb}}}

    References
    ----------
    .. [1] J. Lev, "The Point Biserial Coefficient of Correlation", Ann. Math.
           Statist., Vol. 20, no.1, pp. 125-126, 1949.

    .. [2] R.F. Tate, "Correlation Between a Discrete and a Continuous
           Variable. Point-Biserial Correlation.", Ann. Math. Statist., Vol. 25,
           np. 3, pp. 603-607, 1954.

    .. [3] http://onlinelibrary.wiley.com/doi/10.1002/9781118445112.stat06227/full

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
    rpb, prob = pearsonr(x, y)
    return PointbiserialrResult(rpb, prob)
