def test_kendalltau():
    # with some ties
    x1 = [12, 2, 1, 12, 2]
    x2 = [1, 4, 7, 1, 0]
    expected = (-0.47140452079103173, 0.24821309157521476)
    res = stats.kendalltau(x1, x2)
    assert_approx_equal(res[0], expected[0])
    assert_approx_equal(res[1], expected[1])

    # with only ties in one or both inputs
    assert_(np.all(np.isnan(stats.kendalltau([2,2,2], [2,2,2]))))
    assert_(np.all(np.isnan(stats.kendalltau([2,0,2], [2,2,2]))))
    assert_(np.all(np.isnan(stats.kendalltau([2,2,2], [2,0,2]))))

    # check two different sort methods
    assert_approx_equal(stats.kendalltau(x1, x2, initial_lexsort=False)[1],
                        stats.kendalltau(x1, x2, initial_lexsort=True)[1])

    # and with larger arrays
    np.random.seed(7546)
    x = np.array([np.random.normal(loc=1, scale=1, size=500),
                np.random.normal(loc=1, scale=1, size=500)])
    corr = [[1.0, 0.3],
            [0.3, 1.0]]
    x = np.dot(np.linalg.cholesky(corr), x)
    expected = (0.19291382765531062, 1.1337108207276285e-10)
    res = stats.kendalltau(x[0], x[1])
    assert_approx_equal(res[0], expected[0])
    assert_approx_equal(res[1], expected[1])

    # and do we get a tau of 1 for identical inputs?
    assert_approx_equal(stats.kendalltau([1,1,2], [1,1,2])[0], 1.0)
