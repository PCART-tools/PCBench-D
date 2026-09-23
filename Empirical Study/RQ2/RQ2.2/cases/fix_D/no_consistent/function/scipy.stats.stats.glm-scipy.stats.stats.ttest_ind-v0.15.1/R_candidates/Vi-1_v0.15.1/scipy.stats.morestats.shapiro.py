def shapiro(x, a=None, reta=False):
    """
    Perform the Shapiro-Wilk test for normality.

    The Shapiro-Wilk test tests the null hypothesis that the
    data was drawn from a normal distribution.

    Parameters
    ----------
    x : array_like
        Array of sample data.
    a : array_like, optional
        Array of internal parameters used in the calculation.  If these
        are not given, they will be computed internally.  If x has length
        n, then a must have length n/2.
    reta : bool, optional
        Whether or not to return the internally computed a values.  The
        default is False.

    Returns
    -------
    W : float
        The test statistic.
    p-value : float
        The p-value for the hypothesis test.
    a : array_like, optional
        If `reta` is True, then these are the internally computed "a"
        values that may be passed into this function on future calls.

    See Also
    --------
    anderson : The Anderson-Darling test for normality

    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm

    """
    N = len(x)
    if N < 3:
        raise ValueError("Data must be at least length 3.")
    if a is None:
        a = zeros(N,'f')
        init = 0
    else:
        if len(a) != N//2:
            raise ValueError("len(a) must equal len(x)/2")
        init = 1
    y = sort(x)
    a, w, pw, ifault = statlib.swilk(y, a[:N//2], init)
    if ifault not in [0,2]:
        warnings.warn(str(ifault))
    if N > 5000:
        warnings.warn("p-value may not be accurate for N > 5000.")
    if reta:
        return w, pw, a
    else:
        return w, pw
