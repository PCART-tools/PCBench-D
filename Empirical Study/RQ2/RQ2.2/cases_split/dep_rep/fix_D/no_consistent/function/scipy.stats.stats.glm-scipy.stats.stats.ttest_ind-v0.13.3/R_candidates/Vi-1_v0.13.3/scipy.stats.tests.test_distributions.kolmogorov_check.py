def kolmogorov_check(diststr, args=(), N=20, significance=0.01):
    qtest = stats.ksoneisf(significance, N)
    cdf = eval('stats.'+diststr+'.cdf')
    dist = eval('stats.'+diststr)
    # Get random numbers
    kwds = {'size':N}
    vals = numpy.sort(dist.rvs(*args, **kwds))
    cdfvals = cdf(vals, *args)
    q = max(abs(cdfvals - np.arange(1.0, N+1)/N))
    assert_(q < qtest, msg="Failed q=%f, bound=%f, alpha=%f" % (q, qtest, significance))
    return
