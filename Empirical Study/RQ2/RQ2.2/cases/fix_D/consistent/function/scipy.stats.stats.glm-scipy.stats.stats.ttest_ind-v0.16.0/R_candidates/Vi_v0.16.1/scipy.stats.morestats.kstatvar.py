def kstatvar(data, n=2):
    """
    Returns an unbiased estimator of the variance of the k-statistic.

    See `kstat` for more details of the k-statistic.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2}, optional
        Default is equal to 2.

    Returns
    -------
    kstatvar : float
        The nth k-statistic variance.

    See Also
    --------
    kstat

    """
    data = ravel(data)
    N = len(data)
    if n == 1:
        return kstat(data, n=2) * 1.0/N
    elif n == 2:
        k2 = kstat(data, n=2)
        k4 = kstat(data, n=4)
        return (2*N*k2**2 + (N-1)*k4) / (N*(N+1))
    else:
        raise ValueError("Only n=1 or n=2 supported.")
