def mood(x, y, axis=0):
    """
    Perform Mood's test for equal scale parameters.

    Mood's two-sample test for scale parameters is a non-parametric
    test for the null hypothesis that two samples are drawn from the
    same distribution with the same scale parameter.

    Parameters
    ----------
    x, y : array_like
        Arrays of sample data.
    axis: int, optional
        The axis along which the samples are tested.  `x` and `y` can be of
        different length along `axis`.
        If `axis` is None, `x` and `y` are flattened and the test is done on
        all values in the flattened arrays.

    Returns
    -------
    z : scalar or ndarray
        The z-score for the hypothesis test.  For 1-D inputs a scalar is
        returned.
    p-value : scalar ndarray
        The p-value for the hypothesis test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    ansari : A non-parametric test for the equality of 2 variances
    bartlett : A parametric test for equality of k variances in normal samples
    levene : A parametric test for equality of k variances

    Notes
    -----
    The data are assumed to be drawn from probability distributions ``f(x)``
    and ``f(x/s) / s`` respectively, for some probability density function f.
    The null hypothesis is that ``s == 1``.

    For multi-dimensional arrays, if the inputs are of shapes
    ``(n0, n1, n2, n3)``  and ``(n0, m1, n2, n3)``, then if ``axis=1``, the
    resulting z and p values will have shape ``(n0, n2, n3)``.  Note that
    ``n1`` and ``m1`` don't have to be equal, but the other dimensions do.

    Examples
    --------
    >>> from scipy import stats
    >>> x2 = np.random.randn(2, 45, 6, 7)
    >>> x1 = np.random.randn(2, 30, 6, 7)
    >>> z, p = stats.mood(x1, x2, axis=1)
    >>> p.shape
    (2, 6, 7)

    Find the number of points where the difference in scale is not significant:

    >>> (p > 0.1).sum()
    74

    Perform the test with different scales:

    >>> x1 = np.random.randn(2, 30)
    >>> x2 = np.random.randn(2, 35) * 10.0
    >>> stats.mood(x1, x2, axis=1)
    (array([-5.84332354, -5.6840814 ]), array([5.11694980e-09, 1.31517628e-08]))

    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if axis is None:
        x = x.flatten()
        y = y.flatten()
        axis = 0

    # Determine shape of the result arrays
    res_shape = tuple([x.shape[ax] for ax in range(len(x.shape)) if ax != axis])
    if not (res_shape == tuple([y.shape[ax] for ax in range(len(y.shape)) if
                                ax != axis])):
        raise ValueError("Dimensions of x and y on all axes except `axis` "
                         "should match")

    n = x.shape[axis]
    m = y.shape[axis]
    N = m + n
    if N < 3:
        raise ValueError("Not enough observations.")

    xy = np.concatenate((x, y), axis=axis)
    if axis != 0:
        xy = np.rollaxis(xy, axis)

    xy = xy.reshape(xy.shape[0], -1)

    # Generalized to the n-dimensional case by adding the axis argument, and
    # using for loops, since rankdata is not vectorized.  For improving
    # performance consider vectorizing rankdata function.
    all_ranks = np.zeros_like(xy)
    for j in range(xy.shape[1]):
        all_ranks[:, j] = stats.rankdata(xy[:, j])

    Ri = all_ranks[:n]
    M = sum((Ri - (N + 1.0) / 2) ** 2, axis=0)
    # Approx stat.
    mnM = n * (N * N - 1.0) / 12
    varM = m * n * (N + 1.0) * (N + 2) * (N - 2) / 180
    z = (M - mnM) / sqrt(varM)

    # sf for right tail, cdf for left tail.  Factor 2 for two-sidedness
    z_pos = z > 0
    pval = np.zeros_like(z)
    pval[z_pos] = 2 * distributions.norm.sf(z[z_pos])
    pval[~z_pos] = 2 * distributions.norm.cdf(z[~z_pos])

    if res_shape == ():
        # Return scalars, not 0-D arrays
        z = z[0]
        pval = pval[0]
    else:
        z.shape = res_shape
        pval.shape = res_shape

    return z, pval
