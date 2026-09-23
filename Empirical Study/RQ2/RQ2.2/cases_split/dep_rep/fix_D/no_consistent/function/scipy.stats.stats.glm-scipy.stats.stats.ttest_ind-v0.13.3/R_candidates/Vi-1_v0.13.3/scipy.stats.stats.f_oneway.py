def f_oneway(*args):
    """
    Performs a 1-way ANOVA.

    The one-way ANOVA tests the null hypothesis that two or more groups have
    the same population mean.  The test is applied to samples from two or
    more groups, possibly with differing sizes.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The sample measurements for each group.

    Returns
    -------
    F-value : float
        The computed F-value of the test.
    p-value : float
        The associated p-value from the F-distribution.

    Notes
    -----
    The ANOVA test has important assumptions that must be satisfied in order
    for the associated p-value to be valid.

    1. The samples are independent.
    2. Each sample is from a normally distributed population.
    3. The population standard deviations of the groups are all equal.  This
       property is known as homoscedasticity.

    If these assumptions are not true for a given set of data, it may still be
    possible to use the Kruskal-Wallis H-test (`scipy.stats.kruskal`) although
    with some loss of power.

    The algorithm is from Heiman[2], pp.394-7.


    References
    ----------
    .. [1] Lowry, Richard.  "Concepts and Applications of Inferential
           Statistics". Chapter 14.
           http://faculty.vassar.edu/lowry/ch14pt1.html

    .. [2] Heiman, G.W.  Research Methods in Statistics. 2002.

    """
    args = list(map(np.asarray, args))  # convert to an numpy array
    na = len(args)              # ANOVA on 'na' groups, each in it's own array
    alldata = np.concatenate(args)
    bign = len(alldata)
    sstot = ss(alldata) - (square_of_sums(alldata) / float(bign))
    ssbn = 0
    for a in args:
        ssbn += square_of_sums(a) / float(len(a))
    ssbn -= (square_of_sums(alldata) / float(bign))
    sswn = sstot - ssbn
    dfbn = na - 1
    dfwn = bign - na
    msb = ssbn / float(dfbn)
    msw = sswn / float(dfwn)
    f = msb / msw
    prob = fprob(dfbn, dfwn, f)
    return f, prob
