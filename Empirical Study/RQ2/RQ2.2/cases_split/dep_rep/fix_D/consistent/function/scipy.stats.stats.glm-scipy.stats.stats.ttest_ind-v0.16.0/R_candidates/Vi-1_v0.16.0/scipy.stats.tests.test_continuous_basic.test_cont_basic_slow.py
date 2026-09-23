@npt.dec.slow
def test_cont_basic_slow():
    # same as above for slow distributions
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=integrate.IntegrationWarning)
        for distname, arg in distcont[:]:
            if distname not in distslow:
                continue
            if distname is 'levy_stable':
                continue
            distfn = getattr(stats, distname)
            np.random.seed(765456)
            sn = 500
            rvs = distfn.rvs(size=sn,*arg)
            sm = rvs.mean()
            sv = rvs.var()
            m, v = distfn.stats(*arg)
            yield check_sample_meanvar_, distfn, arg, m, v, sm, sv, sn, \
                  distname + 'sample mean test'
            yield check_cdf_ppf, distfn, arg, distname
            yield check_sf_isf, distfn, arg, distname
            yield check_pdf, distfn, arg, distname
            yield check_pdf_logpdf, distfn, arg, distname
            yield check_cdf_logcdf, distfn, arg, distname
            yield check_sf_logsf, distfn, arg, distname
            # yield check_oth, distfn, arg # is still missing
            if distname in distmissing:
                alpha = 0.01
                yield check_distribution_rvs, distname, arg, alpha, rvs

            locscale_defaults = (0, 1)
            meths = [distfn.pdf, distfn.logpdf, distfn.cdf, distfn.logcdf,
                     distfn.logsf]
            # make sure arguments are within support
            x = 0.5
            if distname == 'invweibull':
                arg = (1,)
            elif distname == 'ksone':
                arg = (3,)
            yield check_named_args, distfn, x, arg, locscale_defaults, meths
            yield check_random_state_property, distfn, arg

            # Entropy
            skp = npt.dec.skipif
            ks_cond = distname in ['ksone', 'kstwobign']
            yield skp(ks_cond)(check_entropy), distfn, arg, distname

            if distfn.numargs == 0:
                yield skp(NUMPY_BELOW_1_7)(check_vecentropy), distfn, arg
            if distfn.__class__._entropy != stats.rv_continuous._entropy:
                yield check_private_entropy, distfn, arg, stats.rv_continuous

            yield check_edge_support, distfn, arg
