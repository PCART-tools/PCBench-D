def check_pmf_cdf(distfn, arg, distname):
    startind = np.int(distfn.ppf(0.01, *arg) - 1)
    index = list(range(startind, startind + 10))
    cdfs, pmfs_cum = distfn.cdf(index,*arg), distfn.pmf(index, *arg).cumsum()

    atol, rtol = 1e-10, 1e-10
    if distname == 'skellam':    # ncx2 accuracy
        atol, rtol = 1e-5, 1e-5
    npt.assert_allclose(cdfs - cdfs[0], pmfs_cum - pmfs_cum[0],
            atol=atol, rtol=rtol)
