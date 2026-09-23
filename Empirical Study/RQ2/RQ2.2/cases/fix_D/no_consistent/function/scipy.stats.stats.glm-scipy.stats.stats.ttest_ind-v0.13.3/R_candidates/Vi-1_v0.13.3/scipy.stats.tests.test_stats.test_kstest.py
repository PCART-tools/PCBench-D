def test_kstest():
    # from numpy.testing import assert_almost_equal

    # comparing with values from R
    x = np.linspace(-1,1,9)
    D,p = stats.kstest(x,'norm')
    assert_almost_equal(D, 0.15865525393145705, 12)
    assert_almost_equal(p, 0.95164069201518386, 1)

    x = np.linspace(-15,15,9)
    D,p = stats.kstest(x,'norm')
    assert_almost_equal(D, 0.44435602715924361, 15)
    assert_almost_equal(p, 0.038850140086788665, 8)

    # the following tests rely on deterministicaly replicated rvs
    np.random.seed(987654321)
    x = stats.norm.rvs(loc=0.2, size=100)
    D,p = stats.kstest(x, 'norm', mode='asymp')
    assert_almost_equal(D, 0.12464329735846891, 15)
    assert_almost_equal(p, 0.089444888711820769, 15)
    assert_almost_equal(np.array(stats.kstest(x, 'norm', mode='asymp')),
                np.array((0.12464329735846891, 0.089444888711820769)), 15)
    assert_almost_equal(np.array(stats.kstest(x,'norm', alternative='less')),
                np.array((0.12464329735846891, 0.040989164077641749)), 15)
    # this 'greater' test fails with precision of decimal=14
    assert_almost_equal(np.array(stats.kstest(x,'norm', alternative='greater')),
                np.array((0.0072115233216310994, 0.98531158590396228)), 12)
