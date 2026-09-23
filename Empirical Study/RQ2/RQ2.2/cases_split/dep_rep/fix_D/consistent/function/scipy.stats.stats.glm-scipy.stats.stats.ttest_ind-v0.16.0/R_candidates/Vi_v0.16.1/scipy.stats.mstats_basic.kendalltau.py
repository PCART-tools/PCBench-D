def kendalltau(x, y, use_ties=True, use_missing=False):
    """
    Computes Kendall's rank correlation tau on two variables *x* and *y*.

    Parameters
    ----------
    x : sequence
        First data list (for example, time).
    y : sequence
        Second data list.
    use_ties : {True, False}, optional
        Whether ties correction should be performed.
    use_missing : {False, True}, optional
        Whether missing data should be allocated a rank of 0 (False) or the
        average rank (True)

    Returns
    -------
    correlation : float
        Kendall tau
    pvalue : float
        Approximate 2-side p-value.

    """
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.flatten(), y.flatten())
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    if m is not nomask:
        x = ma.array(x, mask=m, copy=True)
        y = ma.array(y, mask=m, copy=True)
        n -= m.sum()

    if n < 2:
        return KendalltauResult(np.nan, np.nan)

    rx = ma.masked_equal(rankdata(x, use_missing=use_missing), 0)
    ry = ma.masked_equal(rankdata(y, use_missing=use_missing), 0)
    idx = rx.argsort()
    (rx, ry) = (rx[idx], ry[idx])
    C = np.sum([((ry[i+1:] > ry[i]) * (rx[i+1:] > rx[i])).filled(0).sum()
                for i in range(len(ry)-1)], dtype=float)
    D = np.sum([((ry[i+1:] < ry[i])*(rx[i+1:] > rx[i])).filled(0).sum()
                for i in range(len(ry)-1)], dtype=float)
    if use_ties:
        xties = count_tied_groups(x)
        yties = count_tied_groups(y)
        corr_x = np.sum([v*k*(k-1) for (k,v) in iteritems(xties)], dtype=float)
        corr_y = np.sum([v*k*(k-1) for (k,v) in iteritems(yties)], dtype=float)
        denom = ma.sqrt((n*(n-1)-corr_x)/2. * (n*(n-1)-corr_y)/2.)
    else:
        denom = n*(n-1)/2.
    tau = (C-D) / denom

    var_s = n*(n-1)*(2*n+5)
    if use_ties:
        var_s -= np.sum(v*k*(k-1)*(2*k+5)*1. for (k,v) in iteritems(xties))
        var_s -= np.sum(v*k*(k-1)*(2*k+5)*1. for (k,v) in iteritems(yties))
        v1 = np.sum([v*k*(k-1) for (k, v) in iteritems(xties)], dtype=float) *\
             np.sum([v*k*(k-1) for (k, v) in iteritems(yties)], dtype=float)
        v1 /= 2.*n*(n-1)
        if n > 2:
            v2 = np.sum([v*k*(k-1)*(k-2) for (k,v) in iteritems(xties)],
                        dtype=float) * \
                 np.sum([v*k*(k-1)*(k-2) for (k,v) in iteritems(yties)],
                        dtype=float)
            v2 /= 9.*n*(n-1)*(n-2)
        else:
            v2 = 0
    else:
        v1 = v2 = 0

    var_s /= 18.
    var_s += (v1 + v2)
    z = (C-D)/np.sqrt(var_s)
    prob = special.erfc(abs(z)/np.sqrt(2))
    return KendalltauResult(tau, prob)
