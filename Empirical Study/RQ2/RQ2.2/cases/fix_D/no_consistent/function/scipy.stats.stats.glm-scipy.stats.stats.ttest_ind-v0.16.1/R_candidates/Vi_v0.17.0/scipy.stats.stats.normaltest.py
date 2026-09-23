def normaltest(a, axis=0, nan_policy='propagate'):
    """
    Tests whether a sample differs from a normal distribution.

    This function tests the null hypothesis that a sample comes
    from a normal distribution.  It is based on D'Agostino and
    Pearson's [1]_, [2]_ test that combines skew and kurtosis to
    produce an omnibus test of normality.


    Parameters
    ----------
    a : array_like
        The array containing the data to be tested.
    axis : int or None, optional
        Axis along which to compute test. Default is 0. If None,
        compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    statistic : float or array
        ``s^2 + k^2``, where ``s`` is the z-score returned by `skewtest` and
        ``k`` is the z-score returned by `kurtosistest`.
    pvalue : float or array
       A 2-sided chi squared probability for the hypothesis test.

    References
    ----------
    .. [1] D'Agostino, R. B. (1971), "An omnibus test of normality for
           moderate and large sample size," Biometrika, 58, 341-348

    .. [2] D'Agostino, R. and Pearson, E. S. (1973), "Testing for
           departures from normality," Biometrika, 60, 613-622

    """
    a, axis = _chk_asarray(a, axis)

    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        return mstats_basic.normaltest(a, axis)

    if contains_nan and nan_policy == 'propagate':
        return NormaltestResult(np.nan, np.nan)

    s, _ = skewtest(a, axis)
    k, _ = kurtosistest(a, axis)
    k2 = s*s + k*k

    return NormaltestResult(k2, distributions.chi2.sf(k2, 2))
