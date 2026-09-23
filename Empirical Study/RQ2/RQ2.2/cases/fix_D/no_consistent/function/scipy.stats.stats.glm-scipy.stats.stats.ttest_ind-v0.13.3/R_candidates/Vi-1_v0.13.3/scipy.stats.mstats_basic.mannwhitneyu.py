def mannwhitneyu(x,y, use_continuity=True):
    """
    Computes the Mann-Whitney statistic

    Missing values in `x` and/or `y` are discarded.

    Parameters
    ----------
    x : sequence
        Input
    y : sequence
        Input
    use_continuity : {True, False}, optional
        Whether a continuity correction (1/2.) should be taken into account.

    Returns
    -------
    u : float
        The Mann-Whitney statistics
    prob : float
        Approximate p-value assuming a normal distribution.

    """
    x = ma.asarray(x).compressed().view(ndarray)
    y = ma.asarray(y).compressed().view(ndarray)
    ranks = rankdata(np.concatenate([x,y]))
    (nx, ny) = (len(x), len(y))
    nt = nx + ny
    U = ranks[:nx].sum() - nx*(nx+1)/2.
    U = max(U, nx*ny - U)
    u = nx*ny - U
    #
    mu = (nx*ny)/2.
    sigsq = (nt**3 - nt)/12.
    ties = count_tied_groups(ranks)
    sigsq -= np.sum(v*(k**3-k) for (k,v) in iteritems(ties))/12.
    sigsq *= nx*ny/float(nt*(nt-1))
    #
    if use_continuity:
        z = (U - 1/2. - mu) / ma.sqrt(sigsq)
    else:
        z = (U - mu) / ma.sqrt(sigsq)
    prob = special.erfc(abs(z)/np.sqrt(2))
    return (u, prob)
