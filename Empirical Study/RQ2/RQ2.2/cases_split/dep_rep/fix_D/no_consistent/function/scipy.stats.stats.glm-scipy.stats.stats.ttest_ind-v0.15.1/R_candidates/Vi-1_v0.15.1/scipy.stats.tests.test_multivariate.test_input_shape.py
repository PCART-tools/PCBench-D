def test_input_shape():
    mu = np.arange(3)
    cov = np.identity(2)
    assert_raises(ValueError, multivariate_normal.pdf, (0, 1), mu, cov)
    assert_raises(ValueError, multivariate_normal.pdf, (0, 1, 2), mu, cov)
