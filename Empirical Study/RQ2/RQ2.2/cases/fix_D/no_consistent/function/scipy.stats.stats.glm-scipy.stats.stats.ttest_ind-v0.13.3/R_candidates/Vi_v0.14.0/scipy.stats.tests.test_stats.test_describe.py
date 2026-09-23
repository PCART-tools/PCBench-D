def test_describe():
    x = np.vstack((np.ones((3,4)),2*np.ones((2,4))))
    nc, mmc = (5, ([1., 1., 1., 1.], [2., 2., 2., 2.]))
    mc = np.array([1.4, 1.4, 1.4, 1.4])
    vc = np.array([0.3, 0.3, 0.3, 0.3])
    skc = [0.40824829046386357]*4
    kurtc = [-1.833333333333333]*4
    n, mm, m, v, sk, kurt = stats.describe(x)
    assert_equal(n, nc)
    assert_equal(mm, mmc)
    assert_equal(m, mc)
    assert_equal(v, vc)
    assert_array_almost_equal(sk, skc, decimal=13)  # not sure about precision
    assert_array_almost_equal(kurt, kurtc, decimal=13)
    n, mm, m, v, sk, kurt = stats.describe(x.T, axis=1)
    assert_equal(n, nc)
    assert_equal(mm, mmc)
    assert_equal(m, mc)
    assert_equal(v, vc)
    assert_array_almost_equal(sk, skc, decimal=13)  # not sure about precision
    assert_array_almost_equal(kurt, kurtc, decimal=13)
