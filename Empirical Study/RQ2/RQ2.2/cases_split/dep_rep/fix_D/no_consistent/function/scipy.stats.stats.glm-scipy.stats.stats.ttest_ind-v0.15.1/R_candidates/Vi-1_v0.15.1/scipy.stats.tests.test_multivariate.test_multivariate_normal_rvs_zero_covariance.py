def test_multivariate_normal_rvs_zero_covariance():
    mean = np.zeros(2)
    covariance = np.zeros((2, 2))
    model = multivariate_normal(mean, covariance, allow_singular=True)
    sample = model.rvs()
    assert_equal(sample, [0, 0])
