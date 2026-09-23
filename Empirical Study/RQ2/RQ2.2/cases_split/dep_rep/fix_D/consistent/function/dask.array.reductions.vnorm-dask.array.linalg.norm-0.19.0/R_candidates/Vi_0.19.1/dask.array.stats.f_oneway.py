@doc_wraps(scipy.stats.f_oneway)
def f_oneway(*args):
    # args = [np.asarray(arg, dtype=float) for arg in args]
    # ANOVA on N groups, each in its own array
    num_groups = len(args)
    alldata = da.concatenate(args)
    bign = len(alldata)

    # Determine the mean of the data, and subtract that from all inputs to a
    # variance (via sum_of_sq / sq_of_sum) calculation.  Variance is invariance
    # to a shift in location, and centering all data around zero vastly
    # improves numerical stability.
    offset = alldata.mean()
    alldata -= offset

    sstot = _sum_of_squares(alldata) - (_square_of_sums(alldata) / float(bign))
    ssbn = 0
    for a in args:
        ssbn += _square_of_sums(a - offset) / float(len(a))

    # Naming: variables ending in bn/b are for "between treatments", wn/w are
    # for "within treatments"
    ssbn -= (_square_of_sums(alldata) / float(bign))
    sswn = sstot - ssbn
    dfbn = num_groups - 1
    dfwn = bign - num_groups
    msb = ssbn / float(dfbn)
    msw = sswn / float(dfwn)
    f = msb / msw

    prob = _fdtrc(dfbn, dfwn, f)   # equivalent to stats.f.sf

    return delayed(F_onewayResult, nout=2)(f, prob)
