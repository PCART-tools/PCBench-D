def test_discrete_basic():
    for distname, arg in distdiscrete:
        distfn = getattr(stats,distname)
        # npt.assert_(stats.dlaplace.rvs(0.8) is not None)
        np.random.seed(9765456)
        rvs = distfn.rvs(size=2000,*arg)
        supp = np.unique(rvs)
        m,v = distfn.stats(*arg)
        # yield npt.assert_almost_equal(rvs.mean(), m, decimal=4,err_msg='mean')
        # yield npt.assert_almost_equal, rvs.mean(), m, 2, 'mean' # does not work
        yield check_sample_meanvar, rvs.mean(), m, distname + ' sample mean test'
        yield check_sample_meanvar, rvs.var(), v, distname + ' sample var test'
        yield check_cdf_ppf, distfn, arg, distname + ' cdf_ppf'
        yield check_cdf_ppf2, distfn, arg, supp, distname + ' cdf_ppf'
        yield check_pmf_cdf, distfn, arg, distname + ' pmf_cdf'

        # zipf doesn't fail, but generates floating point warnings.
        # Should be checked.
        if not distname in ['zipf']:
            yield check_oth, distfn, arg, distname + ' oth'
            skurt = stats.kurtosis(rvs)
            sskew = stats.skew(rvs)
            yield check_sample_skew_kurt, distfn, arg, skurt, sskew, \
                          distname + ' skew_kurt'

        # dlaplace doesn't fail, but generates lots of floating point warnings.
        # Should be checked.
        if not distname in ['dlaplace']:  # ['logser']:  #known failure, fixed
            alpha = 0.01
            yield check_discrete_chisquare, distfn, arg, rvs, alpha, \
                          distname + ' chisquare'

    seen = set()
    for distname, arg in distdiscrete:
        if distname in seen:
            continue
        seen.add(distname)
        distfn = getattr(stats,distname)
        locscale_defaults = (0,)
        meths = [distfn.pmf, distfn.logpmf, distfn.cdf, distfn.logcdf,
                 distfn.logsf]
        # make sure arguments are within support
        spec_k = {'randint': 11, 'hypergeom': 4, 'bernoulli': 0, }
        k = spec_k.get(distname, 1)
        yield check_named_args, distfn, k, arg, locscale_defaults, meths
        yield check_scale_docstring, distfn
