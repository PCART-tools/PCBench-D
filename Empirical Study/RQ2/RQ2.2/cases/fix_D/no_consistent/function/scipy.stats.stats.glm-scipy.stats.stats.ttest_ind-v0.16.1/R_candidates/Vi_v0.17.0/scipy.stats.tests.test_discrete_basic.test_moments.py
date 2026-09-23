def test_moments():
    for distname, arg in distdiscrete:
        try:
            distfn = getattr(stats, distname)
        except TypeError:
            distfn = distname
            distname = 'sample distribution'
        m, v, s, k = distfn.stats(*arg, moments='mvsk')
        yield check_normalization, distfn, arg, distname

        # compare `stats` and `moment` methods
        yield check_moment, distfn, arg, m, v, distname
        yield check_mean_expect, distfn, arg, m, distname
        yield check_var_expect, distfn, arg, m, v, distname
        yield check_skew_expect, distfn, arg, m, v, s, distname

        cond = distname in ['zipf']
        msg = distname + ' fails kurtosis'
        yield knf(cond, msg)(check_kurt_expect), distfn, arg, m, v, k, distname

        # frozen distr moments
        yield check_moment_frozen, distfn, arg, m, 1
        yield check_moment_frozen, distfn, arg, v+m*m, 2
