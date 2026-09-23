def test_large_sample():
    # Generate large sample and compare sample mean and sample covariance
    # with mean and covariance matrix.

    np.random.seed(2846)

    n = 3
    mean = np.random.randn(n)
    M = np.random.randn(n, n)
    cov = np.dot(M, M.T)
    size = 5000

    sample = multivariate_normal.rvs(mean, cov, size)

    assert_allclose(numpy.cov(sample.T), cov, rtol=1e-1)
    assert_allclose(sample.mean(0), mean, rtol=1e-1)
