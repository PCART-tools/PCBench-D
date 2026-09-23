def binned_statistic(x, values, statistic='mean',
                     bins=10, range=None):
    """
    Compute a binned statistic for a set of data.

    This is a generalization of a histogram function.  A histogram divides
    the space into bins, and returns the count of the number of points in
    each bin.  This function allows the computation of the sum, mean, median,
    or other statistic of the values within each bin.

    .. versionadded:: 0.11.0

    Parameters
    ----------
    x : array_like
        A sequence of values to be binned.
    values : array_like
        The values on which the statistic will be computed.  This must be
        the same shape as `x`.
    statistic : string or callable, optional
        The statistic to compute (default is 'mean').
        The following statistics are available:

          * 'mean' : compute the mean of values for points within each bin.
            Empty bins will be represented by NaN.
          * 'median' : compute the median of values for points within each
            bin. Empty bins will be represented by NaN.
          * 'count' : compute the count of points within each bin.  This is
            identical to an unweighted histogram.  `values` array is not
            referenced.
          * 'sum' : compute the sum of values for points within each bin.
            This is identical to a weighted histogram.
          * function : a user-defined function which takes a 1D array of
            values, and outputs a single numerical statistic. This function
            will be called on the values in each bin.  Empty bins will be
            represented by function([]), or NaN if this returns an error.

    bins : int or sequence of scalars, optional
        If `bins` is an int, it defines the number of equal-width
        bins in the given range (10, by default). If `bins` is a sequence,
        it defines the bin edges, including the rightmost edge, allowing
        for non-uniform bin widths.
    range : (float, float), optional
        The lower and upper range of the bins.  If not provided, range
        is simply ``(x.min(), x.max())``.  Values outside the range are
        ignored.

    Returns
    -------
    statistic : array
        The values of the selected statistic in each bin.
    bin_edges : array of dtype float
        Return the bin edges ``(length(statistic)+1)``.
    binnumber : 1-D ndarray of ints
        This assigns to each observation an integer that represents the bin
        in which this observation falls. Array has the same length as values.

    See Also
    --------
    numpy.histogram, binned_statistic_2d, binned_statistic_dd

    Notes
    -----
    All but the last (righthand-most) bin is half-open.  In other words, if
    `bins` is::

      [1, 2, 3, 4]

    then the first bin is ``[1, 2)`` (including 1, but excluding 2) and the
    second ``[2, 3)``.  The last bin, however, is ``[3, 4]``, which *includes*
    4.

    Examples
    --------
    >>> stats.binned_statistic([1, 2, 1, 2, 4], np.arange(5), statistic='mean',
    ... bins=3)
    (array([ 1.,  2.,  4.]), array([ 1.,  2.,  3.,  4.]), array([1, 2, 1, 2, 3]))

    >>> stats.binned_statistic([1, 2, 1, 2, 4], np.arange(5), statistic='mean', bins=3)
    (array([ 1.,  2.,  4.]), array([ 1.,  2.,  3.,  4.]), array([1, 2, 1, 2, 3]))

    """
    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N != 1:
        bins = [np.asarray(bins, float)]

    medians, edges, xy = binned_statistic_dd([x], values, statistic,
                                             bins, range)

    return medians, edges[0], xy
