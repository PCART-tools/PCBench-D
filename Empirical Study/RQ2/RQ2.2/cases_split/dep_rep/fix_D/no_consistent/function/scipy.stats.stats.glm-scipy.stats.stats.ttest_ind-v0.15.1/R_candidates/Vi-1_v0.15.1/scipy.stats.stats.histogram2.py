def histogram2(a, bins):
    """
    Compute histogram using divisions in bins.

    Count the number of times values from array `a` fall into
    numerical ranges defined by `bins`.  Range x is given by
    bins[x] <= range_x < bins[x+1] where x =0,N and N is the
    length of the `bins` array.  The last range is given by
    bins[N] <= range_N < infinity.  Values less than bins[0] are
    not included in the histogram.

    Parameters
    ----------
    a : array_like of rank 1
        The array of values to be assigned into bins
    bins : array_like of rank 1
        Defines the ranges of values to use during histogramming.

    Returns
    -------
    histogram2 : ndarray of rank 1
        Each value represents the occurrences for a given bin (range) of
        values.

    """
    # comment: probably obsoleted by numpy.histogram()
    n = np.searchsorted(np.sort(a), bins)
    n = np.concatenate([n, [len(a)]])
    return n[1:]-n[:-1]
