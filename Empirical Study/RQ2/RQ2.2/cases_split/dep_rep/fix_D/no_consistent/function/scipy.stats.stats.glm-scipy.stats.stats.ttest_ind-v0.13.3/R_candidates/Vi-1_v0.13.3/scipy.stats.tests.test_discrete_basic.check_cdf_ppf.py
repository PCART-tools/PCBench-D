def check_cdf_ppf(distfn,arg,msg):
    ppf05 = distfn.ppf(0.5,*arg)
    cdf05 = distfn.cdf(ppf05,*arg)
    npt.assert_almost_equal(distfn.ppf(cdf05-1e-6,*arg),ppf05,
                            err_msg=msg + 'ppf-cdf-median')
    npt.assert_((distfn.ppf(cdf05+1e-4,*arg) > ppf05), msg + 'ppf-cdf-next')
