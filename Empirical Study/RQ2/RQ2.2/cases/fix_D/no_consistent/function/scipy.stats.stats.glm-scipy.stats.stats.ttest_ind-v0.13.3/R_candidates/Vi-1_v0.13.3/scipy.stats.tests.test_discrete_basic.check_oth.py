def check_oth(distfn, arg, msg):
    # checking other methods of distfn
    meanint = round(float(distfn.stats(*arg)[0]))  # closest integer to mean
    npt.assert_almost_equal(distfn.sf(meanint, *arg), 1 -
                            distfn.cdf(meanint, *arg), decimal=8)
    median_sf = distfn.isf(0.5, *arg)

    npt.assert_(distfn.sf(median_sf - 1, *arg) > 0.5)
    npt.assert_(distfn.cdf(median_sf + 1, *arg) > 0.5)
    npt.assert_equal(distfn.isf(0.5, *arg), distfn.ppf(0.5, *arg))
