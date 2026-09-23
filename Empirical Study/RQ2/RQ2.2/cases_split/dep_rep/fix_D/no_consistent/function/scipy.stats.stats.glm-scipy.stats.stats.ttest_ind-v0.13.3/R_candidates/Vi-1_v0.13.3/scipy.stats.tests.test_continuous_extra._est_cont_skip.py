@npt.dec.slow
def _est_cont_skip():
    for distname, arg in distcont:
        distfn = getattr(stats, distname)
        #entropy test checks only for isnan, currently 6 isnan left
        yield check_entropy, distfn, arg, distname + \
              ' entropy nan test'
        # _ppf test has 1 failure be design
        yield check_ppf_private, distfn, arg, distname + \
              ' _ppf private test'
