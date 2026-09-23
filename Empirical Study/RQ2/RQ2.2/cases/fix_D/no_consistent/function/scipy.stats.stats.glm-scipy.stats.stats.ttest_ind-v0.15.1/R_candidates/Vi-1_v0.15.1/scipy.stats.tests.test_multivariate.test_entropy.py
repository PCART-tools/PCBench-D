def test_entropy():
    np.random.seed(2846)

    n = 3
    mean = np.random.randn(n)
    M = np.random.randn(n, n)
    cov = np.dot(M, M.T)

    rv = multivariate_normal(mean, cov)

    # Check that frozen distribution agrees with entropy function
    assert_almost_equal(rv.entropy(), multivariate_normal.entropy(mean, cov))
    # Compare entropy with manually computed expression involving
    # the sum of the logs of the eigenvalues of the covariance matrix
    eigs = np.linalg.eig(cov)[0]
    desired = 1 / 2 * (n * (np.log(2 * np.pi) + 1) + np.sum(np.log(eigs)))
    assert_almost_equal(desired, rv.entropy())
