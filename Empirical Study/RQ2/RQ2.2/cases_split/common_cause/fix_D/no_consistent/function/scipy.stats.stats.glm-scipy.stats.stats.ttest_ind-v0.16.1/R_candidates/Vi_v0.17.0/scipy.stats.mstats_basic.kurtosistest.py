def kurtosistest(a, axis=0):
    """
    Tests whether a dataset has normal kurtosis

    Parameters
    ----------
    a : array
        array of the sample data
    axis : int or None, optional
       Axis along which to compute test. Default is 0. If None,
       compute over the whole array `a`.

    Returns
    -------
    statistic : float
        The computed z-score for this test.
    pvalue : float
        The 2-sided p-value for the hypothesis test

    Notes
    -----
    For more details about `kurtosistest`, see `stats.kurtosistest`.

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    if np.min(n) < 5:
        raise ValueError(
            "kurtosistest requires at least 5 observations; %i observations"
            " were given." % np.min(n))
    if np.min(n) < 20:
        warnings.warn(
            "kurtosistest only valid for n>=20 ... continuing anyway, n=%i" %
            np.min(n))

    b2 = kurtosis(a, axis, fisher=False)
    E = 3.0*(n-1) / (n+1)
    varb2 = 24.0*n*(n-2.)*(n-3) / ((n+1)*(n+1.)*(n+3)*(n+5))
    x = (b2-E)/ma.sqrt(varb2)
    sqrtbeta1 = 6.0*(n*n-5*n+2)/((n+7)*(n+9)) * np.sqrt((6.0*(n+3)*(n+5)) /
                                                        (n*(n-2)*(n-3)))
    A = 6.0 + 8.0/sqrtbeta1 * (2.0/sqrtbeta1 + np.sqrt(1+4.0/(sqrtbeta1**2)))
    term1 = 1 - 2./(9.0*A)
    denom = 1 + x*ma.sqrt(2/(A-4.0))
    if np.ma.isMaskedArray(denom):
        # For multi-dimensional array input
        denom[denom < 0] = masked
    elif denom < 0:
        denom = masked

    term2 = ma.power((1-2.0/A)/denom,1/3.0)
    Z = (term1 - term2) / np.sqrt(2/(9.0*A))

    return KurtosistestResult(Z, 2 * distributions.norm.sf(np.abs(Z)))
