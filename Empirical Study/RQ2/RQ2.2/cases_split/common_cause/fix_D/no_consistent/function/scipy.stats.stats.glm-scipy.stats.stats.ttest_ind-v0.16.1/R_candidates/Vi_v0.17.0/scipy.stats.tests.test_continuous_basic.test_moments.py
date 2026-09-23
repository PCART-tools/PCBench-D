@npt.dec.slow
def test_moments():
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',
                                category=integrate.IntegrationWarning)
        knf = npt.dec.knownfailureif
        fail_normalization = set(['vonmises', 'ksone'])
        fail_higher = set(['vonmises', 'ksone', 'ncf'])
        for distname, arg in distcont[:]:
            if distname is 'levy_stable':
                continue
            distfn = getattr(stats, distname)
            m, v, s, k = distfn.stats(*arg, moments='mvsk')
            cond1 = distname in fail_normalization
            cond2 = distname in fail_higher
            msg = distname + ' fails moments'
            yield knf(cond1, msg)(check_normalization), distfn, arg, distname
            yield knf(cond2, msg)(check_mean_expect), distfn, arg, m, distname
            yield (knf(cond2, msg)(check_var_expect), distfn, arg, m, v,
                   distname)
            yield (knf(cond2, msg)(check_skew_expect), distfn, arg, m, v, s,
                   distname)
            yield (knf(cond2, msg)(check_kurt_expect), distfn, arg, m, v, k,
                   distname)
            yield check_loc_scale, distfn, arg, m, v, distname
            yield check_moment, distfn, arg, m, v, distname
