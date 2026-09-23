def histogram(a, numbins=10, defaultlimits=None, weights=None, printextras=False):
    """
    Separates the range into several bins and returns the number of instances
    in each bin.

    Parameters
    ----------
    a : array_like
        Array of scores which will be put into bins.
    numbins : int, optional
        The number of bins to use for the histogram. Default is 10.
    defaultlimits : tuple (lower, upper), optional
        The lower and upper values for the range of the histogram.
        If no value is given, a range slightly larger then the range of the
        values in a is used. Specifically ``(a.min() - s, a.max() + s)``,
            where ``s = (1/2)(a.max() - a.min()) / (numbins - 1)``.
    weights : array_like, optional
        The weights for each value in `a`. Default is None, which gives each
        value a weight of 1.0
    printextras : bool, optional
        If True, the number of extra points is printed to standard output.
        Default is False.

    Returns
    -------
    histogram : ndarray
        Number of points (or sum of weights) in each bin.
    low_range : float
        Lowest value of histogram, the lower limit of the first bin.
    binsize : float
        The size of the bins (all bins have the same size).
    extrapoints : int
        The number of points outside the range of the histogram.

    See Also
    --------
    numpy.histogram

    Notes
    -----
    This histogram is based on numpy's histogram but has a larger range by
    default if default limits is not set.

    """
    a = np.ravel(a)               # flatten any >1D arrays
    if defaultlimits is None:
        # no range given, so use values in a
        data_min = a.min()
        data_max = a.max()
        # Have bins extend past min and max values slightly
        s = (data_max - data_min) / (2. * (numbins - 1.))
        defaultlimits = (data_min - s, data_max + s)
    # use numpy's histogram method to compute bins
    hist, bin_edges = np.histogram(a, bins=numbins, range=defaultlimits,
                                   weights=weights)
    # hist are not always floats, convert to keep with old output
    hist = np.array(hist, dtype=float)
    # fixed width for bins is assumed, as numpy's histogram gives
    # fixed width bins for int values for 'bins'
    binsize = bin_edges[1] - bin_edges[0]
    # calculate number of extra points
    extrapoints = len([v for v in a
                       if defaultlimits[0] > v or v > defaultlimits[1]])
    if extrapoints > 0 and printextras:
        warnings.warn("Points outside given histogram range = %s"
                      % extrapoints)
    return (hist, defaultlimits[0], binsize, extrapoints)
