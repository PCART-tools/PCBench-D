@npt.dec.slow
def test_cont_basic_slow():
    # same as above for slow distributions
    for distname, arg in distcont[:]:
        if distname not in distslow:
            continue
        distfn = getattr(stats, distname)
        np.random.seed(765456)
        sn = 500
        rvs = distfn.rvs(size=sn,*arg)
        sm = rvs.mean()
        sv = rvs.var()
        skurt = stats.kurtosis(rvs)
        sskew = stats.skew(rvs)
        m,v = distfn.stats(*arg)
        yield check_sample_meanvar_, distfn, arg, m, v, sm, sv, sn, distname + \
              'sample mean test'
        # the sample skew kurtosis test has known failures, not very good distance measure
        # yield check_sample_skew_kurt, distfn, arg, sskew, skurt, distname
        yield check_moment, distfn, arg, m, v, distname
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
