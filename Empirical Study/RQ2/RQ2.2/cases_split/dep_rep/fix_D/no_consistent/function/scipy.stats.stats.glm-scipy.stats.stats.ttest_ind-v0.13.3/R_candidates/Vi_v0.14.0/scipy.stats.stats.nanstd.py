def nanstd(x, axis=0, bias=False):
    """
    Compute the standard deviation over the given axis, ignoring nans.

    Parameters
    ----------
    x : array_like
        Input array.
    axis : int or None, optional
        Axis along which the standard deviation is computed. Default is 0.
        If None, compute over the whole array `x`.
    bias : bool, optional
        If True, the biased (normalized by N) definition is used. If False
        (default), the unbiased definition is used.

    Returns
    -------
    s : float
        The standard deviation.

    See Also
    --------
    nanmean, nanmedian

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.arange(10, dtype=float)
    >>> a[1:3] = np.nan
    >>> np.std(a)
    nan
    >>> stats.nanstd(a)
    2.9154759474226504
    >>> stats.nanstd(a.reshape(2, 5), axis=1)
    array([ 2.0817,  1.5811])
    >>> stats.nanstd(a.reshape(2, 5), axis=None)
    2.9154759474226504

    """
    x, axis = _chk_asarray(x, axis)
    x = x.copy()
    Norig = x.shape[axis]

    mask = np.isnan(x)
    Nnan = np.sum(mask, axis) * 1.0
    n = Norig - Nnan

    x[mask] = 0.0
    m1 = np.sum(x, axis) / n

    if axis:
        d = x - np.expand_dims(m1, axis)
    else:
        d = x - m1

    d *= d

    m2 = np.sum(d, axis) - m1 * m1 * Nnan

    if bias:
        m2c = m2 / n
    else:
        m2c = m2 / (n - 1.0)

    return np.sqrt(m2c)
