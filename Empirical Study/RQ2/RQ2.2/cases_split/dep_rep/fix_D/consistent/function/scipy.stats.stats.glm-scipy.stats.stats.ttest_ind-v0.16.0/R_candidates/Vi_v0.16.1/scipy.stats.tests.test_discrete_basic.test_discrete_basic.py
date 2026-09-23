def test_discrete_basic():
    for distname, arg in distdiscrete:
        distfn = getattr(stats, distname)
        np.random.seed(9765456)
        rvs = distfn.rvs(size=2000, *arg)
        supp = np.unique(rvs)
        m, v = distfn.stats(*arg)
        yield check_cdf_ppf, distfn, arg, supp, distname + ' cdf_ppf'

        yield check_pmf_cdf, distfn, arg, distname
        yield check_oth, distfn, arg, supp, distname + ' oth'
        yield check_edge_support, distfn, arg

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
        yield check_random_state_property, distfn, arg

        # Entropy
        yield check_entropy, distfn, arg, distname
        if distfn.__class__._entropy != stats.rv_discrete._entropy:
            yield check_private_entropy, distfn, arg, stats.rv_discrete
