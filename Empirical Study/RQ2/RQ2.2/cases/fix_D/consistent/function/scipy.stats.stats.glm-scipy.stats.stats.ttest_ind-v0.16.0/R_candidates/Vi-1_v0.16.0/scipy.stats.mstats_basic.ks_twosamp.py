def ks_twosamp(data1, data2, alternative="two-sided"):
    """
    Computes the Kolmogorov-Smirnov test on two samples.

    Missing values are discarded.

    Parameters
    ----------
    data1 : array_like
        First data set
    data2 : array_like
        Second data set
    alternative : {'two-sided', 'less', 'greater'}, optional
        Indicates the alternative hypothesis.  Default is 'two-sided'.

    Returns
    -------
    d : float
        Value of the Kolmogorov Smirnov test
    p : float
        Corresponding p-value.

    """
    (data1, data2) = (ma.asarray(data1), ma.asarray(data2))
    (n1, n2) = (data1.count(), data2.count())
    n = (n1*n2/float(n1+n2))
    mix = ma.concatenate((data1.compressed(), data2.compressed()))
    mixsort = mix.argsort(kind='mergesort')
    csum = np.where(mixsort < n1, 1./n1, -1./n2).cumsum()
    # Check for ties
    if len(np.unique(mix)) < (n1+n2):
        csum = csum[np.r_[np.diff(mix[mixsort]).nonzero()[0],-1]]

    alternative = str(alternative).lower()[0]
    if alternative == 't':
        d = ma.abs(csum).max()
        prob = special.kolmogorov(np.sqrt(n)*d)
    elif alternative == 'l':
        d = -csum.min()
        prob = np.exp(-2*n*d**2)
    elif alternative == 'g':
        d = csum.max()
        prob = np.exp(-2*n*d**2)
    else:
        raise ValueError("Invalid value for the alternative hypothesis: "
                         "should be in 'two-sided', 'less' or 'greater'")

    return (d, prob)
