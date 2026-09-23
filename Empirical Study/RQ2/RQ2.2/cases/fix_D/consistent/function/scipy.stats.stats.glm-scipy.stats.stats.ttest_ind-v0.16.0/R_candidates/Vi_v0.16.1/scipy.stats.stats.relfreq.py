def relfreq(a, numbins=10, defaultreallimits=None, weights=None):
    """
    Returns a relative frequency histogram, using the histogram function.

    Parameters
    ----------
    a : array_like
        Input array.
    numbins : int, optional
        The number of bins to use for the histogram. Default is 10.
    defaultreallimits : tuple (lower, upper), optional
        The lower and upper values for the range of the histogram.
        If no value is given, a range slightly larger than the range of the
        values in a is used. Specifically ``(a.min() - s, a.max() + s)``,
        where ``s = (1/2)(a.max() - a.min()) / (numbins - 1)``.
    weights : array_like, optional
        The weights for each value in `a`. Default is None, which gives each
        value a weight of 1.0

    Returns
    -------
    frequency : ndarray
        Binned values of relative frequency.
    lowerlimit : float
        Lower real limit
    binsize : float
        Width of each bin.
    extrapoints : int
        Extra points.

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.array([1, 4, 2, 1, 3, 1])
    >>> relfreqs, lowlim, binsize, extrapoints = stats.relfreq(a, numbins=4)
    >>> relfreqs
    array([ 0.5       ,  0.16666667,  0.16666667,  0.16666667])
    >>> np.sum(relfreqs)  # relative frequencies should add up to 1
    0.99999999999999989

    """
    h, l, b, e = histogram(a, numbins, defaultreallimits, weights=weights)
    h = np.array(h / float(np.array(a).shape[0]))

    return RelfreqResult(h, l, b, e)
