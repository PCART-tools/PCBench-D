def moment(a, moment=1, axis=0, nan_policy='propagate'):
    r"""
    Calculates the nth moment about the mean for a sample.

    A moment is a specific quantitative measure of the shape of a set of points.
    It is often used to calculate coefficients of skewness and kurtosis due
    to its close relationship with them.


    Parameters
    ----------
    a : array_like
       data
    moment : int or array_like of ints, optional
       order of central moment that is returned. Default is 1.
    axis : int or None, optional
       Axis along which the central moment is computed. Default is 0.
       If None, compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    n-th central moment : ndarray or float
       The appropriate moment along the given axis or over all values if axis
       is None. The denominator for the moment calculation is the number of
       observations, no degrees of freedom correction is done.

    See also
    --------
    kurtosis, skew, describe

    Notes
    -----
    The k-th central moment of a data sample is:

    .. math::

        m_k = \frac{1}{n} \sum_{i = 1}^n (x_i - \bar{x})^k

    Where n is the number of samples and x-bar is the mean. This function uses
    exponentiation by squares [1]_ for efficiency.

    References
    ----------
    .. [1] http://eli.thegreenplace.net/2009/03/21/efficient-integer-exponentiation-algorithms
    """
    a, axis = _chk_asarray(a, axis)

    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        return mstats_basic.moment(a, moment, axis)

    if contains_nan and nan_policy == 'propagate':
        return np.nan

    if a.size == 0:
        # empty array, return nan(s) with shape matching `moment`
        if np.isscalar(moment):
            return np.nan
        else:
            return np.ones(np.asarray(moment).shape, dtype=np.float64) * np.nan

    # for array_like moment input, return a value for each.
    if not np.isscalar(moment):
        mmnt = [_moment(a, i, axis) for i in moment]
        return np.array(mmnt)
    else:
        return _moment(a, moment, axis)
