def cumfreq(a, numbins=10, defaultreallimits=None, weights=None):
    """
    Returns a cumulative frequency histogram, using the histogram function.

    Parameters
    ----------
    a : array_like
        Input array.
    numbins : int, optional
        The number of bins to use for the histogram. Default is 10.
    defaultreallimits : tuple (lower, upper), optional
        The lower and upper values for the range of the histogram.
        If no value is given, a range slightly larger than the range of the
        values in `a` is used. Specifically ``(a.min() - s, a.max() + s)``,
        where ``s = (1/2)(a.max() - a.min()) / (numbins - 1)``.
    weights : array_like, optional
        The weights for each value in `a`. Default is None, which gives each
        value a weight of 1.0

    Returns
    -------
    cumcount : ndarray
        Binned values of cumulative frequency.
    lowerlimit : float
        Lower real limit
    binsize : float
        Width of each bin.
    extrapoints : int
        Extra points.

    Examples
    --------
    >>> from scipy import stats
    >>> x = [1, 4, 2, 1, 3, 1]
    >>> cumfreqs, lowlim, binsize, extrapoints = stats.cumfreq(x, numbins=4)
    >>> cumfreqs
    array([ 3.,  4.,  5.,  6.])
    >>> cumfreqs, lowlim, binsize, extrapoints = \
    ...     stats.cumfreq(x, numbins=4, defaultreallimits=(1.5, 5))
    >>> cumfreqs
    array([ 1.,  2.,  3.,  3.])
    >>> extrapoints
    3

    """
    h, l, b, e = histogram(a, numbins, defaultreallimits, weights=weights)
    cumhist = np.cumsum(h * 1, axis=0)

    CumfreqResult = namedtuple('CumfreqResult', ('cumcount', 'lowerlimit',
                                                 'binsize', 'extrapoints'))
    return CumfreqResult(cumhist, l, b, e)
