def hdquantiles_sd(data, prob=list([.25,.5,.75]), axis=None):
    """
    The standard error of the Harrell-Davis quantile estimates by jackknife.

    Parameters
    ----------
    data : array_like
        Data array.
    prob : sequence, optional
        Sequence of quantiles to compute.
    axis : int, optional
        Axis along which to compute the quantiles. If None, use a flattened
        array.

    Returns
    -------
    hdquantiles_sd : MaskedArray
        Standard error of the Harrell-Davis quantile estimates.

    """
    def _hdsd_1D(data,prob):
        "Computes the std error for 1D arrays."
        xsorted = np.sort(data.compressed())
        n = len(xsorted)
        #.........
        hdsd = np.empty(len(prob), float_)
        if n < 2:
            hdsd.flat = np.nan

        vv = np.arange(n) / float(n-1)
        betacdf = beta.cdf

        for (i,p) in enumerate(prob):
            _w = betacdf(vv, (n+1)*p, (n+1)*(1-p))
            w = _w[1:] - _w[:-1]
            mx_ = np.fromiter([np.dot(w,xsorted[np.r_[list(range(0,k)),
                                                      list(range(k+1,n))].astype(int_)])
                                  for k in range(n)], dtype=float_)
            mx_var = np.array(mx_.var(), copy=False, ndmin=1) * n / float(n-1)
            hdsd[i] = float(n-1) * np.sqrt(np.diag(mx_var).diagonal() / float(n))
        return hdsd
    # Initialization & checks
    data = ma.array(data, copy=False, dtype=float_)
    p = np.array(prob, copy=False, ndmin=1)
    # Computes quantiles along axis (or globally)
    if (axis is None):
        result = _hdsd_1D(data, p)
    else:
        if data.ndim > 2:
            raise ValueError("Array 'data' must be at most two dimensional, "
                             "but got data.ndim = %d" % data.ndim)
        result = ma.apply_along_axis(_hdsd_1D, axis, data, p)

    return ma.fix_invalid(result, copy=False).ravel()
