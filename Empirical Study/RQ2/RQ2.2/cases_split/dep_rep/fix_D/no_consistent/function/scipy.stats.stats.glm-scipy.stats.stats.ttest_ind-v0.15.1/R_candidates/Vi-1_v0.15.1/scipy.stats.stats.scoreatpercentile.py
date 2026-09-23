def scoreatpercentile(a, per, limit=(), interpolation_method='fraction',
                      axis=None):
    """
    Calculate the score at a given percentile of the input sequence.

    For example, the score at `per=50` is the median. If the desired quantile
    lies between two data points, we interpolate between them, according to
    the value of `interpolation`. If the parameter `limit` is provided, it
    should be a tuple (lower, upper) of two values.

    Parameters
    ----------
    a : array_like
        A 1-D array of values from which to extract score.
    per : array_like
        Percentile(s) at which to extract score.  Values should be in range
        [0,100].
    limit : tuple, optional
        Tuple of two scalars, the lower and upper limits within which to
        compute the percentile. Values of `a` outside
        this (closed) interval will be ignored.
    interpolation : {'fraction', 'lower', 'higher'}, optional
        This optional parameter specifies the interpolation method to use,
        when the desired quantile lies between two data points `i` and `j`

          - fraction: ``i + (j - i) * fraction`` where ``fraction`` is the
            fractional part of the index surrounded by ``i`` and ``j``.
          - lower: ``i``.
          - higher: ``j``.

    axis : int, optional
        Axis along which the percentiles are computed. The default (None)
        is to compute the median along a flattened version of the array.

    Returns
    -------
    score : float or ndarray
        Score at percentile(s).

    See Also
    --------
    percentileofscore, numpy.percentile

    Notes
    -----
    This function will become obsolete in the future.
    For Numpy 1.9 and higher, `numpy.percentile` provides all the functionality
    that `scoreatpercentile` provides.  And it's significantly faster.
    Therefore it's recommended to use `numpy.percentile` for users that have
    numpy >= 1.9.

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.arange(100)
    >>> stats.scoreatpercentile(a, 50)
    49.5

    """
    # adapted from NumPy's percentile function.  When we require numpy >= 1.8,
    # the implementation of this function can be replaced by np.percentile.
    a = np.asarray(a)
    if a.size == 0:
        # empty array, return nan(s) with shape matching `per`
        if np.isscalar(per):
            return np.nan
        else:
            return np.ones(np.asarray(per).shape, dtype=np.float64) * np.nan

    if limit:
        a = a[(limit[0] <= a) & (a <= limit[1])]

    sorted = np.sort(a, axis=axis)
    if axis is None:
        axis = 0

    return _compute_qth_percentile(sorted, per, interpolation_method, axis)
