def test_check_grad():
    # Verify if check_grad is able to estimate the derivative of the
    # logistic function.

    def logit(x):
        return 1 / (1 + np.exp(-x))

    def der_logit(x):
        return np.exp(-x) / (1 + np.exp(-x))**2

    x0 = np.array([1.5])

    r = optimize.check_grad(logit, der_logit, x0)
    assert_almost_equal(r, 0)

    r = optimize.check_grad(logit, der_logit, x0, epsilon=1e-6)
    assert_almost_equal(r, 0)

    # Check if the epsilon parameter is being considered.
    r = abs(optimize.check_grad(logit, der_logit, x0, epsilon=1e-1) - 0)
    assert_(r > 1e-7)
