def test_frozen_dirichlet():
    np.random.seed(2846)

    n = np.random.randint(1, 32)
    alpha = np.random.uniform(10e-10, 100, n)

    d = dirichlet(alpha)

    assert_equal(d.var(), dirichlet.var(alpha))
    assert_equal(d.mean(), dirichlet.mean(alpha))
    assert_equal(d.entropy(), dirichlet.entropy(alpha))
    num_tests = 10
    for i in range(num_tests):
        x = np.random.uniform(10e-10, 100, n)
        x /= np.sum(x)
        assert_equal(d.pdf(x[:-1]), dirichlet.pdf(x[:-1], alpha))
        assert_equal(d.logpdf(x[:-1]), dirichlet.logpdf(x[:-1], alpha))
