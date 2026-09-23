@npt.dec.skipif(True)
def test_discrete_private():
    # testing private methods mostly for debugging
    #   some tests might fail by design,
    #   e.g. incorrect definition of distfn.a and distfn.b
    for distname, arg in distdiscrete:
        distfn = getattr(stats,distname)
        rvs = distfn.rvs(size=10000,*arg)
        m,v = distfn.stats(*arg)

        yield check_ppf_ppf, distfn, arg
        yield check_cdf_ppf_private, distfn, arg, distname
        yield check_generic_moment, distfn, arg, m, 1, 3   # last is decimal
        yield check_generic_moment, distfn, arg, v+m*m, 2, 3  # last is decimal
        yield check_moment_frozen, distfn, arg, m, 1, 3   # last is decimal
        yield check_moment_frozen, distfn, arg, v+m*m, 2, 3  # last is decimal
