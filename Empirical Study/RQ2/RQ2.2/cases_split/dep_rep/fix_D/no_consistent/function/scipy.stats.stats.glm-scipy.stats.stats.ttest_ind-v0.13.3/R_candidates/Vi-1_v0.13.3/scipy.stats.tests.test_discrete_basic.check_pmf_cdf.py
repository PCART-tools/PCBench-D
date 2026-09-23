def check_pmf_cdf(distfn, arg, msg):
    startind = np.int(distfn._ppf(0.01,*arg)-1)
    index = list(range(startind,startind+10))
    cdfs = distfn.cdf(index,*arg)
    npt.assert_almost_equal(cdfs, distfn.pmf(index, *arg).cumsum() +
                            cdfs[0] - distfn.pmf(index[0],*arg),
                            decimal=4, err_msg=msg + 'pmf-cdf')
