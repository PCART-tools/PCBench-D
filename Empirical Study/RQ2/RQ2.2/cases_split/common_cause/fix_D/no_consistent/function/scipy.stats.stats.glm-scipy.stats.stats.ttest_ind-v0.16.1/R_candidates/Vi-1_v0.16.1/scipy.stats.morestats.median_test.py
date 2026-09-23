@setastest(False)
def median_test(*args, **kwds):
    """
    Mood's median test.

    Test that two or more samples come from populations with the same median.

    Let ``n = len(args)`` be the number of samples.  The "grand median" of
    all the data is computed, and a contingency table is formed by
    classifying the values in each sample as being above or below the grand
    median.  The contingency table, along with `correction` and `lambda_`,
    are passed to `scipy.stats.chi2_contingency` to compute the test statistic
    and p-value.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The set of samples.  There must be at least two samples.
        Each sample must be a one-dimensional sequence containing at least
        one value.  The samples are not required to have the same length.
    ties : str, optional
        Determines how values equal to the grand median are classified in
        the contingency table.  The string must be one of::

            "below":
                Values equal to the grand median are counted as "below".
            "above":
                Values equal to the grand median are counted as "above".
            "ignore":
                Values equal to the grand median are not counted.

        The default is "below".
    correction : bool, optional
        If True, *and* there are just two samples, apply Yates' correction
        for continuity when computing the test statistic associated with
        the contingency table.  Default is True.
    lambda_ : float or str, optional.
        By default, the statistic computed in this test is Pearson's
        chi-squared statistic.  `lambda_` allows a statistic from the
        Cressie-Read power divergence family to be used instead.  See
        `power_divergence` for details.
        Default is 1 (Pearson's chi-squared statistic).

    Returns
    -------
    stat : float
        The test statistic.  The statistic that is returned is determined by
        `lambda_`.  The default is Pearson's chi-squared statistic.
    p : float
        The p-value of the test.
    m : float
        The grand median.
    table : ndarray
        The contingency table.  The shape of the table is (2, n), where
        n is the number of samples.  The first row holds the counts of the
        values above the grand median, and the second row holds the counts
        of the values below the grand median.  The table allows further
        analysis with, for example, `scipy.stats.chi2_contingency`, or with
        `scipy.stats.fisher_exact` if there are two samples, without having
        to recompute the table.

    See Also
    --------
    kruskal : Compute the Kruskal-Wallis H-test for independent samples.
    mannwhitneyu : Computes the Mann-Whitney rank test on samples x and y.

    Notes
    -----
    .. versionadded:: 0.15.0

    References
    ----------
    .. [1] Mood, A. M., Introduction to the Theory of Statistics. McGraw-Hill
        (1950), pp. 394-399.
    .. [2] Zar, J. H., Biostatistical Analysis, 5th ed. Prentice Hall (2010).
        See Sections 8.12 and 10.15.

    Examples
    --------
    A biologist runs an experiment in which there are three groups of plants.
    Group 1 has 16 plants, group 2 has 15 plants, and group 3 has 17 plants.
    Each plant produces a number of seeds.  The seed counts for each group
    are::

        Group 1: 10 14 14 18 20 22 24 25 31 31 32 39 43 43 48 49
        Group 2: 28 30 31 33 34 35 36 40 44 55 57 61 91 92 99
        Group 3:  0  3  9 22 23 25 25 33 34 34 40 45 46 48 62 67 84

    The following code applies Mood's median test to these samples.

    >>> g1 = [10, 14, 14, 18, 20, 22, 24, 25, 31, 31, 32, 39, 43, 43, 48, 49]
    >>> g2 = [28, 30, 31, 33, 34, 35, 36, 40, 44, 55, 57, 61, 91, 92, 99]
    >>> g3 = [0, 3, 9, 22, 23, 25, 25, 33, 34, 34, 40, 45, 46, 48, 62, 67, 84]
    >>> from scipy.stats import median_test
    >>> stat, p, med, tbl = median_test(g1, g2, g3)

    The median is

    >>> med
    34.0

    and the contingency table is

    >>> tbl
    array([[ 5, 10,  7],
           [11,  5, 10]])

    `p` is too large to conclude that the medians are not the same:

    >>> p
    0.12609082774093244

    The "G-test" can be performed by passing ``lambda_="log-likelihood"`` to
    `median_test`.

    >>> g, p, med, tbl = median_test(g1, g2, g3, lambda_="log-likelihood")
    >>> p
    0.12224779737117837

    The median occurs several times in the data, so we'll get a different
    result if, for example, ``ties="above"`` is used:

    >>> stat, p, med, tbl = median_test(g1, g2, g3, ties="above")
    >>> p
    0.063873276069553273

    >>> tbl
    array([[ 5, 11,  9],
           [11,  4,  8]])

    This example demonstrates that if the data set is not large and there
    are values equal to the median, the p-value can be sensitive to the
    choice of `ties`.

    """
    ties = kwds.pop('ties', 'below')
    correction = kwds.pop('correction', True)
    lambda_ = kwds.pop('lambda_', None)

    if len(kwds) > 0:
        bad_kwd = kwds.keys()[0]
        raise TypeError("median_test() got an unexpected keyword "
                        "argument %r" % bad_kwd)

    if len(args) < 2:
        raise ValueError('median_test requires two or more samples.')

    ties_options = ['below', 'above', 'ignore']
    if ties not in ties_options:
        raise ValueError("invalid 'ties' option '%s'; 'ties' must be one "
                         "of: %s" % (ties, str(ties_options)[1:-1]))

    data = [np.asarray(arg) for arg in args]

    # Validate the sizes and shapes of the arguments.
    for k, d in enumerate(data):
        if d.size == 0:
            raise ValueError("Sample %d is empty. All samples must "
                             "contain at least one value." % (k + 1))
        if d.ndim != 1:
            raise ValueError("Sample %d has %d dimensions.  All "
                             "samples must be one-dimensional sequences." %
                             (k + 1, d.ndim))

    grand_median = np.median(np.concatenate(data))

    # Create the contingency table.
    table = np.zeros((2, len(data)), dtype=np.int64)
    for k, sample in enumerate(data):
        nabove = count_nonzero(sample > grand_median)
        nbelow = count_nonzero(sample < grand_median)
        nequal = sample.size - (nabove + nbelow)
        table[0, k] += nabove
        table[1, k] += nbelow
        if ties == "below":
            table[1, k] += nequal
        elif ties == "above":
            table[0, k] += nequal

    # Check that no row or column of the table is all zero.
    # Such a table can not be given to chi2_contingency, because it would have
    # a zero in the table of expected frequencies.
    rowsums = table.sum(axis=1)
    if rowsums[0] == 0:
        raise ValueError("All values are below the grand median (%r)." %
                         grand_median)
    if rowsums[1] == 0:
        raise ValueError("All values are above the grand median (%r)." %
                         grand_median)
    if ties == "ignore":
        # We already checked that each sample has at least one value, but it
        # is possible that all those values equal the grand median.  If `ties`
        # is "ignore", that would result in a column of zeros in `table`.  We
        # check for that case here.
        zero_cols = np.where((table == 0).all(axis=0))[0]
        if len(zero_cols) > 0:
            msg = ("All values in sample %d are equal to the grand "
                   "median (%r), so they are ignored, resulting in an "
                   "empty sample." % (zero_cols[0] + 1, grand_median))
            raise ValueError(msg)

    stat, p, dof, expected = chi2_contingency(table, lambda_=lambda_,
                                              correction=correction)
    return stat, p, grand_median, table
