def test_exception_singular_cov():
    np.random.seed(1234)
    x = np.random.randn(5)
    mean = np.random.randn(5)
    cov = np.ones((5, 5))
    e = np.linalg.LinAlgError
    assert_raises(e, multivariate_normal, mean, cov)
    assert_raises(e, multivariate_normal.pdf, x, mean, cov)
    assert_raises(e, multivariate_normal.logpdf, x, mean, cov)
