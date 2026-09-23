def f_oneway(*args):
    """
    Performs a 1-way ANOVA, returning an F-value and probability given
    any number of groups.  From Heiman, pp.394-7.

    Usage: ``f_oneway(*args)``, where ``*args`` is 2 or more arrays,
    one per treatment group.

    Returns
    -------
    statistic : float
        The computed F-value of the test.
    pvalue : float
        The associated p-value from the F-distribution.

    """
    # Construct a single array of arguments: each row is a group
    data = argstoarray(*args)
    ngroups = len(data)
    ntot = data.count()
    sstot = (data**2).sum() - (data.sum())**2/float(ntot)
    ssbg = (data.count(-1) * (data.mean(-1)-data.mean())**2).sum()
    sswg = sstot-ssbg
    dfbg = ngroups-1
    dfwg = ntot - ngroups
    msb = ssbg/float(dfbg)
    msw = sswg/float(dfwg)
    f = msb/msw
    prob = special.fdtrc(dfbg, dfwg, f)  # equivalent to stats.f.sf

    return F_onewayResult(f, prob)
