@npt.dec.slow
def test_discrete_extra():
    for distname, arg in distdiscrete:
        distfn = getattr(stats,distname)
        yield check_ppf_limits, distfn, arg, distname + \
              ' ppf limit test'
        yield check_isf_limits, distfn, arg, distname + \
              ' isf limit test'
        yield check_entropy, distfn, arg, distname + \
              ' entropy nan test'
