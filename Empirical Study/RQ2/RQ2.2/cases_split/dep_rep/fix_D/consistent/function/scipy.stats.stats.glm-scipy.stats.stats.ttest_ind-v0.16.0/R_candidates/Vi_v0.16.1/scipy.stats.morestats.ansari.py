def ansari(x, y):
    """
    Perform the Ansari-Bradley test for equal scale parameters

    The Ansari-Bradley test is a non-parametric test for the equality
    of the scale parameter of the distributions from which two
    samples were drawn.

    Parameters
    ----------
    x, y : array_like
        arrays of sample data

    Returns
    -------
    statistic : float
        The Ansari-Bradley test statistic
    pvalue : float
        The p-value of the hypothesis test

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    mood : A non-parametric test for the equality of two scale parameters

    Notes
    -----
    The p-value given is exact when the sample sizes are both less than
    55 and there are no ties, otherwise a normal approximation for the
    p-value is used.

    References
    ----------
    .. [1] Sprent, Peter and N.C. Smeeton.  Applied nonparametric statistical
           methods.  3rd ed. Chapman and Hall/CRC. 2001.  Section 5.8.2.

    """
    x, y = asarray(x), asarray(y)
    n = len(x)
    m = len(y)
    if m < 1:
        raise ValueError("Not enough other observations.")
    if n < 1:
        raise ValueError("Not enough test observations.")

    N = m + n
    xy = r_[x, y]  # combine
    rank = stats.rankdata(xy)
    symrank = amin(array((rank, N - rank + 1)), 0)
    AB = sum(symrank[:n], axis=0)
    uxy = unique(xy)
    repeats = (len(uxy) != len(xy))
    exact = ((m < 55) and (n < 55) and not repeats)
    if repeats and (m < 55 or n < 55):
        warnings.warn("Ties preclude use of exact statistic.")
    if exact:
        astart, a1, ifault = statlib.gscale(n, m)
        ind = AB - astart
        total = sum(a1, axis=0)
        if ind < len(a1)/2.0:
            cind = int(ceil(ind))
            if ind == cind:
                pval = 2.0 * sum(a1[:cind+1], axis=0) / total
            else:
                pval = 2.0 * sum(a1[:cind], axis=0) / total
        else:
            find = int(floor(ind))
            if ind == floor(ind):
                pval = 2.0 * sum(a1[find:], axis=0) / total
            else:
                pval = 2.0 * sum(a1[find+1:], axis=0) / total
        return AnsariResult(AB, min(1.0, pval))

    # otherwise compute normal approximation
    if N % 2:  # N odd
        mnAB = n * (N+1.0)**2 / 4.0 / N
        varAB = n * m * (N+1.0) * (3+N**2) / (48.0 * N**2)
    else:
        mnAB = n * (N+2.0) / 4.0
        varAB = m * n * (N+2) * (N-2.0) / 48 / (N-1.0)
    if repeats:   # adjust variance estimates
        # compute sum(tj * rj**2,axis=0)
        fac = sum(symrank**2, axis=0)
        if N % 2:  # N odd
            varAB = m * n * (16*N*fac - (N+1)**4) / (16.0 * N**2 * (N-1))
        else:  # N even
            varAB = m * n * (16*fac - N*(N+2)**2) / (16.0 * N * (N-1))

    z = (AB - mnAB) / sqrt(varAB)
    pval = distributions.norm.sf(abs(z)) * 2.0
    return AnsariResult(AB, pval)
