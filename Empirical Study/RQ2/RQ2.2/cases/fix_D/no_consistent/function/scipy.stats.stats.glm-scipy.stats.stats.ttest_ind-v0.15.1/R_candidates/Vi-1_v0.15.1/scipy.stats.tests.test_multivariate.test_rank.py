def test_rank():
    # Check that the rank is detected correctly.
    np.random.seed(1234)
    n = 4
    mean = np.random.randn(n)
    for expected_rank in range(1, n + 1):
        s = np.random.randn(n, expected_rank)
        cov = np.dot(s, s.T)
        distn = multivariate_normal(mean, cov, allow_singular=True)
        assert_equal(distn.cov_info.rank, expected_rank)
