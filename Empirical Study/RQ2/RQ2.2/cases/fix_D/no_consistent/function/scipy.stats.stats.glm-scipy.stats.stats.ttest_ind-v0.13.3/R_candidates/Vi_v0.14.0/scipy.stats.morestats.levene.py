def levene(*args,**kwds):
    """
    Perform Levene test for equal variances.

    The Levene test tests the null hypothesis that all input samples
    are from populations with equal variances.  Levene's test is an
    alternative to Bartlett's test `bartlett` in the case where
    there are significant deviations from normality.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The sample data, possibly with different lengths
    center : {'mean', 'median', 'trimmed'}, optional
        Which function of the data to use in the test.  The default
        is 'median'.
    proportiontocut : float, optional
        When `center` is 'trimmed', this gives the proportion of data points
        to cut from each end. (See `scipy.stats.trim_mean`.)
        Default is 0.05.

    Returns
    -------
    W : float
        The test statistic.
    p-value : float
        The p-value for the test.

    Notes
    -----
    Three variations of Levene's test are possible.  The possibilities
    and their recommended usages are:

      * 'median' : Recommended for skewed (non-normal) distributions>
      * 'mean' : Recommended for symmetric, moderate-tailed distributions.
      * 'trimmed' : Recommended for heavy-tailed distributions.

    References
    ----------
    .. [1]  http://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm
    .. [2]   Levene, H. (1960). In Contributions to Probability and Statistics:
               Essays in Honor of Harold Hotelling, I. Olkin et al. eds.,
               Stanford University Press, pp. 278-292.
    .. [3]  Brown, M. B. and Forsythe, A. B. (1974), Journal of the American
              Statistical Association, 69, 364-367

    """
    # Handle keyword arguments.
    center = 'median'
    proportiontocut = 0.05
    for kw, value in kwds.items():
        if kw not in ['center', 'proportiontocut']:
            raise TypeError("levene() got an unexpected keyword argument '%s'" % kw)
        if kw == 'center':
            center = value
        else:
            proportiontocut = value

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = zeros(k)
    Yci = zeros(k,'d')

    if not center in ['mean','median','trimmed']:
        raise ValueError("Keyword argument <center> must be 'mean', 'median'"
              + "or 'trimmed'.")

    if center == 'median':
        func = lambda x: np.median(x, axis=0)
    elif center == 'mean':
        func = lambda x: np.mean(x, axis=0)
    else:  # center == 'trimmed'
        args = tuple(stats.trimboth(np.sort(arg), proportiontocut) for arg in args)
        func = lambda x: np.mean(x, axis=0)

    for j in range(k):
        Ni[j] = len(args[j])
        Yci[j] = func(args[j])
    Ntot = sum(Ni,axis=0)

    # compute Zij's
    Zij = [None]*k
    for i in range(k):
        Zij[i] = abs(asarray(args[i])-Yci[i])
    # compute Zbari
    Zbari = zeros(k,'d')
    Zbar = 0.0
    for i in range(k):
        Zbari[i] = np.mean(Zij[i], axis=0)
        Zbar += Zbari[i]*Ni[i]
    Zbar /= Ntot

    numer = (Ntot-k)*sum(Ni*(Zbari-Zbar)**2,axis=0)

    # compute denom_variance
    dvar = 0.0
    for i in range(k):
        dvar += sum((Zij[i]-Zbari[i])**2,axis=0)

    denom = (k-1.0)*dvar

    W = numer / denom
    pval = distributions.f.sf(W,k-1,Ntot-k)  # 1 - cdf
    return W, pval
