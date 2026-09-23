def check_cdf_ppf2(distfn,arg,supp,msg):
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp,*arg),*arg),
                           supp, msg + '-roundtrip')
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp,*arg)-1e-8,*arg),
                           supp, msg + '-roundtrip')
