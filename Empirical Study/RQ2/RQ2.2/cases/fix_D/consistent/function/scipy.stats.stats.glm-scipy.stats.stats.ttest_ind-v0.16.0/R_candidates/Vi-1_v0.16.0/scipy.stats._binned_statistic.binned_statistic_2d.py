def binned_statistic_2d(x, y, values, statistic='mean',
                        bins=10, range=None):
    """
    Compute a bidimensional binned statistic for a set of data.

    This is a generalization of a histogram2d function.  A histogram divides
    the space into bins, and returns the count of the number of points in
    each bin.  This function allows the computation of the sum, mean, median,
    or other statistic of the values within each bin.

    Parameters
    ----------
    x : (N,) array_like
        A sequence of values to be binned along the first dimension.
    y : (M,) array_like
        A sequence of values to be binned along the second dimension.
    values : (N,) array_like
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

    bins : int or [int, int] or array_like or [array, array], optional
        The bin specification:

          * the number of bins for the two dimensions (nx=ny=bins),
          * the number of bins in each dimension (nx, ny = bins),
          * the bin edges for the two dimensions (x_edges = y_edges = bins),
          * the bin edges in each dimension (x_edges, y_edges = bins).

    range : (2,2) array_like, optional
        The leftmost and rightmost edges of the bins along each dimension
        (if not specified explicitly in the `bins` parameters):
        [[xmin, xmax], [ymin, ymax]]. All values outside of this range will be
        considered outliers and not tallied in the histogram.

    Returns
    -------
    statistic : (nx, ny) ndarray
        The values of the selected statistic in each two-dimensional bin
    x_edges : (nx + 1) ndarray
        The bin edges along the first dimension.
    y_edges : (ny + 1) ndarray
        The bin edges along the second dimension.
    binnumber : 1-D ndarray of ints
        This assigns to each observation an integer that represents the bin
        in which this observation falls. Array has the same length as `values`.

    See Also
    --------
    numpy.histogram2d, binned_statistic, binned_statistic_dd

    Notes
    -----

    .. versionadded:: 0.11.0

    """

    # This code is based on np.histogram2d
    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N != 1 and N != 2:
        xedges = yedges = np.asarray(bins, float)
        bins = [xedges, yedges]

    medians, edges, xy = binned_statistic_dd([x, y], values, statistic,
                                             bins, range)

    BinnedStatistic2dResult = namedtuple('BinnedStatistic2dResult',
                                         ('statistic', 'x_edge', 'y_edge',
                                          'binnumber'))
    return BinnedStatistic2dResult(medians, edges[0], edges[1], xy)
