def kurtosistest(a, axis=0):
    """
    Tests whether a dataset has normal kurtosis

    This function tests the null hypothesis that the kurtosis
    of the population from which the sample was drawn is that
    of the normal distribution: ``kurtosis = 3(n-1)/(n+1)``.

    Parameters
    ----------
    a : array
        array of the sample data
    axis : int or None
        the axis to operate along, or None to work on the whole array.
        The default is the first axis.

    Returns
    -------
    z-score : float
        The computed z-score for this test.
    p-value : float
        The 2-sided p-value for the hypothesis test

    Notes
    -----
    Valid only for n>20.  The Z-score is set to 0 for bad entries.

    """
    a, axis = _chk_asarray(a, axis)
    n = float(a.shape[axis])
    if n < 5:
        raise ValueError(
            "kurtosistest requires at least 5 observations; %i observations"
            " were given." % int(n))
    if n < 20:
        warnings.warn(
            "kurtosistest only valid for n>=20 ... continuing anyway, n=%i" %
            int(n))
    b2 = kurtosis(a, axis, fisher=False)
    E = 3.0*(n-1) / (n+1)
    varb2 = 24.0*n*(n-2)*(n-3) / ((n+1)*(n+1)*(n+3)*(n+5))
    x = (b2-E)/np.sqrt(varb2)
    sqrtbeta1 = 6.0*(n*n-5*n+2)/((n+7)*(n+9)) * np.sqrt((6.0*(n+3)*(n+5)) /
                                                       (n*(n-2)*(n-3)))
    A = 6.0 + 8.0/sqrtbeta1 * (2.0/sqrtbeta1 + np.sqrt(1+4.0/(sqrtbeta1**2)))
    term1 = 1 - 2/(9.0*A)
    denom = 1 + x*np.sqrt(2/(A-4.0))
    denom = np.where(denom < 0, 99, denom)
    term2 = np.where(denom < 0, term1, np.power((1-2.0/A)/denom,1/3.0))
    Z = (term1 - term2) / np.sqrt(2/(9.0*A))
    Z = np.where(denom == 99, 0, Z)
    if Z.ndim == 0:
        Z = Z[()]
    # JPNote: p-value sometimes larger than 1
    # zprob uses upper tail, so Z needs to be positive
    return Z, 2 * distributions.norm.sf(np.abs(Z))
