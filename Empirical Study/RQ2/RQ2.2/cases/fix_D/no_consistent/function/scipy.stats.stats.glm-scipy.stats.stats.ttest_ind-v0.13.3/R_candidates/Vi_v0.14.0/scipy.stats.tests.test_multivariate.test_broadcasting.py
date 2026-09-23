def test_broadcasting():
    np.random.seed(1234)
    n = 4

    # Construct a random covariance matrix.
    data = np.random.randn(n, n)
    cov = np.dot(data, data.T)
    mean = np.random.randn(n)

    # Construct an ndarray which can be interpreted as
    # a 2x3 array whose elements are random data vectors.
    X = np.random.randn(2, 3, n)

    # Check that multiple data points can be evaluated at once.
    for i in range(2):
        for j in range(3):
            actual = multivariate_normal.pdf(X[i, j], mean, cov)
            desired = multivariate_normal.pdf(X, mean, cov)[i, j]
            assert_allclose(actual, desired)
