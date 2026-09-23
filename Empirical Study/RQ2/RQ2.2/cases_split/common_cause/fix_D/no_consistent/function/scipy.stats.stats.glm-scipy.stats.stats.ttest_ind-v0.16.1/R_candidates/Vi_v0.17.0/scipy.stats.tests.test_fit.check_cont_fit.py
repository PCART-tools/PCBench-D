def check_cont_fit(distname,arg):
    if distname in failing_fits:
        # Skip failing fits unless overridden
        xfail = True
        try:
            xfail = not int(os.environ['SCIPY_XFAIL'])
        except:
            pass
        if xfail:
            msg = "Fitting %s doesn't work reliably yet" % distname
            msg += " [Set environment variable SCIPY_XFAIL=1 to run this test nevertheless.]"
            dec.knownfailureif(True, msg)(lambda: None)()

    distfn = getattr(stats, distname)

    truearg = np.hstack([arg,[0.0,1.0]])
    diffthreshold = np.max(np.vstack([truearg*thresh_percent,
                                      np.ones(distfn.numargs+2)*thresh_min]),0)

    for fit_size in fit_sizes:
        # Note that if a fit succeeds, the other fit_sizes are skipped
        np.random.seed(1234)

        with np.errstate(all='ignore'):
            rvs = distfn.rvs(size=fit_size, *arg)
            est = distfn.fit(rvs)  # start with default values

        diff = est - truearg

        # threshold for location
        diffthreshold[-2] = np.max([np.abs(rvs.mean())*thresh_percent,thresh_min])

        if np.any(np.isnan(est)):
            raise AssertionError('nan returned in fit')
        else:
            if np.all(np.abs(diff) <= diffthreshold):
                break
    else:
        txt = 'parameter: %s\n' % str(truearg)
        txt += 'estimated: %s\n' % str(est)
        txt += 'diff     : %s\n' % str(diff)
        raise AssertionError('fit not very good in %s\n' % distfn.name + txt)
