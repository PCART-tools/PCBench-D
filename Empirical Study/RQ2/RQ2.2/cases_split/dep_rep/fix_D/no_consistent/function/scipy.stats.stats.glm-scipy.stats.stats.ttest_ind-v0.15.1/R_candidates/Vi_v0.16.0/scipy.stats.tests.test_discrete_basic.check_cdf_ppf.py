def check_cdf_ppf(distfn, arg, supp, msg):
    # cdf is a step function, and ppf(q) = min{k : cdf(k) >= q, k integer}
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp, *arg), *arg),
                           supp, msg + '-roundtrip')
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp, *arg) - 1e-8, *arg),
                           supp, msg + '-roundtrip')
    supp1 = supp[supp < distfn.b]
    npt.assert_array_equal(distfn.ppf(distfn.cdf(supp1, *arg) + 1e-8, *arg),
                     supp1 + distfn.inc, msg + 'ppf-cdf-next')
