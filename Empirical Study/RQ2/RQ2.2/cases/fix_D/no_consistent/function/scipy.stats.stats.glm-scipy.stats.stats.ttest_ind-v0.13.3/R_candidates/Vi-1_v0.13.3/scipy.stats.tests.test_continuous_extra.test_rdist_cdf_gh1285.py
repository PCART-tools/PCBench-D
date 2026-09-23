@npt.dec.slow
def test_rdist_cdf_gh1285():
    # check workaround in rdist._cdf for issue gh-1285.
    distfn = stats.rdist
    values = [0.001, 0.5, 0.999]
    npt.assert_almost_equal(distfn.cdf(distfn.ppf(values, 541.0), 541.0),
                            values, decimal=5)
