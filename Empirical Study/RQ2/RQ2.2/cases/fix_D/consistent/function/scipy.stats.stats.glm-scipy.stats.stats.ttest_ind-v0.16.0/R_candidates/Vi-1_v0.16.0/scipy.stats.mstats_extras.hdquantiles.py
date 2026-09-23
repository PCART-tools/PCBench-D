def hdquantiles(data, prob=list([.25,.5,.75]), axis=None, var=False,):
    """
    Computes quantile estimates with the Harrell-Davis method.

    The quantile estimates are calculated as a weighted linear combination
    of order statistics.

    Parameters
    ----------
    data : array_like
        Data array.
    prob : sequence, optional
        Sequence of quantiles to compute.
    axis : int or None, optional
        Axis along which to compute the quantiles. If None, use a flattened
        array.
    var : bool, optional
        Whether to return the variance of the estimate.

    Returns
    -------
    hdquantiles : MaskedArray
        A (p,) array of quantiles (if `var` is False), or a (2,p) array of
        quantiles and variances (if `var` is True), where ``p`` is the
        number of quantiles.

    """
    def _hd_1D(data,prob,var):
        "Computes the HD quantiles for a 1D array. Returns nan for invalid data."
        xsorted = np.squeeze(np.sort(data.compressed().view(ndarray)))
        # Don't use length here, in case we have a numpy scalar
        n = xsorted.size

        hd = np.empty((2,len(prob)), float_)
        if n < 2:
            hd.flat = np.nan
            if var:
                return hd
            return hd[0]

        v = np.arange(n+1) / float(n)
        betacdf = beta.cdf
        for (i,p) in enumerate(prob):
            _w = betacdf(v, (n+1)*p, (n+1)*(1-p))
            w = _w[1:] - _w[:-1]
            hd_mean = np.dot(w, xsorted)
            hd[0,i] = hd_mean
            #
            hd[1,i] = np.dot(w, (xsorted-hd_mean)**2)
            #
        hd[0, prob == 0] = xsorted[0]
        hd[0, prob == 1] = xsorted[-1]
        if var:
            hd[1, prob == 0] = hd[1, prob == 1] = np.nan
            return hd
        return hd[0]
    # Initialization & checks
    data = ma.array(data, copy=False, dtype=float_)
    p = np.array(prob, copy=False, ndmin=1)
    # Computes quantiles along axis (or globally)
    if (axis is None) or (data.ndim == 1):
        result = _hd_1D(data, p, var)
    else:
        if data.ndim > 2:
            raise ValueError("Array 'data' must be at most two dimensional, "
                             "but got data.ndim = %d" % data.ndim)
        result = ma.apply_along_axis(_hd_1D, axis, data, p, var)

    return ma.fix_invalid(result, copy=False)
