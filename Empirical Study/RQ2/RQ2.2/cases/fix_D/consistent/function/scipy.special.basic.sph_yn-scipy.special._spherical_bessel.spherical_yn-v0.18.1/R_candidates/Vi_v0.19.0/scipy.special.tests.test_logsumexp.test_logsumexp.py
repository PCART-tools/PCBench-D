def test_logsumexp():
    # Test whether logsumexp() function correctly handles large inputs.
    a = np.arange(200)
    desired = np.log(np.sum(np.exp(a)))
    assert_almost_equal(logsumexp(a), desired)

    # Now test with large numbers
    b = [1000, 1000]
    desired = 1000.0 + np.log(2.0)
    assert_almost_equal(logsumexp(b), desired)

    n = 1000
    b = np.ones(n) * 10000
    desired = 10000.0 + np.log(n)
    assert_almost_equal(logsumexp(b), desired)

    x = np.array([1e-40] * 1000000)
    logx = np.log(x)

    X = np.vstack([x, x])
    logX = np.vstack([logx, logx])
    assert_array_almost_equal(np.exp(logsumexp(logX)), X.sum())
    assert_array_almost_equal(np.exp(logsumexp(logX, axis=0)), X.sum(axis=0))
    assert_array_almost_equal(np.exp(logsumexp(logX, axis=1)), X.sum(axis=1))

    # Handling special values properly
    assert_equal(logsumexp(np.inf), np.inf)
    assert_equal(logsumexp(-np.inf), -np.inf)
    assert_equal(logsumexp(np.nan), np.nan)
    assert_equal(logsumexp([-np.inf, -np.inf]), -np.inf)

    # Handling an array with different magnitudes on the axes
    assert_array_almost_equal(logsumexp([[1e10, 1e-10],
                                         [-1e10, -np.inf]], axis=-1),
                              [1e10, -1e10])

    # Test keeping dimensions
    assert_array_almost_equal(logsumexp([[1e10, 1e-10],
                                         [-1e10, -np.inf]],
                                        axis=-1,
                                        keepdims=True),
                              [[1e10], [-1e10]])

    # Test multiple axes
    assert_array_almost_equal(logsumexp([[1e10, 1e-10],
                                         [-1e10, -np.inf]],
                                        axis=(-1,-2)),
                              1e10)
