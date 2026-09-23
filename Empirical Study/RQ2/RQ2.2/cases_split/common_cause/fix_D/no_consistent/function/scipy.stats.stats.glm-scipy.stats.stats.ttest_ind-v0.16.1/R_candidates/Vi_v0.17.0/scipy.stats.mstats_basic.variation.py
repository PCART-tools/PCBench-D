def variation(a, axis=0):
    """
    Computes the coefficient of variation, the ratio of the biased standard
    deviation to the mean.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or None, optional
        Axis along which to calculate the coefficient of variation. Default
        is 0. If None, compute over the whole array `a`.

    Returns
    -------
    variation : ndarray
        The calculated variation along the requested axis.

    Notes
    -----
    For more details about `variation`, see `stats.variation`.

    """
    a, axis = _chk_asarray(a, axis)
    return a.std(axis)/a.mean(axis)
