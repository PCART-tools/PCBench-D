def check_cdf_ppf_private(distfn,arg,msg):
    ppf05 = distfn._ppf(0.5,*arg)
    cdf05 = distfn.cdf(ppf05,*arg)
    npt.assert_almost_equal(distfn._ppf(cdf05-1e-6,*arg),ppf05,
                            err_msg=msg + '_ppf-cdf-median ')
    npt.assert_((distfn._ppf(cdf05+1e-4,*arg) > ppf05), msg + '_ppf-cdf-next')
