@np.deprecate(message="Deprecated in scipy 0.13.0 - use numpy.median instead.")
def cmedian(a, numbins=1000):
    """
    Returns the computed median value of an array.

    All of the values in the input array are used. The input array is first
    histogrammed using `numbins` bins. The bin containing the median is
    selected by searching for the halfway point in the cumulative histogram.
    The median value is then computed by linearly interpolating across that
    bin.

    Parameters
    ----------
    a : array_like
        Input array.
    numbins : int
        The number of bins used to histogram the data. More bins give greater
        accuracy to the approximation of the median.

    Returns
    -------
    cmedian : float
        An approximation of the median.

    References
    ----------
    [CRCProbStat2000]_ Section 2.2.6

    .. [CRCProbStat2000] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.

    """
    # TODO: numpy.median() always seems to be a better choice.
    # A better version of this function would take already-histogrammed data
    # and compute the median from that.
    a = np.ravel(a)
    n = float(len(a))

    # We will emulate the (fixed!) bounds selection scheme used by
    # scipy.stats.histogram(), but use numpy.histogram() since it is faster.
    amin = a.min()
    amax = a.max()
    estbinwidth = (amax - amin)/float(numbins - 1)
    binsize = (amax - amin + estbinwidth) / float(numbins)
    (hist, bins) = np.histogram(a, numbins,
        range=(amin-binsize*0.5, amax+binsize*0.5))
    binsize = bins[1] - bins[0]
    cumhist = np.cumsum(hist)           # make cumulative histogram
    cfbin = np.searchsorted(cumhist, n/2.0)
    LRL = bins[cfbin]      # get lower read limit of that bin
    if cfbin == 0:
        cfbelow = 0.0
    else:
        cfbelow = cumhist[cfbin-1]       # cum. freq. below bin
    freq = hist[cfbin]                  # frequency IN the 50%ile bin
    median = LRL + ((n/2.0-cfbelow)/float(freq))*binsize  # MEDIAN
    return median
