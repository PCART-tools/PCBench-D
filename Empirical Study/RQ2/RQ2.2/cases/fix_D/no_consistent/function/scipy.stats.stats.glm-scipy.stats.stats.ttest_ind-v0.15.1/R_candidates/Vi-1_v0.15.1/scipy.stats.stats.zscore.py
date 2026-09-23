def zscore(a, axis=0, ddof=0):
    """
    Calculates the z score of each value in the sample, relative to the sample
    mean and standard deviation.

    Parameters
    ----------
    a : array_like
        An array like object containing the sample data.
    axis : int or None, optional
        If `axis` is equal to None, the array is first raveled. If `axis` is
        an integer, this is the axis over which to operate. Default is 0.
    ddof : int, optional
        Degrees of freedom correction in the calculation of the
        standard deviation. Default is 0.

    Returns
    -------
    zscore : array_like
        The z-scores, standardized by mean and standard deviation of input
        array `a`.

    Notes
    -----
    This function preserves ndarray subclasses, and works also with
    matrices and masked arrays (it uses `asanyarray` instead of `asarray`
    for parameters).

    Examples
    --------
    >>> a = np.array([ 0.7972,  0.0767,  0.4383,  0.7866,  0.8091,  0.1954,
                       0.6307, 0.6599,  0.1065,  0.0508])
    >>> from scipy import stats
    >>> stats.zscore(a)
    array([ 1.1273, -1.247 , -0.0552,  1.0923,  1.1664, -0.8559,  0.5786,
            0.6748, -1.1488, -1.3324])

    Computing along a specified axis, using n-1 degrees of freedom (``ddof=1``)
    to calculate the standard deviation:

    >>> b = np.array([[ 0.3148,  0.0478,  0.6243,  0.4608],
                      [ 0.7149,  0.0775,  0.6072,  0.9656],
                      [ 0.6341,  0.1403,  0.9759,  0.4064],
                      [ 0.5918,  0.6948,  0.904 ,  0.3721],
                      [ 0.0921,  0.2481,  0.1188,  0.1366]])
    >>> stats.zscore(b, axis=1, ddof=1)
    array([[-0.19264823, -1.28415119,  1.07259584,  0.40420358],
           [ 0.33048416, -1.37380874,  0.04251374,  1.00081084],
           [ 0.26796377, -1.12598418,  1.23283094, -0.37481053],
           [-0.22095197,  0.24468594,  1.19042819, -1.21416216],
           [-0.82780366,  1.4457416 , -0.43867764, -0.1792603 ]])
    """
    a = np.asanyarray(a)
    mns = a.mean(axis=axis)
    sstd = a.std(axis=axis, ddof=ddof)
    if axis and mns.ndim < a.ndim:
        return ((a - np.expand_dims(mns, axis=axis)) /
                 np.expand_dims(sstd,axis=axis))
    else:
        return (a - mns) / sstd
