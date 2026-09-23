def probplot(x, sparams=(), dist='norm', fit=True, plot=None):
    """
    Calculate quantiles for a probability plot of sample data against a
    specified theoretical distribution.

    `probplot` optionally calculates a best-fit line for the data and plots the
    results using Matplotlib or a given plot function.

    Parameters
    ----------
    x : array_like
        Sample/response data from which `probplot` creates the plot.
    sparams : tuple, optional
        Distribution-specific shape parameters (location(s) and scale(s)).
    dist : str, optional
        Distribution function name. The default is 'norm' for a normal
        probability plot.
    fit : bool, optional
        Fit a least-squares regression (best-fit) line to the sample data if
        True (default).
    plot : object, optional
        If given, plots the quantiles and least squares fit.
        `plot` is an object with methods "plot", "title", "xlabel", "ylabel"
        and "text". The matplotlib.pyplot module or a Matplotlib axes object
        can be used, or a custom object with the same methods.
        By default, no plot is created.

    Returns
    -------
    (osm, osr) : tuple of ndarrays
        Tuple of theoretical quantiles (osm, or order statistic medians) and
        ordered responses (osr).
    (slope, intercept, r) : tuple of floats, optional
        Tuple  containing the result of the least-squares fit, if that is
        performed by `probplot`. `r` is the square root of the coefficient of
        determination.  If ``fit=False`` and ``plot=None``, this tuple is not
        returned.

    Notes
    -----
    Even if `plot` is given, the figure is not shown or saved by `probplot`;
    ``plot.show()`` or ``plot.savefig('figname.png')`` should be used after
    calling `probplot`.

    Examples
    --------
    >>> import scipy.stats as stats
    >>> nsample = 100
    >>> np.random.seed(7654321)

    A t distribution with small degrees of freedom:

    >>> ax1 = plt.subplot(221)
    >>> x = stats.t.rvs(3, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    A t distribution with larger degrees of freedom:

    >>> ax2 = plt.subplot(222)
    >>> x = stats.t.rvs(25, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    A mixture of 2 normal distributions with broadcasting:

    >>> ax3 = plt.subplot(223)
    >>> x = stats.norm.rvs(loc=[0,5], scale=[1,1.5],
    ...                    size=(nsample/2.,2)).ravel()
    >>> res = stats.probplot(x, plot=plt)

    A standard normal distribution:

    >>> ax4 = plt.subplot(224)
    >>> x = stats.norm.rvs(loc=0, scale=1, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    """
    N = len(x)
    Ui = zeros(N) * 1.0
    Ui[-1] = 0.5**(1.0 / N)
    Ui[0] = 1 - Ui[-1]
    i = arange(2, N)
    Ui[1:-1] = (i - 0.3175) / (N + 0.365)
    try:
        ppf_func = eval('distributions.%s.ppf' % dist)
    except AttributeError:
        raise ValueError("%s is not a valid distribution with a ppf." % dist)
    if sparams is None:
        sparams = ()
    if isscalar(sparams):
        sparams = (sparams,)
    if not isinstance(sparams, tuple):
        sparams = tuple(sparams)
    """
    res = inspect.getargspec(ppf_func)
    if not ('loc' == res[0][-2] and 'scale' == res[0][-1] and \
            0.0==res[-1][-2] and 1.0==res[-1][-1]):
        raise ValueError("Function has does not have default location "
              "and scale parameters\n  that are 0.0 and 1.0 respectively.")
    if (len(sparams) < len(res[0])-len(res[-1])-1) or \
       (len(sparams) > len(res[0])-3):
        raise ValueError("Incorrect number of shape parameters.")
    """
    osm = ppf_func(Ui, *sparams)
    osr = sort(x)
    if fit or (plot is not None):
        # perform a linear fit.
        slope, intercept, r, prob, sterrest = stats.linregress(osm, osr)
    if plot is not None:
        plot.plot(osm, osr, 'o', osm, slope*osm + intercept)
        plot.title('Probability Plot')
        plot.xlabel('Quantiles')
        plot.ylabel('Ordered Values')

        xmin = amin(osm)
        xmax = amax(osm)
        ymin = amin(x)
        ymax = amax(x)
        posx = xmin + 0.70 * (xmax - xmin)
        posy = ymin + 0.01 * (ymax - ymin)
        plot.text(posx, posy, "r^2=%1.4f" % r)
    if fit:
        return (osm, osr), (slope, intercept, r)
    else:
        return osm, osr
