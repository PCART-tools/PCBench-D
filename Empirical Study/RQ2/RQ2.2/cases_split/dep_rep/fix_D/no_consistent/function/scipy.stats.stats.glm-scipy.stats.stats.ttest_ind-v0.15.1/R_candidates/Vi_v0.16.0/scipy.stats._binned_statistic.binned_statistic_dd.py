def binned_statistic_dd(sample, values, statistic='mean',
                        bins=10, range=None):
    """
    Compute a multidimensional binned statistic for a set of data.

    This is a generalization of a histogramdd function.  A histogram divides
    the space into bins, and returns the count of the number of points in
    each bin.  This function allows the computation of the sum, mean, median,
    or other statistic of the values within each bin.

    Parameters
    ----------
    sample : array_like
        Data to histogram passed as a sequence of D arrays of length N, or
        as an (N,D) array.
    values : array_like
        The values on which the statistic will be computed.  This must be
        the same shape as x.
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

    bins : sequence or int, optional
        The bin specification:

          * A sequence of arrays describing the bin edges along each dimension.
          * The number of bins for each dimension (nx, ny, ... =bins)
          * The number of bins for all dimensions (nx=ny=...=bins).

    range : sequence, optional
        A sequence of lower and upper bin edges to be used if the edges are
        not given explicitely in `bins`. Defaults to the minimum and maximum
        values along each dimension.

    Returns
    -------
    statistic : ndarray, shape(nx1, nx2, nx3,...)
        The values of the selected statistic in each two-dimensional bin
    bin_edges : list of ndarrays
        A list of D arrays describing the (nxi + 1) bin edges for each
        dimension
    binnumber : 1-D ndarray of ints
        This assigns to each observation an integer that represents the bin
        in which this observation falls. Array has the same length as values.

    See Also
    --------
    np.histogramdd, binned_statistic, binned_statistic_2d

    Notes
    -----

    .. versionadded:: 0.11.0

    """
    known_stats = ['mean', 'median', 'count', 'sum', 'std']
    if not callable(statistic) and statistic not in known_stats:
        raise ValueError('invalid statistic %r' % (statistic,))

    # This code is based on np.histogramdd
    try:
        # Sample is an ND-array.
        N, D = sample.shape
    except (AttributeError, ValueError):
        # Sample is a sequence of 1D arrays.
        sample = np.atleast_2d(sample).T
        N, D = sample.shape

    nbin = np.empty(D, int)
    edges = D * [None]
    dedges = D * [None]

    try:
        M = len(bins)
        if M != D:
            raise AttributeError('The dimension of bins must be equal '
                                 'to the dimension of the sample x.')
    except TypeError:
        bins = D * [bins]

    # Select range for each dimension
    # Used only if number of bins is given.
    if range is None:
        smin = np.atleast_1d(np.array(sample.min(0), float))
        smax = np.atleast_1d(np.array(sample.max(0), float))
    else:
        smin = np.zeros(D)
        smax = np.zeros(D)
        for i in np.arange(D):
            smin[i], smax[i] = range[i]

    # Make sure the bins have a finite width.
    for i in np.arange(len(smin)):
        if smin[i] == smax[i]:
            smin[i] = smin[i] - .5
            smax[i] = smax[i] + .5

    # Create edge arrays
    for i in np.arange(D):
        if np.isscalar(bins[i]):
            nbin[i] = bins[i] + 2  # +2 for outlier bins
            edges[i] = np.linspace(smin[i], smax[i], nbin[i] - 1)
        else:
            edges[i] = np.asarray(bins[i], float)
            nbin[i] = len(edges[i]) + 1  # +1 for outlier bins
        dedges[i] = np.diff(edges[i])

    nbin = np.asarray(nbin)

    # Compute the bin number each sample falls into.
    Ncount = {}
    for i in np.arange(D):
        Ncount[i] = np.digitize(sample[:, i], edges[i])

    # Using digitize, values that fall on an edge are put in the right bin.
    # For the rightmost bin, we want values equal to the right
    # edge to be counted in the last bin, and not as an outlier.
    for i in np.arange(D):
        # Rounding precision
        decimal = int(-np.log10(dedges[i].min())) + 6
        # Find which points are on the rightmost edge.
        on_edge = np.where(np.around(sample[:, i], decimal)
                           == np.around(edges[i][-1], decimal))[0]
        # Shift these points one bin to the left.
        Ncount[i][on_edge] -= 1

    # Compute the sample indices in the flattened statistic matrix.
    ni = nbin.argsort()
    xy = np.zeros(N, int)
    for i in np.arange(0, D - 1):
        xy += Ncount[ni[i]] * nbin[ni[i + 1:]].prod()
    xy += Ncount[ni[-1]]

    result = np.empty(nbin.prod(), float)

    if statistic == 'mean':
        result.fill(np.nan)
        flatcount = np.bincount(xy, None)
        flatsum = np.bincount(xy, values)
        a = flatcount.nonzero()
        result[a] = flatsum[a] / flatcount[a]
    elif statistic == 'std':
        result.fill(0)
        flatcount = np.bincount(xy, None)
        flatsum = np.bincount(xy, values)
        flatsum2 = np.bincount(xy, values ** 2)
        a = flatcount.nonzero()
        result[a] = np.sqrt(flatsum2[a] / flatcount[a]
                            - (flatsum[a] / flatcount[a]) ** 2)
    elif statistic == 'count':
        result.fill(0)
        flatcount = np.bincount(xy, None)
        a = np.arange(len(flatcount))
        result[a] = flatcount
    elif statistic == 'sum':
        result.fill(0)
        flatsum = np.bincount(xy, values)
        a = np.arange(len(flatsum))
        result[a] = flatsum
    elif statistic == 'median':
        result.fill(np.nan)
        for i in np.unique(xy):
            result[i] = np.median(values[xy == i])
    elif callable(statistic):
        with warnings.catch_warnings():
            # Numpy generates a warnings for mean/std/... with empty list
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            old = np.seterr(invalid='ignore')
            try:
                null = statistic([])
            except:
                null = np.nan
            np.seterr(**old)
        result.fill(null)
        for i in np.unique(xy):
            result[i] = statistic(values[xy == i])

    # Shape into a proper matrix
    result = result.reshape(np.sort(nbin))
    for i in np.arange(nbin.size):
        j = ni.argsort()[i]
        result = result.swapaxes(i, j)
        ni[i], ni[j] = ni[j], ni[i]

    # Remove outliers (indices 0 and -1 for each dimension).
    core = D * [slice(1, -1)]
    result = result[core]

    if (result.shape != nbin - 2).any():
        raise RuntimeError('Internal Shape Error')

    BinnedStatisticddResult = namedtuple('BinnedStatisticddResult',
                                         ('statistic', 'bin_edges',
                                          'binnumber'))
    return BinnedStatisticddResult(result, edges, xy)
