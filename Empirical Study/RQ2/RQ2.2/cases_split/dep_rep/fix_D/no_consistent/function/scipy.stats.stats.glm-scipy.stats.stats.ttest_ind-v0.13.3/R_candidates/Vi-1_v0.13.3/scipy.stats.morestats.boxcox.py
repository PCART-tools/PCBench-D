def boxcox(x,lmbda=None,alpha=None):
    """
    Return a positive dataset transformed by a Box-Cox power transformation.

    Parameters
    ----------
    x : ndarray
        Input array.
    lmbda : {None, scalar}, optional
        If `lmbda` is not None, do the transformation for that value.

        If `lmbda` is None, find the lambda that maximizes the log-likelihood
        function and return it as the second output argument.
    alpha : {None, float}, optional
        If `alpha` is not None, return the ``100 * (1-alpha)%`` confidence
        interval for `lmbda` as the third output argument.

        If `alpha` is not None it must be between 0.0 and 1.0.

    Returns
    -------
    boxcox : ndarray
        Box-Cox power transformed array.
    maxlog : float, optional
        If the `lmbda` parameter is None, the second returned argument is
        the lambda that maximizes the log-likelihood function.
    (min_ci, max_ci) : tuple of float, optional
        If `lmbda` parameter is None and `alpha` is not None, this returned
        tuple of floats represents the minimum and maximum confidence limits
        given `alpha`.

    """
    if any(x < 0):
        raise ValueError("Data must be positive.")
    if lmbda is not None:  # single transformation
        lmbda = lmbda*(x == x)
        y = where(lmbda == 0, log(x), (x**lmbda - 1)/lmbda)
        return y

    # Otherwise find the lmbda that maximizes the log-likelihood function.
    def tempfunc(lmb, data):  # function to minimize
        return -boxcox_llf(lmb,data)
    lmax = optimize.brent(tempfunc, brack=(-2.0,2.0),args=(x,))
    y = boxcox(x, lmax)
    if alpha is None:
        return y, lmax
    # Otherwise find confidence interval
    interval = _boxcox_conf_interval(x, lmax, alpha)
    return y, lmax, interval
