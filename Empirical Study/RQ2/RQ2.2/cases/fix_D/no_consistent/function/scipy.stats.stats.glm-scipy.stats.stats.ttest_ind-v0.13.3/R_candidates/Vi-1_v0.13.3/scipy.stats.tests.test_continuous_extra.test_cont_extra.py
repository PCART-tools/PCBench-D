@npt.dec.slow
def test_cont_extra():
    for distname, arg in distcont[:]:
        distfn = getattr(stats, distname)

        yield check_ppf_limits, distfn, arg, distname + \
              ' ppf limit test'
        yield check_isf_limits, distfn, arg, distname + \
              ' isf limit test'
        yield check_loc_scale, distfn, arg, distname + \
              ' loc, scale test'
