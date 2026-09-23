def check_discrete_chisquare(distfn, arg, rvs, alpha, msg):
    """Perform chisquare test for random sample of a discrete distribution

    Parameters
    ----------
    distname : string
        name of distribution function
    arg : sequence
        parameters of distribution
    alpha : float
        significance level, threshold for p-value

    Returns
    -------
    result : bool
        0 if test passes, 1 if test fails

    """
    wsupp = 0.05

    # construct intervals with minimum mass `wsupp`.
    # intervals are left-half-open as in a cdf difference
    lo = max(distfn.a, -1000)
    distsupport = xrange(lo, min(distfn.b, 1000) + 1)
    last = 0
    distsupp = [lo]
    distmass = []
    for ii in distsupport:
        current = distfn.cdf(ii, *arg)
        if current - last >= wsupp - 1e-14:
            distsupp.append(ii)
            distmass.append(current - last)
            last = current
            if current > (1 - wsupp):
                break
    if distsupp[-1] < distfn.b:
        distsupp.append(distfn.b)
        distmass.append(1 - last)
    distsupp = np.array(distsupp)
    distmass = np.array(distmass)

    # convert intervals to right-half-open as required by histogram
    histsupp = distsupp + 1e-8
    histsupp[0] = distfn.a

    # find sample frequencies and perform chisquare test
    freq, hsupp = np.histogram(rvs, histsupp)
    chis, pval = stats.chisquare(np.array(freq), len(rvs)*distmass)

    npt.assert_(pval > alpha,
                'chisquare - test for %s at arg = %s with pval = %s' %
                (msg, str(arg), str(pval)))
