def test_rvs_shape():
    # Check that rvs parses the mean and covariance correctly, and returns
    # an array of the right shape
    N = 300
    d = 4
    sample = multivariate_normal.rvs(mean=np.zeros(d), cov=1, size=N)
    assert_equal(sample.shape, (N, d))

    sample = multivariate_normal.rvs(mean=None,
                                     cov=np.array([[2, .1], [.1, 1]]),
                                     size=N)
    assert_equal(sample.shape, (N, 2))

    u = multivariate_normal(mean=0, cov=1)
    sample = u.rvs(N)
    assert_equal(sample.shape, (N, ))
