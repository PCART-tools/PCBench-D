def test_chisquare_masked_arrays():
    # Test masked arrays.
    obs = np.array([[8, 8, 16, 32, -1], [-1, -1, 3, 4, 5]]).T
    mask = np.array([[0, 0, 0, 0, 1], [1, 1, 0, 0, 0]]).T
    mobs = np.ma.masked_array(obs, mask)
    expected_chisq = np.array([24.0, 0.5])
    expected_g = np.array([2*(2*8*np.log(0.5) + 32*np.log(2.0)),
                           2*(3*np.log(0.75) + 5*np.log(1.25))])

    chi2 = stats.distributions.chi2

    chisq, p = stats.chisquare(mobs)
    mat.assert_array_equal(chisq, expected_chisq)
    mat.assert_array_almost_equal(p, chi2.sf(expected_chisq,
                                             mobs.count(axis=0) - 1))

    g, p = stats.power_divergence(mobs, lambda_='log-likelihood')
    mat.assert_array_almost_equal(g, expected_g, decimal=15)
    mat.assert_array_almost_equal(p, chi2.sf(expected_g,
                                             mobs.count(axis=0) - 1))

    chisq, p = stats.chisquare(mobs.T, axis=1)
    mat.assert_array_equal(chisq, expected_chisq)
    mat.assert_array_almost_equal(p, chi2.sf(expected_chisq,
                                             mobs.T.count(axis=1) - 1))
    g, p = stats.power_divergence(mobs.T, axis=1, lambda_="log-likelihood")
    mat.assert_array_almost_equal(g, expected_g, decimal=15)
    mat.assert_array_almost_equal(p, chi2.sf(expected_g,
                                             mobs.count(axis=0) - 1))

    obs1 = np.ma.array([3, 5, 6, 99, 10], mask=[0, 0, 0, 1, 0])
    exp1 = np.ma.array([2, 4, 8, 10, 99], mask=[0, 0, 0, 0, 1])
    chi2, p = stats.chisquare(obs1, f_exp=exp1)
    # Because of the mask at index 3 of obs1 and at index 4 of exp1,
    # only the first three elements are included in the calculation
    # of the statistic.
    mat.assert_array_equal(chi2, 1/2 + 1/4 + 4/8)

    # When axis=None, the two values should have type np.float64.
    chisq, p = stats.chisquare(np.ma.array([1,2,3]), axis=None)
    assert_(isinstance(chisq, np.float64))
    assert_(isinstance(p, np.float64))
    assert_equal(chisq, 1.0)
    assert_almost_equal(p, stats.distributions.chi2.sf(1.0, 2))

    # Empty arrays:
    # A data set with length 0 returns a masked scalar.
    with np.errstate(invalid='ignore'):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            chisq, p = stats.chisquare(np.ma.array([]))
    assert_(isinstance(chisq, np.ma.MaskedArray))
    assert_equal(chisq.shape, ())
    assert_(chisq.mask)

    empty3 = np.ma.array([[],[],[]])

    # empty3 is a collection of 0 data sets (whose lengths would be 3, if
    # there were any), so the return value is an array with length 0.
    chisq, p = stats.chisquare(empty3)
    assert_(isinstance(chisq, np.ma.MaskedArray))
    mat.assert_array_equal(chisq, [])

    # empty3.T is an array containing 3 data sets, each with length 0,
    # so an array of size (3,) is returned, with all values masked.
    with np.errstate(invalid='ignore'):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            chisq, p = stats.chisquare(empty3.T)

    assert_(isinstance(chisq, np.ma.MaskedArray))
    assert_equal(chisq.shape, (3,))
    assert_(np.all(chisq.mask))
