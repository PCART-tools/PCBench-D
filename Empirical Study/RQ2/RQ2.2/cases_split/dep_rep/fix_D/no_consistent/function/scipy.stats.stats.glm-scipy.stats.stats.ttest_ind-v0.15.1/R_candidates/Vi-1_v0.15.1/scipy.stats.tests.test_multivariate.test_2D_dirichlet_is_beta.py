def test_2D_dirichlet_is_beta():
    np.random.seed(2846)

    alpha = np.random.uniform(10e-10, 100, 2)
    d = dirichlet(alpha)
    b = beta(alpha[0], alpha[1])

    num_tests = 10
    for i in range(num_tests):
        x = np.random.uniform(10e-10, 100, 2)
        x /= np.sum(x)
        assert_almost_equal(b.pdf(x), d.pdf([x]))

    assert_almost_equal(b.mean(), d.mean()[0])
    assert_almost_equal(b.var(), d.var()[0])
