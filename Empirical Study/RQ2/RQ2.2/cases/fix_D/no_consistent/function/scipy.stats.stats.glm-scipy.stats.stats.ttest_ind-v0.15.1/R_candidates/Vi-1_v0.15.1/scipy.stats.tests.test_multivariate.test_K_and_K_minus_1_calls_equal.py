def test_K_and_K_minus_1_calls_equal():
    # Test that calls with K and K-1 entries yield the same results.

    np.random.seed(2846)

    n = np.random.randint(1, 32)
    alpha = np.random.uniform(10e-10, 100, n)

    d = dirichlet(alpha)
    num_tests = 10
    for i in range(num_tests):
        x = np.random.uniform(10e-10, 100, n)
        x /= np.sum(x)
        assert_almost_equal(d.pdf(x[:-1]), d.pdf(x))
