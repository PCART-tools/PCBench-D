def nanmean(x, axis=0):
    """
    Compute the mean over the given axis ignoring nans.

    Parameters
    ----------
    x : ndarray
        Input array.
    axis : int, optional
        Axis along which the mean is computed. Default is 0, i.e. the
        first axis.

    Returns
    -------
    m : float
        The mean of `x`, ignoring nans.

    See Also
    --------
    nanstd, nanmedian

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.linspace(0, 4, 3)
    >>> a
    array([ 0.,  2.,  4.])
    >>> a[-1] = np.nan
    >>> stats.nanmean(a)
    1.0

    """
    x, axis = _chk_asarray(x,axis)
    x = x.copy()
    Norig = x.shape[axis]
    factor = 1.0-np.sum(np.isnan(x),axis)*1.0/Norig

    x[np.isnan(x)] = 0
    return np.mean(x,axis)/factor
