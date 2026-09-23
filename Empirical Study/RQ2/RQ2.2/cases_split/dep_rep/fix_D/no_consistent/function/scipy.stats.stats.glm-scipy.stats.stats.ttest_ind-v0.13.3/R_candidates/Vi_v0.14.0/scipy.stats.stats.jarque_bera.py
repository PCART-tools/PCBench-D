def jarque_bera(x):
    """
    Perform the Jarque-Bera goodness of fit test on sample data.

    The Jarque-Bera test tests whether the sample data has the skewness and
    kurtosis matching a normal distribution.

    Note that this test only works for a large enough number of data samples
    (>2000) as the test statistic asymptotically has a Chi-squared distribution
    with 2 degrees of freedom.

    Parameters
    ----------
    x : array_like
        Observations of a random variable.

    Returns
    -------
    jb_value : float
        The test statistic.
    p : float
        The p-value for the hypothesis test.

    References
    ----------
    .. [1] Jarque, C. and Bera, A. (1980) "Efficient tests for normality,
           homoscedasticity and serial independence of regression residuals",
           6 Econometric Letters 255-259.

    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(987654321)
    >>> x = np.random.normal(0, 1, 100000)
    >>> y = np.random.rayleigh(1, 100000)
    >>> stats.jarque_bera(x)
    (4.7165707989581342, 0.09458225503041906)
    >>> stats.jarque_bera(y)
    (6713.7098548143422, 0.0)

    """
    x = np.asarray(x)
    n = float(x.size)
    if n == 0:
        raise ValueError('At least one observation is required.')

    mu = x.mean()
    diffx = x - mu
    skewness = (1 / n * np.sum(diffx**3)) / (1 / n * np.sum(diffx**2))**(3 / 2.)
    kurtosis = (1 / n * np.sum(diffx**4)) / (1 / n * np.sum(diffx**2))**2
    jb_value = n / 6 * (skewness**2 + (kurtosis - 3)**2 / 4)
    p = 1 - distributions.chi2.cdf(jb_value, 2)

    return jb_value, p
