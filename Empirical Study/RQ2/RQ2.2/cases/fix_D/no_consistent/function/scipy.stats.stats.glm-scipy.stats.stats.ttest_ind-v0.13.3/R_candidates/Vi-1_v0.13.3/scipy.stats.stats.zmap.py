def zmap(scores, compare, axis=0, ddof=0):
    """
    Calculates the relative z-scores.

    Returns an array of z-scores, i.e., scores that are standardized to zero
    mean and unit variance, where mean and variance are calculated from the
    comparison array.

    Parameters
    ----------
    scores : array_like
        The input for which z-scores are calculated.
    compare : array_like
        The input from which the mean and standard deviation of the
        normalization are taken; assumed to have the same dimension as
        `scores`.
    axis : int or None, optional
        Axis over which mean and variance of `compare` are calculated.
        Default is 0.
    ddof : int, optional
        Degrees of freedom correction in the calculation of the
        standard deviation. Default is 0.

    Returns
    -------
    zscore : array_like
        Z-scores, in the same shape as `scores`.

    Notes
    -----
    This function preserves ndarray subclasses, and works also with
    matrices and masked arrays (it uses `asanyarray` instead of `asarray`
    for parameters).

    Examples
    --------
    >>> a = [0.5, 2.0, 2.5, 3]
    >>> b = [0, 1, 2, 3, 4]
    >>> zmap(a, b)
    array([-1.06066017,  0.        ,  0.35355339,  0.70710678])
    """
    scores, compare = map(np.asanyarray, [scores, compare])
    mns = compare.mean(axis=axis)
    sstd = compare.std(axis=axis, ddof=ddof)
    if axis and mns.ndim < compare.ndim:
        return ((scores - np.expand_dims(mns, axis=axis)) /
                 np.expand_dims(sstd,axis=axis))
    else:
        return (scores - mns) / sstd
